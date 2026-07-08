{# メディア芸術データベース マンガ単行本（cm101）の生データ。
   main.py が公式データセットリポジトリの JSON-LD を平坦化して
   .fdl/madb_manga_book.ndjson に保存する。型変換は stg で行うため全列 VARCHAR で読む。 #}

{{ config(materialized='table') }}

select *
from read_json(
    '.fdl/madb_manga_book.ndjson',
    format='newline_delimited',
    columns={
        'book_id': 'VARCHAR',
        'title': 'VARCHAR',
        'title_kana': 'VARCHAR',
        'alternate_title': 'VARCHAR',
        'volume': 'VARCHAR',
        'volume_sort': 'VARCHAR',
        'series_id': 'VARCHAR',
        'series_name': 'VARCHAR',
        'creator_id': 'VARCHAR',
        'creator_statement': 'VARCHAR',
        'publisher_name': 'VARCHAR',
        'publisher_name_kana': 'VARCHAR',
        'publisher_code': 'VARCHAR',
        'brand': 'VARCHAR',
        'brand_kana': 'VARCHAR',
        'date_published': 'VARCHAR',
        'publication_place': 'VARCHAR',
        'language': 'VARCHAR',
        'isbn': 'VARCHAR',
        'jpno': 'VARCHAR',
        'ndc': 'VARCHAR',
        'product_id': 'VARCHAR',
        'pages': 'VARCHAR',
        'book_size': 'VARCHAR',
        'price': 'VARCHAR',
        'note': 'VARCHAR'
    }
)
