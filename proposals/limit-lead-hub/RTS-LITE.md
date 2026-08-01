# RTS-Lite — LD-LEAD-0001

## PROJECT

Limit Lead Hub MVP

## PURPOSE

限界開発スターターキットの受取希望者を、メール・LINE・Xから最低一つの連絡口で受け付け、同意・配布版・送付状態を一つの台帳で管理する。

## CANONICAL SOURCE

- Repository: `nobutakayamauchi/RTS-AGE`
- Proposal branch: `feat/limit-lead-hub-mvp-20260801`
- Work Order / Issue: `#75`
- Runtime data canonical source: deployment owner's private Google Sheets

GitHubに置くのはコードと空の構造だけ。実リード情報は置かない。

## BOUNDARY

### Allowed

- `proposals/limit-lead-hub/**`
- proposal documentation
- static and manual tests
- draft PR metadata

### Protected

- production proxy runtime
- existing `server.py` and API routes
- production `.env`
- existing Google/LINE/X accounts
- live messaging
- real personal data
- `main` direct push

## STATUS

`PROPOSAL_BUILT / LIVE_UNVERIFIED`

## IMPLEMENTED

- Google Apps Script public form
- central Sheets ledger
- separate consent fields
- email queue with quota and safety caps
- LINE/X inbound-manual flow
- version tracking
- audit log
- two-step unsubscribe handling
- setup and operations docs
- reproducible static contract test
- manual test plan

## EVIDENCE

- JavaScript static syntax check: `PASS` using Node V8-compatible syntax check
- Static contract test: `PASS` via `node tests/static-contract.test.cjs`
- Source review: `PASS_WITH_LIMITATIONS`
- Google Apps Script live execution: `PENDING`
- Gmail/MailApp delivery: `PENDING`
- LINE flow: `PENDING`
- X flow: `PENDING`
- legal text review: `PENDING`

## UNKNOWNS

- User's exact Google account type and live MailApp quota
- Current LINE account state and previous failure cause
- Exact X receiving configuration
- Final privacy-policy URL
- Final kit delivery URL
- Final retention period
- Whether external newsletter integration will be needed before list growth

## RECOVERY

- Code recovery: GitHub branch/commit
- Runtime recovery: Google Sheets copy made before live deployment
- Channel failure: disable channel in form/config; retain ledger
- Mail quota failure: keep Delivery as PENDING and resume later
- Bad deploy: revert to prior Apps Script deployment version

## NEXT ACTION

1. Review draft PR
2. User creates or chooses a private Google Sheets test container
3. Copy files into Apps Script
4. Run T01–T15 using only controlled test data
5. Record evidence in Issue #75
6. Only then approve production deployment

## PRODUCTION GATE

Production is approved only when:

- config validation passes
- T01–T15 applicable tests pass
- one controlled email delivery succeeds
- LINE/X selected paths are manually verified
- privacy/use-purpose page is visible before form submission
- backup exists
- no real personal data appears in GitHub or screenshots
