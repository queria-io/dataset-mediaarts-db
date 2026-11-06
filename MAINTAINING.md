# 運用メモ

## データ更新手順

main.py が公式データセットリポジトリからマンガ単行本（cm101）・マンガ単行本シリーズ（cm104）・
マンガ雑誌各号（cm102）の JSON-LD zip を取得して平坦化した NDJSON へ整形し、
dbt build で書誌テーブルを再生成する。
ビルドは `bash scripts/build.sh` で実行する（Queria に公開する）。

