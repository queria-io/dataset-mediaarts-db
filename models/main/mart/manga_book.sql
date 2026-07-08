{# マンガ単行本の書誌データ。メディア芸術データベース（MADB）の詳細ページ URL を付与する。 #}

{{ config(materialized='table') }}

select
    book_id,
    title,
    title_kana,
    alternate_title,
    volume,
    volume_sort,
    series_id,
    series_name,
    creator_id,
    creator_statement,
    publisher_name,
    publisher_name_kana,
    publisher_code,
    brand,
    brand_kana,
    date_published,
    published_year,
    publication_place,
    language,
    isbn,
    jpno,
    ndc,
    product_id,
    pages,
    book_size,
    price,
    note,
    'https://mediaarts-db.artmuseums.go.jp/id/' || book_id as source_url
from {{ ref('stg_manga_book') }}
