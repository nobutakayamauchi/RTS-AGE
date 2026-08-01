# Limit Lead Hub MVP

`LD-LEAD-0001` — 限界開発スターターキット向けの、無料枠優先・チャネル交換可能な受付／配布管理システムです。

> **現在地:** proposal build。コードと手順は作成済みですが、Google Apps Script、Gmail、LINE、Xでの実機テストと本番公開は未実施です。

## 何を解決するか

受取希望者は、メール・LINE・Xから最低一つを選びます。複数選択も可能です。

- メール: Apps Scriptの送信キューで自動配布
- LINE: 申込者から受付番号を送ってもらい、手動返信
- X: 申込者からDMまたは返信をもらい、手動返信

本体はGoogle Sheetsの台帳です。各チャネルは交換可能な出口として扱います。

```text
Webフォーム
    ↓
Google Sheets
    ├─ Leads       連絡先・同意・状態
    ├─ Deliveries  配布キュー・配布版・結果
    ├─ Audit       操作・状態遷移
    └─ Config      交換可能な設定
    ↓
email / LINE / X
```

## MVPで守る境界

- 送付に必要な同意と、更新通知・商品案内の同意を分離
- メールは残り送信枠と独自安全上限を確認してキュー処理
- LINEの一斉配信／Push APIは使わない
- Xの自動・大量DMは使わない
- 秘密情報をソースコードへ置かない
- 実データをGitHubへ置かない
- 配信停止は確認ボタンを押す二段階方式
- 失敗時もフォーム申請そのものを消さず、再送可能な状態を残す

## ファイル

| ファイル | 役割 |
| --- | --- |
| `Code.gs` | 台帳、受付、配布キュー、配信停止、監査ログ |
| `Form.html` | 公開申込フォーム |
| `Unsubscribe.html` | 誤クリックを避ける二段階の配信停止確認 |
| `appsscript.json` | Apps Script設定 |
| `docs/SETUP.md` | 初期構築と公開手順 |
| `docs/OPERATIONS.md` | 日々の運用、LINE/X手動配布、障害対応 |
| `docs/PRIVACY-CHECKLIST.md` | 利用目的・同意・保管に関する実装チェック |
| `tests/static-contract.test.cjs` | Nodeで再現できる静的契約テスト |
| `tests/MANUAL-TEST-PLAN.md` | 実機テスト項目 |
| `RTS-LITE.md` | 正本、変更範囲、証拠、復旧、次の一手 |

## 最小導入順

1. 新しいGoogle Sheetsを作成
2. 拡張機能 → Apps Script
3. `Code.gs`、`Form.html`、`Unsubscribe.html`、`appsscript.json`を配置
4. Sheetsを再読み込みし、`Limit Lead Hub → 初期セットアップ`
5. `Config`を差し替え
6. `Limit Lead Hub → 設定を検証`
7. ウェブアプリとしてテストデプロイ
8. 架空データだけで手動テスト
9. 問題がなければ本番デプロイ
10. `Limit Lead Hub → トリガーを設定`

詳細は `docs/SETUP.md` を参照してください。

静的契約テストは、このディレクトリで実行します。

```bash
node tests/static-contract.test.cjs
```

## 無料枠について

Apps ScriptのMailAppは、一般の手動Gmail送信上限とは別に、アカウント種別ごとの送信先数上限があります。コードは `MailApp.getRemainingDailyQuota()` を毎回確認し、さらに `MAIL_SAFETY_CAP_PER_DAY` と `MAIL_SAFETY_CAP_PER_RUN` で低い独自上限を設定します。

初期値は以下です。

```text
MAIL_SAFETY_CAP_PER_RUN = 20
MAIL_SAFETY_CAP_PER_DAY = 80
```

実際の残量がこれより少なければ、残量側が優先されます。

## LINEとXを自動化しない理由

このMVPでは、アカウント停止・規約違反・誤送信のリスクを避けるため、利用者が先に連絡する受動方式に固定します。

```text
申請
  ↓
受付番号 LD-...
  ↓
利用者が LINE / X から「KIT LD-...」を送る
  ↓
運営者が台帳で照合し、リンクを返信
  ↓
スプレッドシートメニューで完了記録
```

将来API接続する場合も、中央台帳の形式は変えず、チャネルアダプターだけ交換します。

## まだやっていないこと

- Google実機での権限承認
- ウェブアプリ公開
- 実メール送信
- LINE公式アカウントとの実地照合
- Xでの実地照合
- 法務専門家による文面レビュー
- 外部メルマガサービス連携

これらが終わるまで、状態は `VERIFYING` ではなく `PROPOSAL_BUILT / LIVE_UNVERIFIED` です。

## 公式資料

- Apps Script quotas: https://developers.google.com/apps-script/guides/services/quotas
- Gmail sending limits: https://support.google.com/mail/answer/22839
- LINE Official Account plans: https://www.lycbiz.com/jp/service/line-official-account/plan/
- LINE message-count rules: https://www.lycbiz.com/jp/manual/OfficialAccountManager/account-settings/
- X automation rules: https://help.x.com/en/rules-and-policies/x-automation
- 個人情報保護委員会 通則ガイドライン: https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/
