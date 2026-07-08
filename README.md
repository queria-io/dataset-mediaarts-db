# dataset-mediaarts-db

## データ出典

[メディア芸術データベース（MADB）](https://mediaarts-db.artmuseums.go.jp/)のデータセットです。
メディア芸術データベースは独立行政法人国立美術館 国立アートリサーチセンター（旧 文化庁）が運営する
マンガ・アニメ・ゲーム・メディアアートの所蔵・書誌情報データベースで、そのメタデータは
[公式データセットリポジトリ](https://github.com/mediaarts-db/dataset)で機械可読形式（JSON-LD / Turtle）
として公開されています。

本データセットは現在、マンガ単行本（情報資源分類 cm101）の書誌情報を収録します。
マンガ雑誌・アニメ・ゲーム等の他分類は将来の拡張余地です。

## テーブル: manga_book

マンガ単行本の書誌データです。日本国内で刊行されたマンガ単行本を1冊1レコードで収録し、
タイトル・巻数・著者・出版者・レーベル・ISBN・出版年月・ページ数などを持ちます。

- book_id: 単行本ID（VARCHAR、メディア芸術データベースの資料識別子。例 M189456。主キー）
- title: タイトル（VARCHAR）
- title_kana: タイトルヨミ（VARCHAR、ひらがな・カタカナ表記の読み）
- alternate_title: 別タイトル（VARCHAR）
- volume: 巻表示（VARCHAR、表示上の巻数・巻次）
- volume_sort: 巻の並び順（DOUBLE、シリーズ内の並び替え用数値）
- series_id: シリーズID（VARCHAR、所属するマンガ単行本シリーズ cm104 の識別子。例 C268475）
- series_name: シリーズ名（VARCHAR）
- creator_id: 著者ID（VARCHAR、メディア芸術データベースの著者識別子。例 C57152）
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

原典の JSON-LD は値が文字列・言語タグ付き値・その配列で混在するため、プレーン文字列と
読み（ja-hrkt）の分離、リソース URI からの ID 抽出、出版者の名称・読み・コードの仕分けを
行ったうえで列に平坦化しています。複数値は " | " で連結しています。書誌の値そのものは
改変していません。

### データ更新手順

main.py が公式データセットリポジトリからマンガ単行本（cm101）の JSON-LD zip を取得して
平坦化した NDJSON へ整形し、dbt build で書誌テーブルを再生成する。
ビルドは `bash scripts/build.sh local` で実行する。

## ライセンス

[メディア芸術データベースデータセット](https://github.com/mediaarts-db/dataset)の利用条件
（自由な二次利用可）に従う。

出典: 「メディア芸術データベースデータセット」（独立行政法人国立美術館 国立アートリサーチセンター）
（https://github.com/mediaarts-db/dataset）を加工して作成。

JSON-LD の書誌メタデータを表形式へ平坦化する加工を行っている。書誌の値そのものは改変していない。
