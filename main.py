"""メディア芸術データベース（MADB）の取得 + dbt ビルド。

1. madb: 公式データセットリポジトリからマンガの書誌 JSON-LD を取得し、
         分類ごとに平坦化した NDJSON へ整形する。
2. dbt:  dbt ビルド。
"""

import logging
from pathlib import Path

from dbt.cli.main import dbtRunner

from madb import SOURCES, download_and_flatten

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pipelines")

WORK_DIR = Path(".queria")


def ndjson_path(name: str) -> Path:
    return WORK_DIR / f"madb_{name}.ndjson"


def dbt_build() -> None:
    dbt = dbtRunner()
    for cmd in (["deps"], ["run"], ["docs", "generate"]):
        result = dbt.invoke(cmd)
        if not result.success:
            raise SystemExit(f"dbt {cmd[0]} failed")


def main() -> None:
    WORK_DIR.mkdir(exist_ok=True)

    logger.info("1/2: madb")
    for name, source in SOURCES.items():
        path = ndjson_path(name)
        rows = download_and_flatten(source, path)
        logger.info(f"  {path.name}: {rows} rows")

    logger.info("2/2: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
