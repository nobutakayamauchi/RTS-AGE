# セットアップ手順

## 0. 完成条件

この手順の完成は、単にフォームが表示されることではありません。

- 架空のメール申請が `Leads` と `Deliveries` に残る
- メールがキューから送信される、または送信枠不足で安全に保留される
- LINEのみ・Xのみの申請で受付番号が表示される
- 手動配布完了を記録できる
- 配信停止リンクで同意状態が変わる
- `Audit` に主要イベントが残る
- 元のSheetsを複製すれば復旧できる

## 1. Google Sheetsを作る

1. 新しいGoogle Sheetsを作成
2. 名前を `Limit Lead Hub` などに変更
3. タイムゾーンを日本へ設定
4. 実顧客データを入れる前に、共有設定を確認

シートは自分だけ、または本当に必要な管理者だけに共有してください。

## 2. Apps Scriptへファイルを置く

Sheetsから、`拡張機能 → Apps Script` を開きます。

以下を配置します。

- `Code.gs`
- `Form.html`
- `Unsubscribe.html`
- `appsscript.json`

`appsscript.json`を編集するには、Apps Script設定からマニフェスト表示を有効にします。

## 3. 初期セットアップ

Sheetsを再読み込みし、上部メニューから次を実行します。

```text
Limit Lead Hub → 初期セットアップ
```

初回はGoogleの権限確認が表示されます。内容を確認し、自分が作成したスクリプトであることを確かめてから許可してください。

実行後、以下のシートができます。

- `Leads`
- `Deliveries`
- `Audit`
- `Config`

また、Script Propertiesに `SPREADSHEET_ID` が保存されます。

## 4. Configを差し替える

最低限、以下を変更します。

| key | 設定 |
| --- | --- |
| `CURRENT_KIT_VERSION` | 配布版。例 `v0.1.0` |
| `KIT_NAME` | 配布物名 |
| `KIT_URL` | 固定の最新版配布ページURL |
| `LINE_ADD_URL` | LINE公式アカウント追加URL。使わないなら空欄 |
| `X_PROFILE_URL` | XプロフィールURL。使わないなら空欄 |
| `PRIVACY_POLICY_URL` | 利用目的・取扱方針のURL |
| `SENDER_NAME` | メール送信者名 |

送信安全上限は最初は下げたままにします。

```text
MAIL_SAFETY_CAP_PER_RUN = 20
MAIL_SAFETY_CAP_PER_DAY = 80
```

## 5. 設定を検証する

```text
Limit Lead Hub → 設定を検証
```

`ok: true`になるまで公開しません。

特に `KIT_URL` が `example.com/replace-me` のままでは公開禁止です。

## 6. テストデプロイ

1. `デプロイ → デプロイをテスト`
2. ウェブアプリを開く
3. `tests/MANUAL-TEST-PLAN.md` の架空データで確認
4. 実在する第三者のアドレス・LINE名・Xアカウントは使わない

## 7. 本番デプロイ

テスト通過後に新しいデプロイを作成します。

- 種類: ウェブアプリ
- 次のユーザーとして実行: 自分
- アクセスできるユーザー: 申込を受ける範囲に合わせる

公開URLを取得したら、`Config` の `WEB_APP_URL` に保存してください。

その後、もう一度 `Limit Lead Hub → 設定を検証` を実行します。

## 8. メールキュートリガー

```text
Limit Lead Hub → トリガーを設定
```

15分ごとに非公開のメールキュー処理が実行されます。

Apps Scriptの残り送信先数は毎回自動確認されます。上限到達時は未送信を `PENDING` のまま残し、次回へ回します。

## 9. LINEの準備

LINEはMVPではAPI接続しません。

1. LINE公式アカウントを準備
2. 友だち追加URLを `LINE_ADD_URL` へ設定
3. あいさつメッセージに次を案内

```text
スターターキットを受け取る方は、申請後に表示された受付番号を
「KIT LD-...」の形で送ってください。
```

受信後、`Deliveries`で受付番号を検索し、キットURLを手動返信します。

## 10. Xの準備

XもMVPでは自動DMしません。

1. 配布用の固定投稿を作る
2. 申請者にDMまたは返信で `KIT LD-...` を送ってもらう
3. 台帳で照合
4. キットURLを手動返信
5. 完了記録

```text
Limit Lead Hub → LINE/X手動配布を完了
```

受付番号を入力した後、LINEなら `line`、Xなら `x` を指定します。

## 11. バックアップ

本番公開前に、Sheets全体を複製してください。

推奨名:

```text
Limit Lead Hub BACKUP before-live 2026-08-01
```

コードはGitHubのコミット・PRを復旧点にします。個人情報を含むSheetsはGitHubへ出しません。
