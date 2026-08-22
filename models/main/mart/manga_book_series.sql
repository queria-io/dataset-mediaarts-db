{# マンガ単行本シリーズの書誌データ。メディア芸術データベース（MADB）の詳細ページ URL を付与する。 #}

{{ config(materialized='table') }}

select
    series_id,
    title,
    title_kana,
    alternate_title,
    series_name,
    version,
    creator_id,
    creator_statement,
    contributor,
    original_work_creator,
    publisher_name,
    publisher_name_kana,
    publisher_code,
    brand,
    brand_kana,
    date_published,
    published_year,
    date_published_final,
    final_published_year,
    volume_count,
    ndc,
    content_rating,
    additional_genre,
    language,
    publication_place,
    description,
    note,
    'https://mediaarts-db.artmuseums.go.jp/id/' || series_id as source_url
from {{ ref('stg_manga_book_series') }}
