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
- loopback-only validation
- synthetic test data
- restricted HTTPS publication of the public form, starter kit, privacy page, and unsubscribe flow

### Protected

- existing production service on port 8082
- existing `server.py` and API routes
- production `.env`
- live LINE/X accounts
- real customer data
- admin, CSV, OpenAPI, docs, health, and internal API routes from public access
- `main` direct push

## STATUS

`SERVER_MVP_COMPLETE / PUBLICATION_APPROVED_IN_PROGRESS`

## EVIDENCE

- Server-side source committed: PASS
- Google Apps Script dependency removed from canonical design: PASS
- SQLite schema present: PASS
- public form / admin / CSV / unsubscribe source present: PASS
- self-hosted starter-kit ZIP and privacy page present: PASS
- server syntax/import check: PASS
- loopback boot on `127.0.0.1:8090`: PASS
- synthetic email / LINE / X / multi-channel flows: PASS
- admin auth / CSV / delivery transitions / unsubscribe: PASS
- SQLite backup/restore and integrity: PASS
- public routing boundary inspected: PASS
- restricted Caddy publication template: PASS
- reverse proxy/TLS live publication: IN_PROGRESS
- real email delivery adapter: PENDING

## RECOVERY

- Code: branch commit or PR #77
- Runtime: SQLite `.backup`
- Bad deploy: stop `limit-lead-hub.service`, stop Caddy, and restore the previous SQLite copy
- Channel failure: retain ledger and replace only the channel adapter
- Google variant: closed draft PR #76 remains reference-only

## NEXT ACTION

1. merge reviewed PR #77
2. install the application as an independent systemd service on loopback port 8090
3. install Caddy without exposing admin/internal routes
4. publish through a temporary HTTPS hostname
5. verify externally from a non-server client
6. delete synthetic runtime data before accepting real leads
7. record deployment evidence in Issue #75

## PRODUCTION GATE

Public form publication is approved by the user. Real lead acceptance remains gated on successful external HTTPS verification, removal of synthetic data, confirmed admin-route denial, and a fresh SQLite backup.
