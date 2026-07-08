{# 巻の並び順を数値へ、出版年月から出版年を導出する。
   date_published は YYYY / YYYY-MM / YYYY-MM-DD が混在するため文字列のまま保持する。 #}

select
    book_id,
    title,
    title_kana,
    alternate_title,
    volume,
    try_cast(volume_sort as DOUBLE) as volume_sort,
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
    case
        when regexp_matches(date_published, '^\d{4}')
        then substr(date_published, 1, 4)::INTEGER
    end as published_year,
    publication_place,
    language,
    isbn,
    jpno,
    ndc,
    product_id,
    pages,
    book_size,
    price,
    note
from {{ ref('raw_manga_book') }}
