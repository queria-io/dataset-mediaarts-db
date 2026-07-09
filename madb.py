"""メディア芸術データベース（MADB）データセットの取得・展開。

公式データセットリポジトリ（github.com/mediaarts-db/dataset）から
マンガ単行本（cm101）の JSON-LD zip を取得し、class:MangaBook ノードを
スカラー列に平坦化した NDJSON へ変換する。

JSON-LD の値は文字列・言語タグ付き dict・それらの list が混在するため、
平坦化（プレーン文字列と ja-hrkt 読みの分離、URI からの ID 抽出）は
SQL ではなくここで行い、dbt には列が確定した NDJSON を渡す。
"""

import io
import json
import re
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ZIP_URL = (
    "https://raw.githubusercontent.com/mediaarts-db/dataset"
    "/main/data/json-ld/metadata_cm-item_cm101_json.zip"
)

# 平坦化した NDJSON の列（すべて文字列。型変換は stg で行う）
FIELDS = [
    "book_id",
    "title",
    "title_kana",
    "alternate_title",
    "volume",
    "volume_sort",
    "series_id",
    "series_name",
    "creator_id",
    "creator_statement",
    "publisher_name",
    "publisher_name_kana",
    "publisher_code",
    "brand",
    "brand_kana",
    "date_published",
    "publication_place",
    "language",
    "isbn",
    "jpno",
    "ndc",
    "product_id",
    "pages",
    "book_size",
    "price",
    "note",
]

_JOIN = " | "


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _plains(value) -> list[str]:
    """言語タグの無いプレーン文字列のみを取り出す。"""
    return [v for v in _as_list(value) if isinstance(v, str)]


def _kana(value) -> str | None:
    """ja-hrkt（ひらがな・カタカナ読み）の値を取り出す。"""
    values = [
        v["@value"]
        for v in _as_list(value)
        if isinstance(v, dict) and v.get("@language") == "ja-hrkt"
    ]
    return _JOIN.join(values) or None


def _join(values: list[str]) -> str | None:
    return _JOIN.join(values) or None


def _id_suffix(uri: str) -> str:
    """リソース URI 末尾の ID（M189456 / C57152 等）を取り出す。"""
    return uri.rstrip("/").rsplit("/", 1)[-1]


def _creator_id(node: dict) -> str | None:
    # creator は URI 文字列、dcterms:creator は {"@id": URI} で入る
    for v in _plains(node.get("creator")):
        if v.startswith("http"):
            return _id_suffix(v)
    for v in _as_list(node.get("dcterms:creator")):
        if isinstance(v, dict) and "@id" in v:
            return _id_suffix(v["@id"])
    return None


def _creator_statement(node: dict) -> str | None:
    # 責任表示（例 "[著]桂正和"）。schema:creator を優先し、
    # 無ければ creator に混在するプレーン文字列（URI を除く）を使う
    statements = _plains(node.get("schema:creator"))
    if not statements:
        statements = [v for v in _plains(node.get("creator")) if not v.startswith("http")]
    return _join(statements)


_PUBLISHER_CODE = re.compile(r"P\d+(?:,P\d+)*")
_TRANSIENT_HTTP_STATUS = {429, 500, 502, 503, 504}


def _publisher(node: dict) -> tuple[str | None, str | None, str | None]:
    """出版者の名称・読み・コードを取り出す。

    publisher / schema:publisher には「名称 ∥ 読み」（コンマ区切りで複数値）と
    出版者コード（P4080000000 等）がレコードにより入れ替わって入るため、
    両フィールドを走査してコードと名称を仕分ける。
    例: "集英社　∥　シュウエイシャ" / "ひばり書房　∥　ヒバリ ショボウ,株式会社ひばり書房"
    """
    values = _plains(node.get("publisher")) + _plains(node.get("schema:publisher"))
    codes = [v for v in values if _PUBLISHER_CODE.fullmatch(v)]

    names: list[str] = []
    kanas: list[str] = []
    for value in values:
        if _PUBLISHER_CODE.fullmatch(value):
            continue
        for element in value.split(","):
            parts = [p.strip(" 　") for p in element.split("∥")]
            if parts[0] and parts[0] not in names:
                names.append(parts[0])
            if len(parts) > 1 and parts[1] and parts[1] not in kanas:
                kanas.append(parts[1])

    code = node.get("dcterms:publisher") or (codes[0] if codes else None)
    return _join(names), _join(kanas), code


def _series_id(node: dict) -> str | None:
    value = node.get("isPartOf")
    if isinstance(value, str) and value.startswith("http"):
        return _id_suffix(value)
    return None


def flatten(node: dict) -> dict:
    """class:MangaBook ノードを 1 レコードへ平坦化する。"""
    publisher_name, publisher_name_kana, publisher_code = _publisher(node)
    return {
        "book_id": node.get("identifier"),
        "title": _join(_plains(node.get("name"))) or node.get("label"),
        "title_kana": _kana(node.get("name")),
        "alternate_title": _join(_plains(node.get("alternateName"))),
        "volume": node.get("volumeNumber"),
        "volume_sort": node.get("position"),
        "series_id": _series_id(node),
        "series_name": _join(_plains(node.get("seriesName"))),
        "creator_id": _creator_id(node),
        "creator_statement": _creator_statement(node),
        "publisher_name": publisher_name,
        "publisher_name_kana": publisher_name_kana,
        "publisher_code": publisher_code,
        "brand": _join(_plains(node.get("brand"))),
        "brand_kana": _kana(node.get("brand")),
        "date_published": node.get("datePublished"),
        "publication_place": node.get("location"),
        "language": node.get("inLanguage"),
        "isbn": node.get("isbn"),
        "jpno": node.get("jpno"),
        "ndc": node.get("ndc"),
        "product_id": node.get("productID"),
        "pages": node.get("numberOfPages"),
        "book_size": node.get("size"),
        "price": node.get("price"),
        "note": node.get("note"),
    }


def _download_zip(url: str, *, max_attempts: int = 5) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "dataset-mediaarts-db/0.1"},
    )

    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=120) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code not in _TRANSIENT_HTTP_STATUS or attempt == max_attempts:
                raise
            retry_after = e.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                delay = int(retry_after)
            else:
                delay = min(60, 2 ** attempt)
        except urllib.error.URLError:
            if attempt == max_attempts:
                raise
            delay = min(60, 2 ** attempt)

        time.sleep(delay)

    raise RuntimeError("unreachable")


def download_and_flatten(ndjson_path: Path) -> int:
    """cm101 zip を取得し、平坦化した NDJSON を書き出す。行数を返す。"""
    payload = _download_zip(ZIP_URL)

    rows = 0
    with (
        zipfile.ZipFile(io.BytesIO(payload)) as archive,
        ndjson_path.open("w", encoding="utf-8") as out,
    ):
        for member in sorted(archive.namelist()):
            with archive.open(member) as f:
                graph = json.load(f)["@graph"]
            for node in graph:
                if node.get("@type") != "class:MangaBook":
                    continue
                record = flatten(node)
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                rows += 1
    return rows
