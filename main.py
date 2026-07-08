"""メディア芸術データベース（MADB）の取得 + dbt ビルド。

1. madb: 公式データセットリポジトリからマンガ単行本（cm101）の JSON-LD を取得し、
         平坦化した NDJSON へ整形する。
2. dbt:  dbt ビルド。
"""

import logging
from pathlib import Path

from dbt.cli.main import dbtRunner

from madb import download_and_flatten

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")

FDL_DIR = Path(".fdl")
NDJSON_PATH = FDL_DIR / "madb_manga_book.ndjson"


def dbt_build() -> None:
    dbt = dbtRunner()
    for cmd in (["deps"], ["run"], ["docs", "generate"]):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {cmd[0]} failed")


def main() -> None:
    FDL_DIR.mkdir(exist_ok=True)

    logger.info("1/2: madb (マンガ単行本 cm101)")
    rows = download_and_flatten(NDJSON_PATH)
    logger.info(f"  madb_manga_book.ndjson: {rows} rows")

    logger.info("2/2: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
