"""メディア芸術データベース（MADB）データセットの取得・展開。

公式データセットリポジトリ（github.com/mediaarts-db/dataset）から
情報資源分類ごとの JSON-LD zip を取得し、対象クラスのノードを
スカラー列に平坦化した NDJSON へ変換する。

JSON-LD の値は文字列・言語タグ付き dict・それらの list が混在するため、
平坦化（プレーン文字列と ja-hrkt 読みの分離、URI からの ID 抽出）は
SQL ではなくここで行い、dbt には列が確定した NDJSON を渡す。
"""

import io
import json
import re
import urllib.request
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/mediaarts-db/dataset/main/data/json-ld/"

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
    """リソース URI 末尾の ID（M189456 / C57152 等）を取り出す。

    複数の URI がコンマで連結された値（著者が複数のレコード）も分解する。
    """
    return _JOIN.join(u.rstrip("/").rsplit("/", 1)[-1] for u in uri.split(",") if u)


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


def _part_of_id(node: dict) -> str | None:
    """上位コレクション（シリーズ・雑誌）の ID。"""
    value = node.get("isPartOf")
    if isinstance(value, str) and value.startswith("http"):
        return _id_suffix(value)
    return None


def flatten_manga_book(node: dict) -> dict:
    """class:MangaBook（マンガ単行本 cm101）を 1 レコードへ平坦化する。"""
    publisher_name, publisher_name_kana, publisher_code = _publisher(node)
    return {
        "book_id": node.get("identifier"),
        "title": _join(_plains(node.get("name"))) or node.get("label"),
        "title_kana": _kana(node.get("name")),
        "alternate_title": _join(_plains(node.get("alternateName"))),
        "volume": node.get("volumeNumber"),
        "volume_sort": node.get("position"),
        "series_id": _part_of_id(node),
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


def flatten_manga_magazine_issue(node: dict) -> dict:
    """class:MangaMagazineIssue（マンガ雑誌各号 cm102）を 1 レコードへ平坦化する。"""
    publisher_name, publisher_name_kana, publisher_code = _publisher(node)
    return {
        "issue_id": node.get("identifier"),
        "magazine_id": _part_of_id(node),
        "magazine_name": _join(_plains(node.get("name"))) or node.get("label"),
        "magazine_name_kana": _kana(node.get("name")),
        "issue_label": node.get("label"),
        "alternate_title": _join(_plains(node.get("alternateName"))),
        "volume_number": node.get("volumeNumber"),
        "issue_number": node.get("issueNumber"),
        "issue_number_displayed": node.get("issueNumberDisplayed"),
        "sub_issue_number": node.get("subIssueNumber"),
        "total_volume_number": node.get("totalVolumeNumber"),
        "combined_issue": node.get("combinedIssue"),
        "issue_number_displayed_combined": node.get("issueNumberDisplayedCombined"),
        "year_displayed": node.get("yearDisplayed"),
        "month_displayed": node.get("monthDisplayed"),
        "day_displayed": node.get("dayDisplayed"),
        "date_published": node.get("datePublished"),
        "date_released": node.get("dateReleased"),
        "publisher_name": publisher_name,
        "publisher_name_kana": publisher_name_kana,
        "publisher_code": publisher_code,
        "publisher_person": node.get("ma:publisher"),
        "editor": node.get("editor"),
        "pages": node.get("numberOfPages"),
        "book_size": node.get("size"),
        "price": node.get("price"),
        "ndc": node.get("ndc"),
        "content_rating": node.get("contentRating"),
        "note": node.get("note"),
    }


def flatten_manga_book_series(node: dict) -> dict:
    """class:MangaBookSeries（マンガ単行本シリーズ cm104）を 1 レコードへ平坦化する。"""
    publisher_name, publisher_name_kana, publisher_code = _publisher(node)
    return {
        "series_id": node.get("identifier"),
        "title": _join(_plains(node.get("name"))) or node.get("label"),
        "title_kana": _kana(node.get("name")),
        "alternate_title": _join(_plains(node.get("alternateName"))),
        "series_name": _join(_plains(node.get("seriesName"))),
        "version": node.get("version"),
        "creator_id": _creator_id(node),
        "creator_statement": _creator_statement(node),
        "contributor": _join(_plains(node.get("contributor"))),
        "original_work_creator": _join(_plains(node.get("originalWorkCreator"))),
        "publisher_name": publisher_name,
        "publisher_name_kana": publisher_name_kana,
        "publisher_code": publisher_code,
        "brand": _join(_plains(node.get("brand"))),
        "brand_kana": _kana(node.get("brand")),
        "date_published": node.get("datePublished"),
        "date_published_final": node.get("datePublishedFinal"),
        "volume_count": node.get("numberOfItems"),
        "ndc": node.get("ndc"),
        "content_rating": node.get("contentRating"),
        "additional_genre": node.get("additionalGenre"),
        "language": node.get("inLanguage"),
        "publication_place": node.get("location"),
        "description": node.get("description"),
        "note": node.get("note"),
    }


@dataclass(frozen=True)
class Source:
    """情報資源分類ごとの取得元と平坦化。"""

    zip_name: str
    node_type: str
    flatten: Callable[[dict], dict]

    @property
    def url(self) -> str:
        return BASE_URL + self.zip_name


SOURCES = {
    "manga_book": Source(
        "metadata_cm-item_cm101_json.zip", "class:MangaBook", flatten_manga_book
    ),
    "manga_magazine_issue": Source(
        "metadata_cm-item_cm102_json.zip",
        "class:MangaMagazineIssue",
        flatten_manga_magazine_issue,
    ),
    "manga_book_series": Source(
        "metadata_cm-col_cm104_json.zip",
        "class:MangaBookSeries",
        flatten_manga_book_series,
    ),
}


def download_and_flatten(source: Source, ndjson_path: Path) -> int:
    """zip を取得し、平坦化した NDJSON を書き出す。行数を返す。

    zip には対象クラス以外のノード（所蔵情報や掲載作品の空白ノード）も入るため、
    @type で絞り込む。
    """
    with urllib.request.urlopen(source.url) as resp:
        payload = resp.read()

    rows = 0
    with (
        zipfile.ZipFile(io.BytesIO(payload)) as archive,
        ndjson_path.open("w", encoding="utf-8") as out,
    ):
        for member in sorted(archive.namelist()):
            with archive.open(member) as f:
                graph = json.load(f)["@graph"]
            for node in graph:
                if node.get("@type") != source.node_type:
                    continue
                record = source.flatten(node)
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                rows += 1
    return rows
