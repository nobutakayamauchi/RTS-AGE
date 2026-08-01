# RTS-Lite — LD-LEAD-SERVER-0001

## PROJECT

Limit Lead Hub Server MVP

## PURPOSE

限界開発スターターキットの受取希望者をメール・LINE・Xから最低一つの窓口で受け付け、同意・配布版・送付状態をサーバー上のSQLiteで管理する。

## CANONICAL SOURCE

- Code: `nobutakayamauchi/RTS-AGE`
- Branch: `feat/limit-lead-hub-server-mvp-20260801`
- Work Order: Issue `#75`
- Runtime data: server-private SQLite file

実リード情報・バックアップ・秘密情報はGitHubへ置かない。

## BOUNDARY

### Allowed

- `proposals/limit-lead-hub-server/**`
- isolated server proposal
- loopback-only test
- synthetic test data

### Protected

- existing production service on port 8082
- existing `server.py` and API routes
- production `.env`
- live LINE/X accounts
- real customer data
- public deployment
- `main` direct push

## STATUS

`PROPOSAL_BUILT / SERVER_LIVE_UNVERIFIED`

## EVIDENCE

- Server-side source committed: PASS
- Google Apps Script dependency removed from canonical design: PASS
- SQLite schema present: PASS
- public form / admin / CSV / unsubscribe source present: PASS
- server syntax check: PENDING
- loopback boot: PENDING
- live browser test: PENDING
- backup/restore: PENDING
- reverse proxy/TLS: PENDING
- real delivery adapter: PENDING

## RECOVERY

- Code: branch commit or draft PR
- Runtime: SQLite `.backup`
- Bad deploy: stop the new service and restore previous SQLite copy
- Channel failure: retain ledger and replace only the channel adapter
- Google variant: closed draft PR #76 remains reference-only

## NEXT ACTION

1. Open draft PR
2. Pull branch to the server without touching the running 8082 service
3. create test `.env`
4. run syntax/import check
5. start on `127.0.0.1:8090`
6. execute synthetic tests
7. record results in Issue #75

## PRODUCTION GATE

Production remains `NOT_APPROVED` until configuration secrets are changed, synthetic tests pass, backup/restore succeeds, and the public/admin routing boundary is reviewed.
