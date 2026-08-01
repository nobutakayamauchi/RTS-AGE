# 手動テスト計画

## テスト原則

- 本番公開前は架空データだけを使う
- 実在する第三者の連絡先を無断で使わない
- 最初のメール送信は自分の検証用アドレス1件だけ
- LINE/Xは自分の検証用アカウントから利用者発の連絡として試す
- 各テスト後に `Leads`、`Deliveries`、`Audit` を確認

## T01 初期セットアップ

**操作**

1. 空のSheetsへコードを配置
2. `Limit Lead Hub → 初期セットアップ`

**期待**

- 4シートが作成される
- ヘッダーが固定される
- Config初期値が入る
- Script PropertiesへSpreadsheet IDが入る
- Auditへ `SETUP_COMPLETED`

## T02 設定不足を検出

**操作**

初期値のまま `Limit Lead Hub → 設定を検証`

**期待**

- `ok = false`
- `KIT_URL`未変更が問題として返る

## T03 メールのみ

**入力**

- メール選択
- 自分の検証用メール
- delivery同意true
- updates/offers false

**期待**

- lead ID発行
- Leadsに1行
- Deliveriesにemail/PENDING
- キュー処理後にSENT
- メールに版、受取リンク、受付番号、停止リンク
- AuditにLEAD_CREATEDとEMAIL_SENT

## T04 LINEのみ

**入力**

- LINE選択
- delivery同意true

**期待**

- メールアドレス不要
- 受付番号表示
- `KIT LD-...`の案内
- Deliveriesはline/MANUAL_REQUIRED
- `スプレッドシートメニューの「LINE/X手動配布を完了」`後にSENT

## T05 Xのみ

**入力**

- X選択
- 有効なX handle
- delivery同意true

**期待**

- 受付番号表示
- Deliveriesはx/MANUAL_REQUIRED
- 不正なhandleは拒否

## T06 複数チャネル

**入力**

- email + LINE + X
- emailをpreferred

**期待**

- Leadは1件
- Deliveryは3件
- emailだけ自動キュー
- LINE/Xは手動待ち

## T07 チャネル未選択

**期待**

- クライアント側とサーバー側の両方で拒否
- Leadsへ書き込まれない

## T08 delivery同意なし

**期待**

- 拒否
- updates/offersだけを選んでも受付しない

## T09 ボット用ハニーポット

**入力**

非表示のwebsiteフィールドに値を入れて直接submit

**期待**

- 受付拒否
- 個人情報行を作らない

## T10 送信枠ゼロ

**準備**

`MAIL_SAFETY_CAP_PER_DAY`を、当日送信済み数以下へ一時設定

**期待**

- `Limit Lead Hub → メールキューを処理` は例外終了しない
- PENDINGが残る
- AuditへEMAIL_QUEUE_SKIPPED

## T11 送信失敗

**準備**

検証環境で意図的に送信エラーを再現できる場合のみ実施

**期待**

- attemptsが増える
- 3回未満はPENDING
- 3回目でFAILED
- error_code/messageが残る

## T12 配信停止

**操作**

メールの停止リンクを開く

**期待**

- Lead status = UNSUBSCRIBED
- consent_updates/offers = false
- 未送信emailがCANCELLED
- AuditへALL_UNSUBSCRIBED

## T13 不正な停止トークン

**期待**

- 対象なしと表示
- 他のLeadを変更しない

## T14 シートヘッダー改変

**操作**

複製したテスト環境でヘッダーを変更し、setup実行

**期待**

- 自動上書きせずエラー
- 既存データを破壊しない

## T15 復旧

**操作**

1. 本番前バックアップSheetsを複製
2. Apps Scriptコードをコミット版から復元
3. setupまたはSPREADSHEET_IDを再設定

**期待**

- Lead/Delivery/Auditが読み出せる
- 未送信キューを再開できる

## 未検証ラベル

実機テストが終わるまで、PRとRTS-Liteの状態は以下です。

```text
CODE_STATIC_CHECK = PASS
GOOGLE_LIVE_TEST = PENDING
EMAIL_LIVE_TEST = PENDING
LINE_LIVE_TEST = PENDING
X_LIVE_TEST = PENDING
PRODUCTION_DEPLOY = NOT_APPROVED
```
