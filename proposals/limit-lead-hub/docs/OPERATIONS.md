# 運用手順

## 毎日の確認

`Deliveries`をフィルタして、以下を確認します。

- `PENDING`: メール送信待ち
- `MANUAL_REQUIRED`: LINE/Xで手動対応が必要
- `FAILED`: 3回失敗し、自動再試行を止めた
- `SENT`: 送付済み
- `CANCELLED`: 配信停止または同意不足

## メール

通常は15分ごとのトリガーで処理されます。手動実行も可能です。

```text
Limit Lead Hub → メールキューを処理
```

送信枠が少ない場合、キューは消えません。独自安全上限またはGoogle側上限が回復した後に再処理します。

`FAILED`を再送する場合は、原因を確認してからステータスを `PENDING` に戻します。原因を直さず一括で戻さないでください。

## LINE

1. LINEで `KIT LD-...` を受信
2. `Leads`で受付番号を検索
3. `channel_line = TRUE` と `consent_delivery = TRUE` を確認
4. `Deliveries`で同じ受付番号・channel `line` を確認
5. `KIT_URL`を返信
6. 完了記録

```text
Limit Lead Hub → LINE/X手動配布を完了
```

一斉配信はこのMVPの運用外です。

## X

1. DMまたは返信で `KIT LD-...` を受信
2. `Leads`の `x_handle` と照合
3. 受付番号・同意を確認
4. キットURLを返信
5. 完了記録

```text
Limit Lead Hub → LINE/X手動配布を完了
```

フォローしているだけの人へ、こちらから大量DMしません。

## 更新版の配布

MVPの初回自動メールは、申請時のキット送付だけです。更新一斉送信機能はまだ実装していません。

更新版を出す場合:

1. `CURRENT_KIT_VERSION` を変更
2. `KIT_URL`の内容を更新
3. `consent_updates = TRUE` の対象を抽出
4. 送信数と同意を確認
5. 別Work Orderで更新配信キューを作る

同意のない人を更新案内リストへ混ぜないでください。

## 重複申請

MVPは、同じ人の複数申請を自動統合しません。誤統合による個人情報事故を避けるためです。

同じメール・Xアカウントを見つけた場合:

- 古い申請を消さない
- 受付番号ごとに配布履歴を残す
- 必要なら `notes` に関連受付番号を記録
- 自動統合は次段階の仕様として扱う

## 配信停止

メール本文の停止リンクは、`consent_updates` と `consent_offers` をfalseにし、lead statusを `UNSUBSCRIBED` にします。未送信のメールキューもキャンセルします。

一度停止した人へ再配信する場合は、新しい明示的な同意を取得してください。

## 障害時

### フォームが開かない

- Apps Scriptのデプロイ状態
- 実行ユーザー
- アクセス範囲
- Apps Script実行ログ
- `SPREADSHEET_ID`

を確認します。

### メールが送れない

- `MailApp.getRemainingDailyQuota()`
- `MAIL_SAFETY_CAP_PER_DAY`
- `Deliveries.error_code`
- 宛先の形式
- Apps Script実行履歴

を確認します。

### LINE/Xアカウントが使えない

中央台帳はそのまま残します。

- 当該チャネルの新規受付をフォーム説明から外す
- 既存申請者へ、利用可能な別チャネルから再連絡を依頼
- `Config`のURLを交換

台帳をLINE/X側へ依存させないことが復旧の核心です。
