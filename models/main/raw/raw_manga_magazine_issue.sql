{# メディア芸術データベース マンガ雑誌各号（cm102）の生データ。
   main.py が公式データセットリポジトリの JSON-LD を平坦化して
   .queria/madb_manga_magazine_issue.ndjson に保存する。型変換は stg で行うため全列 VARCHAR で読む。 #}

{{ config(materialized='table') }}

select *
from read_json(
    '.queria/madb_manga_magazine_issue.ndjson',
    format='newline_delimited',
    columns={
        'issue_id': 'VARCHAR',
        'magazine_id': 'VARCHAR',
        'magazine_name': 'VARCHAR',
        'magazine_name_kana': 'VARCHAR',
        'issue_label': 'VARCHAR',
        'alternate_title': 'VARCHAR',
        'volume_number': 'VARCHAR',
        'issue_number': 'VARCHAR',
        'issue_number_displayed': 'VARCHAR',
        'sub_issue_number': 'VARCHAR',
        'total_volume_number': 'VARCHAR',
        'combined_issue': 'VARCHAR',
        'issue_number_displayed_combined': 'VARCHAR',
        'year_displayed': 'VARCHAR',
        'month_displayed': 'VARCHAR',
        'day_displayed': 'VARCHAR',
        'date_published': 'VARCHAR',
        'date_released': 'VARCHAR',
        'publisher_name': 'VARCHAR',
        'publisher_name_kana': 'VARCHAR',
        'publisher_code': 'VARCHAR',
        'publisher_person': 'VARCHAR',
        'editor': 'VARCHAR',
        'pages': 'VARCHAR',
        'book_size': 'VARCHAR',
        'price': 'VARCHAR',
        'ndc': 'VARCHAR',
        'content_rating': 'VARCHAR',
        'note': 'VARCHAR'
    }
)
