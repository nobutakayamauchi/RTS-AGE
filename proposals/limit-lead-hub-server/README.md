# Limit Lead Hub Server MVP

Google Sheets / Apps Script版を置き換える、既存サーバー向けの小型リード受付・配布管理システムです。

## 現在地

`PROPOSAL_BUILT / SERVER_LIVE_UNVERIFIED`

Google UIを本線から外し、以下をサーバー内で完結させます。

```text
公開申込フォーム
    ↓
FastAPI
    ↓
SQLite
    ├─ leads
    ├─ deliveries
    └─ audit
    ↓
email / LINE / X の交換可能な出口
```

## MVPでできること

- メール・LINE・Xから最低一つを選ぶ申込フォーム
- 複数チャネル選択
- 今回の送付／更新通知／商品案内の同意分離
- 非推測型の受付番号と配信停止トークン
- SQLiteによるリード・配布履歴・監査ログ保存
- LINE/Xの手動配布待ち一覧
- メール送付待ちキュー
- Basic認証付き管理画面
- 手動で送付済み／失敗を記録
- CSV出力
- 配信停止

メールはこの第一段階では `PENDING` に積むだけです。SMTP、Brevo、Gmail API等は後からアダプターとして接続します。

## 起動

既存RTS-AGE環境の依存関係を利用できます。

```bash
cd proposals/limit-lead-hub-server
cp .env.example .env
set -a
. ./.env
set +a
uv run uvicorn app:app --host 127.0.0.1 --port 8090
```

確認:

```bash
curl http://127.0.0.1:8090/healthz
```

ブラウザ:

```text
/lead/apply   公開申込フォーム
/lead/admin   管理画面
```

## 公開前に必ず変更する値

```text
LLH_KIT_URL
LLH_ADMIN_PASSWORD
LLH_ADMIN_ACTION_TOKEN
LLH_PRIVACY_POLICY_URL
```

`/healthz` の `config_problems` が空になるまでは外部公開しません。

## 配置方針

最初は `127.0.0.1:8090` にのみバインドし、既存のリバースプロキシ経由で必要なパスだけ公開します。

```text
/lead/apply
/api/leads
/lead/unsubscribe
/api/unsubscribe
```

管理系は公開範囲を狭めます。

```text
/lead/admin
/api/admin/*
/lead/export.csv
```

可能なら管理系はVPN、IP制限、別ホスト、追加認証のいずれかを重ねます。

## バックアップ

SQLiteを停止または整合した状態でコピーします。

```bash
mkdir -p backups
sqlite3 data/limit-lead-hub.sqlite3 ".backup 'backups/limit-lead-hub-$(date +%F-%H%M%S).sqlite3'"
```

実データをGitHubへコミットしません。

## Google版の扱い

旧PR #76は `SUPERSEDED`。Google Sheets / Apps Script版は参考実装として残し、本番運用には使いません。

## 次の実機工程

1. サーバーへブランチを取得
2. テスト用 `.env` を作成
3. ループバックで起動
4. 架空データでメールのみ／LINEのみ／Xのみ／複数チャネルを確認
5. 管理画面・CSV・配信停止を確認
6. SQLiteバックアップと復元を確認
7. その後にメール送信アダプターを選定
8. リバースプロキシとTLSを設定

実機検証完了前の本番公開は `NOT_APPROVED` です。
