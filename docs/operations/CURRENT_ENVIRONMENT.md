# RTS-AGE Current Environment

## Document status

- Snapshot time: 2026-08-01 12:04 JST
- Purpose: record the currently verified deployment, security boundary, repository copies, and candidate validation state
- Secrets: not included
- Candidate automated test result: **PENDING at this checkpoint**

This document distinguishes confirmed facts from pending or unverified items. Update it after every production switch, connection change, authentication change, or runtime upgrade.

## Current architecture

```mermaid
flowchart TD
    I[iPhone / operator] --> SSH[SSH client]
    I --> GH[GitHub]
    I --> AI[ChatGPT / Codex等]
    SSH --> VM[Oracle Cloud VM]
    GH --> P[/home/ubuntu/free-claude-code\nproduction copy]
    GH --> C[/home/ubuntu/RTS-AGE\ncandidate copy]
    VM --> SD[systemd]
    SD --> SVC[rts.service]
    SVC --> P
    P --> API[FastAPI / Uvicorn\n127.0.0.1:8082]
    API --> PROVIDERS[外部AIプロバイダー]
    C --> TESTS[dependency sync / tests / candidate runtime]
```

## Host and operating system

| Item | Verified value |
| --- | --- |
| Hosting | Oracle Cloud virtual server |
| Hostname | `rts` |
| OS | Ubuntu 24.04.4 LTS |
| Kernel | `6.17.0-1019-oracle` |
| Git | `2.43.0` |
| System Python | `3.12.3` |
| uv | `0.11.21` |
| Node.js | Not installed |
| Pending OS updates | 0 at the last verification |
| Reboot required | No at the last verification |
| Broken package audit | 0 lines |

The kernel was updated from `6.17.0-1011-oracle` to `6.17.0-1019-oracle`, followed by a successful reboot.

## Production systemd service

| Item | Verified value |
| --- | --- |
| Unit | `rts.service` |
| Unit file | `/etc/systemd/system/rts.service` |
| Enabled | Yes |
| Active state | `active` |
| Substate | `running` |
| User | `ubuntu` |
| Working directory | `/home/ubuntu/free-claude-code` |
| Command | `/home/ubuntu/free-claude-code/.venv/bin/python server.py` |
| Environment file | `/home/ubuntu/free-claude-code/.env` |
| Restart policy | `on-failure` |
| Restart delay | 5 seconds |
| Logging | systemd journal |

At the last full health check:

```text
ExecMainStatus=0
NRestarts=0
HTTP /=200 before authentication hardening
journal warning..alert: no entries
```

After authentication hardening, protected root access without credentials correctly returns `401`.

## Production repository copy

| Item | Verified value |
| --- | --- |
| Path | `/home/ubuntu/free-claude-code` |
| GitHub repository | `nobutakayamauchi/RTS-AGE` |
| Branch | `fix/nvidia-nim-payload` |
| Commit | `828430b3c5a731ee18c0a80dd95da980e96c8ef7` |
| Local tracked changes | 0 at the last verification |
| Runtime Python | CPython 3.14.0 through the project virtual environment |

The branch commit contains the NVIDIA NIM payload correction. That correction was already merged to GitHub main through PR #3. The production copy has not yet been switched to current main.

## Production API boundary

| Check | Verified result |
| --- | --- |
| Listener | `127.0.0.1:8082` |
| IPv4 loopback listeners | 1 |
| IPv6 loopback listeners | 0 |
| Non-loopback listeners | 0 |
| `/health` | HTTP `200` |
| `/` without authentication | HTTP `401` |
| `/` with authentication | HTTP `200` |
| Access through server private interface | No response (`000`) |

This means the application is currently reachable only from the server loopback interface. A remote client must use a controlled path such as an SSH tunnel rather than connecting directly to port 8082.

## Authentication and secret file permissions

| File | Purpose | Mode |
| --- | --- | --- |
| `/home/ubuntu/free-claude-code/.env` | Runtime provider and server configuration | `600` |
| `/home/ubuntu/.config/rts/client.env` | Local client base URL and authentication token | `600` |

The actual token and provider keys are intentionally excluded from this document.

## Firewall and reverse proxy state

| Item | Verified state |
| --- | --- |
| UFW | Not installed |
| `iptables-persistent` | Installed |
| `netfilter-persistent` | Installed |
| nginx | Inactive |
| Caddy | Inactive |
| Apache | Inactive |

A previous command attempted to call UFW, but UFW was not installed and no UFW rules were applied. The application boundary was secured by binding the service to loopback and requiring application authentication.

Oracle Cloud Security List or NSG settings were not reviewed during this checkpoint. Because the process has no non-loopback listener, port 8082 is not exposed by the application itself.

## Candidate repository copy

| Item | Verified value |
| --- | --- |
| Path | `/home/ubuntu/RTS-AGE` |
| Branch | `main` |
| Commit | `5af03d0922daa1d55b8e5e33adc77f150d1690a8` |
| Sync method | fast-forward from `origin/main` |
| Commits advanced | 147 |
| Files changed by sync | 79 |
| Approximate additions | 5,019 lines |
| Local tracked changes | 0 |
| Candidate Python | 3.14.0 |
| Dependency manager | uv |
| Packages installed in candidate venv | 76 |
| Dependency command | `uv sync --frozen` |
| Dependency sync result | Passed |

The candidate copy is separate from production. Synchronizing and installing dependencies in this directory did not change the active `rts.service` or production port 8082.

## Candidate test state

At this snapshot, the following automated test command had been started:

```bash
env MESSAGING_PLATFORM=none VOICE_NOTE_ENABLED=false \
  timeout 600 uv run --frozen pytest -q -n 2
```

The command redirects output to a temporary log and may remain visually quiet while tests run.

Status at this document checkpoint:

```text
candidate repository sync: PASSED
candidate dependency sync: PASSED
candidate automated tests: PENDING
candidate parallel runtime on 18082: NOT STARTED
production switch to current main: NOT STARTED
```

Do not mark the candidate as production-ready until the test result and parallel runtime checks are recorded.

## Confirmed backup and rollback points

| Backup | Purpose |
| --- | --- |
| `/var/backups/rts-security-20260801T024655Z` | Pre-hardening `.env` and systemd service backup |
| `/var/backups/rts-pre-update-*` | Pre-OS-update package, service, and Git state records |

The security hardening command also created a local client configuration containing the newly generated token. Token values must never be copied into GitHub documentation.

## Current production/candidate split

```text
PRODUCTION
/home/ubuntu/free-claude-code
└─ active through rts.service
   └─ 127.0.0.1:8082

CANDIDATE
/home/ubuntu/RTS-AGE
└─ current GitHub main
   ├─ Python 3.14 venv prepared
   ├─ dependencies synchronized
   ├─ automated tests pending
   └─ parallel port 18082 not yet validated
```

## Remaining work before production switch

1. Record the complete candidate automated test result.
2. If tests pass, start the candidate temporarily on `127.0.0.1:18082` with messaging and voice integrations disabled.
3. Verify candidate health, authentication, model listing, and loopback-only binding.
4. Confirm production 8082 remains healthy during candidate testing.
5. Prepare a backup-backed systemd switch plan.
6. Switch only after explicit human approval.
7. Run final health, authentication, listener, restart-count, and journal checks.
8. Update this document and the environment changelog.

## Known unknowns

- The active provider and model values were not printed because configuration files contain secrets.
- Oracle Cloud Security List and NSG rules were not inspected in this session.
- Candidate automated test outcome was pending when this snapshot was written.
- Candidate compatibility with the active live provider has not yet been validated through a real message request.
- No reverse proxy or HTTPS termination is currently part of the local service path.

## Update trigger

Update this document whenever any of the following changes:

- production Git commit or branch
- service working directory or command
- port or bind address
- authentication policy
- secret file location or permission
- Python or uv version
- provider routing
- candidate validation state
- backup or rollback procedure
- external access method
