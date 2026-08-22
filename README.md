# dataset-mediaarts-db

## データ出典

[メディア芸術データベース（MADB）](https://mediaarts-db.artmuseums.go.jp/)のデータセットです。
メディア芸術データベースは独立行政法人国立美術館 国立アートリサーチセンター（旧 文化庁）が運営する
マンガ・アニメ・ゲーム・メディアアートの所蔵・書誌情報データベースで、そのメタデータは
[公式データセットリポジトリ](https://github.com/mediaarts-db/dataset)で機械可読形式（JSON-LD / Turtle）
として公開されています。

本データセットは現在、マンガ単行本（情報資源分類 cm101）・マンガ単行本シリーズ（cm104）・
マンガ雑誌各号（cm102）の書誌情報を収録します。アニメ・ゲーム等の他分野は将来の拡張余地です。

## テーブル: manga_book

マンガ単行本の書誌データです。日本国内で刊行されたマンガ単行本を1冊1レコードで収録し、
タイトル・巻数・著者・出版者・レーベル・ISBN・出版年月・ページ数などを持ちます。

- book_id: 単行本ID（VARCHAR、メディア芸術データベースの資料識別子。例 M189456。主キー）
- title: タイトル（VARCHAR）
- title_kana: タイトルヨミ（VARCHAR、ひらがな・カタカナ表記の読み）
- alternate_title: 別タイトル（VARCHAR）
- volume: 巻表示（VARCHAR、表示上の巻数・巻次）
- volume_sort: 巻の並び順（DOUBLE、シリーズ内の並び替え用数値）
- series_id: シリーズID（VARCHAR、所属するマンガ単行本シリーズ cm104 の識別子。例 C268475。manga_book_series と結合できる）
- series_name: シリーズ名（VARCHAR）
- creator_id: 著者ID（VARCHAR、メディア芸術データベースの著者識別子。例 C57152。複数の著者は " | " で連結）
- creator_statement: 著者表示（VARCHAR、責任表示。例 "[著]桂正和"）
- publisher_name: 出版者（VARCHAR）
- publisher_name_kana: 出版者ヨミ（VARCHAR）
- publisher_code: 出版者コード（VARCHAR、メディア芸術データベースの出版者識別子）
- brand: レーベル（VARCHAR、叢書・レーベル名）
- brand_kana: レーベルヨミ（VARCHAR）
- date_published: 出版年月（VARCHAR、YYYY / YYYY-MM / YYYY-MM-DD が混在）
- published_year: 出版年（INTEGER、date_published から導出）
- publication_place: 出版地（VARCHAR）
- language: 言語（VARCHAR）
- isbn: ISBN（VARCHAR）
- jpno: 全国書誌番号（VARCHAR、国立国会図書館の JP 番号）
- ndc: NDC分類（VARCHAR、日本十進分類法の分類記号）
- product_id: 商品コード（VARCHAR）
- pages: ページ数（VARCHAR、表示形式のまま保持。例 "234p"）
- book_size: 判型（VARCHAR、大きさ。例 "19cm"）
- price: 価格（VARCHAR）
- note: 注記（VARCHAR）
- source_url: 詳細ページURL（VARCHAR、メディア芸術データベースの資料詳細ページ）

## テーブル: manga_book_series

マンガ単行本シリーズの書誌データです。単行本をまとめるシリーズを1レコードで収録し、
タイトル・著者・出版者・レーベル・全巻数・初刊と最終巻の発行日などを持ちます。
manga_book.series_id と結合できます。

- series_id: シリーズID（VARCHAR、メディア芸術データベースの資料識別子。例 C253219。主キー）
- title: タイトル（VARCHAR）
- title_kana: タイトルヨミ（VARCHAR）
- alternate_title: 別タイトル（VARCHAR）
- series_name: シリーズ名（VARCHAR、このシリーズが所属する上位シリーズ）
- version: 版表示（VARCHAR、例 "コミック版"）
- creator_id: 著者ID（VARCHAR、複数の著者は " | " で連結）
- creator_statement: 著者表示（VARCHAR、責任表示。例 "[著]尾玉なみえ"）
- contributor: その他の著者（VARCHAR）
- original_work_creator: 原作者（VARCHAR）
- publisher_name: 発行者名（VARCHAR）
- publisher_name_kana: 発行者名ヨミ（VARCHAR）
- publisher_code: 発行者コード（VARCHAR）
- brand: レーベル（VARCHAR、例 "シリウスKC"）
- brand_kana: レーベルヨミ（VARCHAR）
- date_published: 出版日（VARCHAR、初刊。YYYY / YYYY-MM / YYYY-MM-DD が混在）
- published_year: 出版年（INTEGER、date_published から導出）
- date_published_final: 最終巻発行日（VARCHAR、終刊したシリーズの最新巻。原典の YYYYMMDD 詰めを date_published と同じ表記へ揃え、不明な桁は落とす）
- final_published_year: 最終巻発行年（INTEGER）
- volume_count: 全巻数（INTEGER、シリーズを構成する単行本の件数）
- ndc: NDC分類（VARCHAR）
- content_rating: レーティング（VARCHAR、例 "成年コミック"）
- additional_genre: サブジャンル（VARCHAR、例 "短編集"）
- language: 言語（VARCHAR）
- publication_place: 発行地（VARCHAR）
- description: 概要（VARCHAR）
- note: 備考（VARCHAR）
- source_url: 詳細ページURL（VARCHAR）

## テーブル: manga_magazine_issue

マンガ雑誌各号の書誌データです。日本国内で刊行されたマンガ雑誌を1号1レコードで収録し、
雑誌名・巻号・通巻・発行日・発行者・編集人・ページ数・価格などを持ちます。

- issue_id: 各号ID（VARCHAR、メディア芸術データベースの資料識別子。例 M533115。主キー）
- magazine_id: マンガ雑誌ID（VARCHAR、号がまとまる雑誌 cm105 の識別子。例 C119009）
- magazine_name: 雑誌名（VARCHAR）
- magazine_name_kana: 雑誌名ヨミ（VARCHAR）
- issue_label: 各号の表示名（VARCHAR、例 "マーガレット 2004年 表示号数17"）
- alternate_title: 別タイトル（VARCHAR）
- volume_number: 巻（VARCHAR）
- issue_number: 号（VARCHAR）
- issue_number_displayed: 表示号数（VARCHAR、表紙などに表示される号。巻次とは区別される）
- sub_issue_number: 補助号数（VARCHAR、数値以外での順序の記述。例 "9月1日号増刊"）
- total_volume_number: 通巻（VARCHAR）
- combined_issue: 合併（VARCHAR、合併号のとき "合併"）
- issue_number_displayed_combined: 表示合併号数（VARCHAR）
- year_displayed: 表示年（INTEGER、表紙などに表示される年）
- month_displayed: 表示月（INTEGER）
- day_displayed: 表示日（INTEGER）
- date_published: 出版日（VARCHAR、YYYY / YYYY-MM / YYYY-MM-DD が混在）
- published_year: 出版年（INTEGER、date_published から導出）
- date_released: 発売年月日（VARCHAR、奥付等に表示される発売日）
- publisher_name: 発行者名（VARCHAR）
- publisher_name_kana: 発行者名ヨミ（VARCHAR）
- publisher_code: 発行者コード（VARCHAR）
- publisher_person: 発行人（VARCHAR、発行の責任者である個人）
- editor: 編集人（VARCHAR、編集人である個人）
- pages: ページ数（VARCHAR、表示形式のまま保持。例 "440p"）
- book_size: 大きさ（VARCHAR、判型。例 "26cm"）
- price: 価格（VARCHAR）
- ndc: NDC分類（VARCHAR）
- content_rating: レーティング（VARCHAR、例 "成年向け雑誌"）
- note: 備考（VARCHAR）
- source_url: 詳細ページURL（VARCHAR）

## 加工の方針

原典の JSON-LD は値が文字列・言語タグ付き値・その配列で混在するため、プレーン文字列と
読み（ja-hrkt）の分離、リソース URI からの ID 抽出、出版者の名称・読み・コードの仕分けを
行ったうえで列に平坦化しています。複数値は " | " で連結しています。日付は原典の表記を
そのまま保持し、年の列と最終巻発行日の表記揃えだけを導出しています。書誌の値そのものは
改変していません。

### データ更新手順

main.py が公式データセットリポジトリからマンガ単行本（cm101）・マンガ単行本シリーズ（cm104）・
マンガ雑誌各号（cm102）の JSON-LD zip を取得して平坦化した NDJSON へ整形し、
dbt build で書誌テーブルを再生成する。
ビルドは `bash scripts/build.sh` で実行する（Queria に公開する）。

## ライセンス

[メディア芸術データベースデータセット](https://github.com/mediaarts-db/dataset)の利用条件
（自由な二次利用可）に従う。

出典: 「メディア芸術データベースデータセット」（独立行政法人国立美術館 国立アートリサーチセンター）
（https://github.com/mediaarts-db/dataset）を加工して作成。

JSON-LD の書誌メタデータを表形式へ平坦化する加工を行っている。書誌の値そのものは改変していない。
