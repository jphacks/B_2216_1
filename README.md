# B_2216's API server

## 概要

B2216班(ええいっく)のバックエンドAPIサーバーです。
機能としては、次のようなものがあります

- イスデバイスからのデータを受信し、DBに格納する
- アプリからの要求に対してデータを要求に沿った形に加工し、送信する
  - 日、週、月単位で体重データの平均を取り、時系列データとして送信
  - 同様の時間間隔で座っていた時間の合計を計算し送信


## How to run server

1. Set the sqlite database file path to `DATABASE_URI` variable in `.env` file. For example, `DATABASE_URI="sqlite:///./app.db"`.
2. Run the following command:
   1. Using Docker (recommended):
      ```sh
      docker compose up -d
      ```
   2. Native (option):
      ```sh
      pip install -r requirements.txt
      uvicorn uvicorn src.main:app --reload
      ```

## frontend URL
https://github.com/jphacks/B_2216