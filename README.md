## OfuroNotify

お風呂の時間を計るためのAWS Lambda Functionです。
dynamodbにデータを保存します。dynamodbのcreate table権限があれば自動的にテーブルを作成します。

# TODO

* loggerを使うようにする
* webhook実装

# 外部仕様

* 設定は環境変数から取得します。
* exec.sh-sampleを参照して下さい。

# 内部仕様

## dynamodb

### OfuroHistories

履歴テーブル

### LastOfuro

最新の（最後に書き込んだ）データのみの複製を持つテーブル