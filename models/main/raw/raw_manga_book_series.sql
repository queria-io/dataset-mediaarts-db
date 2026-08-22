{# メディア芸術データベース マンガ単行本シリーズ（cm104）の生データ。
   main.py が公式データセットリポジトリの JSON-LD を平坦化して
   .queria/madb_manga_book_series.ndjson に保存する。型変換は stg で行うため全列 VARCHAR で読む。 #}

{{ config(materialized='table') }}

select *
from read_json(
    '.queria/madb_manga_book_series.ndjson',
    format='newline_delimited',
    columns={
        'series_id': 'VARCHAR',
        'title': 'VARCHAR',
        'title_kana': 'VARCHAR',
        'alternate_title': 'VARCHAR',
        'series_name': 'VARCHAR',
        'version': 'VARCHAR',
        'creator_id': 'VARCHAR',
        'creator_statement': 'VARCHAR',
        'contributor': 'VARCHAR',
        'original_work_creator': 'VARCHAR',
        'publisher_name': 'VARCHAR',
        'publisher_name_kana': 'VARCHAR',
        'publisher_code': 'VARCHAR',
        'brand': 'VARCHAR',
        'brand_kana': 'VARCHAR',
        'date_published': 'VARCHAR',
        'date_published_final': 'VARCHAR',
        'volume_count': 'VARCHAR',
        'ndc': 'VARCHAR',
        'content_rating': 'VARCHAR',
        'additional_genre': 'VARCHAR',
        'language': 'VARCHAR',
        'publication_place': 'VARCHAR',
        'description': 'VARCHAR',
        'note': 'VARCHAR'
    }
)
