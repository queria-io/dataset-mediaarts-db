{# 表示年月日と全巻数を数値へ、出版日から出版年を導出する。
   date_published は YYYY / YYYY-MM / YYYY-MM-DD が混在するため文字列のまま保持する。
   巻・号・通巻は "3・4"（合併号）や "Vol.1" のような表記が混じるため文字列のまま扱う。 #}

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
    try_cast(year_displayed as INTEGER) as year_displayed,
    try_cast(month_displayed as INTEGER) as month_displayed,
    try_cast(day_displayed as INTEGER) as day_displayed,
    date_published,
    case
        when regexp_matches(date_published, '^\d{4}')
        then substr(date_published, 1, 4)::INTEGER
    end as published_year,
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
    note
from {{ ref('raw_manga_magazine_issue') }}
