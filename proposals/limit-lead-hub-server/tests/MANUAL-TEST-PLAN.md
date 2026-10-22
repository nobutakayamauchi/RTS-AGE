# Manual Test Plan — Server MVP

Use synthetic data only until production approval.

## S01 Import and syntax

```bash
cd proposals/limit-lead-hub-server
python -m py_compile app.py
uv run python -c "import app; print(app.app.title)"
```

Expected: no traceback, title `Limit Lead Hub`.

## S02 Loopback boot

```bash
uv run uvicorn app:app --host 127.0.0.1 --port 8090
curl http://127.0.0.1:8090/healthz
```

Expected: `ok: true`; config problems list incomplete values.

## S03 No channel

POST `/api/leads` with all channels false.

Expected: HTTP 400; no lead row.

## S04 Email only

Use a controlled test address.

Expected:
- one lead
- one email delivery
- status `PENDING`
- no actual email sent

## S05 LINE only

Expected:
- email not required
- one LINE delivery
- status `MANUAL_REQUIRED`
- response instructs `KIT LD-...`

## S06 X only

Expected:
- valid `@handle` accepted
- malformed handle rejected
- status `MANUAL_REQUIRED`

## S07 Multiple channels

Expected: one lead and one delivery per selected channel.

## S08 Consent separation

Expected:
- delivery consent required
- updates/offers optional
- unchecked values stored as zero

## S09 Admin authentication

Expected:
- unauthenticated `/lead/admin` returns 401
- correct Basic credentials show ledger
- wrong action token returns 403

## S10 Manual completion

Mark LINE/X delivery as sent.

Expected:
- status `SENT`
- attempts increment
- sent timestamp set
- lead last delivery updated
- audit event present

## S11 CSV

Expected: authenticated download, UTF-8 BOM, no unsubscribe token column.

## S12 Unsubscribe

Use the stored token in a controlled test.

Expected:
- lead becomes `UNSUBSCRIBED`
- update/offer consent becomes zero
- pending email delivery becomes `CANCELLED`
- audit event present

## S13 Backup and restore

```bash
sqlite3 data/limit-lead-hub.sqlite3 ".backup '/tmp/llh-test-backup.sqlite3'"
```

Point `LLH_DB_PATH` to the copy and restart.

Expected: lead, delivery, and audit rows remain readable.

## S14 Existing production isolation

Expected:
- existing port 8082 remains untouched
- proposal binds only to `127.0.0.1:8090`
- no systemd unit is installed until separate approval

## Gate

```text
SYNTAX_IMPORT = PENDING
LOOPBACK_BOOT = PENDING
SYNTHETIC_FLOW = PENDING
BACKUP_RESTORE = PENDING
PUBLIC_PROXY = NOT_APPROVED
REAL_CUSTOMER_DATA = NOT_APPROVED
```
