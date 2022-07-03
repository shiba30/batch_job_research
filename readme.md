# 求人情報スクレイピングバッチ【job_research】

"job_research"(以下、本バッチ)は、[パーソル テクノロジースタッフの求人サイト]("https://persol-tech-s.co.jp/jobsearch/result/")から、下記の項目を取得する

* 題名
* 職種
* 給与
* 勤務地
* 勤務時間

取得した結果をCSVファイル(job_research/csv/result.csv)に出力する

# Features

本バッチは、Seleniumライブラリを使用して、XPathにて要素を取得している

# Requirement

本バッチを動かすのに必要なライブラリなどを列挙する

* PyMySQL 1.0.2
* selenium 4.3.0


# Installation

Requirementで列挙したライブラリなどのインストール方法

```
pip install -r requirements/requirements.txt
```

# Directory structure

以下、ディレクトリ構成

```
job_research/
    ├ config/
    |    └ config.ini (DB接続情報ファイル)
    ├ db/
    |   ├ sql/
    |   |   ├ create_db.sql (テーブル作成SQL)
    |   |   ├ insert.sql (求人情報登録SQL)
    |   |   └ select.sql (求人情報取得SQL)
    |   └ db_utils.py (DB操作クラス)
    ├ csv/
    |   └ result.csv (取得結果csv)
    ├ product/
    |   └ get_job_opportunities.py (求人情報スクレイピングバッチ)
    ├ requirements/
    |   ├ development.txt
    |   └ requirements.txt
    ├ chromedriver
    └ readme.md
```

# Task

アドバンスド：
    作りが違う各社のホームページから基本データ（代表名、電話番号、メールアドレス）を抽出するにはどの様な方法が考えられるか（方法を考え、Readmeに記載するだけで良いです）

1. XPathのcontainsを使用して、"会社概要" or "COMPANY" などの文字列が含まれているページに遷移する
2. 会社の基本情報が書かれたページで、"代表" "取締役" "電話番号TEL(正規表現で検索するのもあり)" などの文字列で検索して取得する