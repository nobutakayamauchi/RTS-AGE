# Limit Lead Hub Server MVP

FastAPI + SQLite で、限界開発スターターキットの受取希望者と配布状態を管理する最小構成です。

## Public routes

- `/lead/apply` — 受取申請フォーム
- `/kit` — スターターキット案内
- `/kit/latest` — 最新ZIP
- `/lead/privacy` — 取扱方針
- `/lead/unsubscribe` — 配信停止画面
- `/api/leads` — 公開申込API
- `/api/unsubscribe` — 公開配信停止API

## Private routes

- `/lead/admin`
- `/lead/export.csv`
- `/api/admin/**`
- `/healthz`
- FastAPI docs / OpenAPI routes

公開時は `caddy/limit-lead-hub.Caddyfile` の許可リストを使い、private routes を外部へ通さないでください。

## Loopback test

```bash
LLH_UVICORN_BIN=/home/ubuntu/RTS-AGE/.venv/bin/uvicorn bash scripts/bootstrap-test.sh
```

停止:

```bash
bash scripts/stop-test.sh
```

## Production layout

- application: `/home/ubuntu/RTS-AGE/proposals/limit-lead-hub-server`
- environment: `.env`（Git管理外、`chmod 600`）
- database: `data/limit-lead-hub.sqlite3`
- application service: `systemd/limit-lead-hub.service`
- publication boundary: `caddy/limit-lead-hub.Caddyfile`
- upstream: `127.0.0.1:8090`

## Current channel behavior

- email: `PENDING` キューへ記録。送信アダプターは未接続。
- LINE: `MANUAL_REQUIRED`。利用者が受付番号を送る方式。
- X: `MANUAL_REQUIRED`。利用者が受付番号を送る方式。

実リード投入前に、合成データを削除し、SQLiteバックアップを作成し、外部HTTPS・管理経路遮断を確認してください。
