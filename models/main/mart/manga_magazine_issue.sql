{# マンガ雑誌各号の書誌データ。メディア芸術データベース（MADB）の詳細ページ URL を付与する。 #}

{{ config(materialized='table') }}

select
    issue_id,
    magazine_id,
    magazine_name,
    magazine_name_kana,
    issue_label,
    alternate_title,
    volume_number,
    issue_number,
    issue_number_displayed,
    sub_issue_number,
    total_volume_number,
    combined_issue,
    issue_number_displayed_combined,
    year_displayed,
    month_displayed,
    day_displayed,
    date_published,
    published_year,
    date_released,
    publisher_name,
    publisher_name_kana,
    publisher_code,
    publisher_person,
    editor,
    pages,
    book_size,
    price,
    ndc,
    content_rating,
    note,
    'https://mediaarts-db.artmuseums.go.jp/id/' || issue_id as source_url
from {{ ref('stg_manga_magazine_issue') }}
