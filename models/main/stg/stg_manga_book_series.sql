{# 全巻数を数値へ、出版日から出版年を導出する。
   date_published は YYYY / YYYY-MM / YYYY-MM-DD が混在するため文字列のまま保持する。
   date_published_final は YYYYMMDD 詰め（年だけ・年月だけの値も混じる）で、不明な桁は
   0 埋め、日付そのものが不明なシリーズは 0 の並びで入る。date_published と同じ表記へ揃え、
   不明な桁は落とし、年が 0 のものは NULL にする。 #}

with parts as (
    select
        *,
        substr(date_published_final, 1, 4) as final_year,
        substr(date_published_final, 5, 2) as final_month,
        substr(date_published_final, 7, 2) as final_day
    from {{ ref('raw_manga_book_series') }}
),

normalized as (
    select
        *,
        case
            when final_year is null or final_year = '0000' or length(final_year) < 4 then null
            when final_month in ('', '00') then final_year
            when final_day in ('', '00') then final_year || '-' || final_month
            else final_year || '-' || final_month || '-' || final_day
        end as date_published_final_normalized
    from parts
)

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
    case
        when regexp_matches(date_published, '^\d{4}')
        then substr(date_published, 1, 4)::INTEGER
    end as published_year,
    date_published_final_normalized as date_published_final,
    case
        when regexp_matches(date_published_final_normalized, '^\d{4}')
        then substr(date_published_final_normalized, 1, 4)::INTEGER
    end as final_published_year,
    try_cast(volume_count as INTEGER) as volume_count,
    ndc,
    content_rating,
    additional_genre,
    language,
    publication_place,
    description,
    note
from normalized
