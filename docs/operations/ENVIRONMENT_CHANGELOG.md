# RTS-AGE Environment Changelog

This file is an append-only operational changelog for deployment, connection, authentication, runtime, and recovery changes.

## Rules

- Add new entries at the top.
- Use JST for operator-facing timestamps and include UTC when the server event time matters.
- Never record API keys, authentication tokens, passwords, private keys, or customer data.
- Separate confirmed results from pending work.
- Record failed attempts when they changed the understanding of the environment.
- Link code changes to a commit or PR when available.
- Do not rewrite an old entry to make the process look cleaner than it was. Add a correction entry instead.

---

## 2026-08-01 — OS maintenance, security boundary, and current-main candidate preparation

### Summary

The Ubuntu host was updated and rebooted, the production RTS-AGE service was verified, the API boundary was changed from all-interface listening to loopback-only access with authentication, and a separate candidate copy was synchronized to the current GitHub main for testing.

### OS maintenance

Confirmed results:

- Ubuntu: `24.04.4 LTS`
- Kernel changed from `6.17.0-1011-oracle` to `6.17.0-1019-oracle`
- Reboot completed at `2026-08-01 02:23 UTC`
- Remaining package updates: 0
- Remaining removals: 0
- `dpkg --audit`: 0 lines
- Additional reboot required: no
- Production service returned automatically after reboot

Production post-reboot health:

```text
ActiveState=active
SubState=running
ExecMainStatus=0
NRestarts=0
HTTP /=200
journal warning..alert: no entries
```

### Production architecture audit

Confirmed service configuration:

```text
Unit: /etc/systemd/system/rts.service
User: ubuntu
WorkingDirectory: /home/ubuntu/free-claude-code
ExecStart: /home/ubuntu/free-claude-code/.venv/bin/python server.py
EnvironmentFile: /home/ubuntu/free-claude-code/.env
Restart: on-failure
RestartSec: 5
```

Confirmed runtime state before hardening:

```text
Listener: 0.0.0.0:8082
Production repository branch: fix/nvidia-nim-payload
Production repository commit: 828430b3c5a731ee18c0a80dd95da980e96c8ef7
Production repository changes: 0
```

A second, non-production copy existed at `/home/ubuntu/RTS-AGE` on an older main commit.

### Security hardening

Changes applied:

- Generated a new application authentication token without printing it.
- Added `HOST=127.0.0.1` to the production environment.
- Added `ANTHROPIC_AUTH_TOKEN` to the production environment.
- Set `/home/ubuntu/free-claude-code/.env` to mode `600`.
- Created `/home/ubuntu/.config/rts/client.env` with mode `600`.
- Restarted `rts.service`.
- Created rollback backup `/var/backups/rts-security-20260801T024655Z`.

Verified results:

```text
service=active
health=200
root_without_auth=401
root_with_auth=200
ipv4_loopback_listeners=1
ipv6_loopback_listeners=0
non_loopback_listeners=0
private_interface_response=000
env_mode=600
client_config_mode=600
security_boundary=passed
```

### UFW attempt and correction

The first hardening command attempted to call UFW after the application checks passed. UFW was not installed, so those commands returned `command not found`.

No UFW rules were applied.

Subsequent verification found:

```text
ufw=not_installed
iptables-persistent=installed
netfilter-persistent=installed
```

Decision:

- Do not install UFW as part of this correction.
- Retain the existing persistent netfilter arrangement.
- Treat loopback-only binding plus application authentication as the confirmed service boundary.
- Review Oracle Cloud Security List or NSG rules separately if external network policy documentation is required.

### Long command interruption

A combined candidate validation command was too long for the mobile terminal paste path and ended with the bash continuation prompt:

```text
>
```

The command was cancelled with `Ctrl+C`.

Recovery checks confirmed:

```text
production=active
production_health=200
candidate_changes=0
port_18082_listeners=0
```

Decision:

Split future mobile-terminal operations into separate steps:

1. repository sync
2. dependency sync
3. automated tests
4. candidate runtime test
5. production switch
6. final verification

### Candidate repository synchronization

Candidate path:

```text
/home/ubuntu/RTS-AGE
```

Synchronization result:

```text
Previous commit: 51112a4cf340b8e41a9314aa397a7a43fa7204b1
Current main:    5af03d0922daa1d55b8e5e33adc77f150d1690a8
Method: fast-forward
Commits advanced: 147
Files changed: 79
Additions: 5,019
Deletions: 88
Local tracked changes after sync: 0
candidate_sync=passed
```

The NVIDIA NIM payload fix had already been merged into main through PR #3. The production branch was not an unmerged source of truth; the local production copy was simply behind current main.

### Candidate dependency preparation

Command:

```bash
uv sync --frozen
```

Confirmed results:

```text
Python=3.14.0
Packages installed=76
sync_exit=0
candidate Git changes=0
production_health=200
candidate_dependency_sync=passed
```

The candidate received a new isolated `.venv`. Production remained on port 8082 and was not changed.

### Candidate automated tests

Started with messaging and voice integrations disabled:

```bash
env MESSAGING_PLATFORM=none VOICE_NOTE_ENABLED=false \
  timeout 600 uv run --frozen pytest -q -n 2
```

Status at the time this changelog entry was created:

```text
candidate_tests=PENDING
candidate_parallel_runtime=NOT_STARTED
production_switch=NOT_STARTED
```

Add a new correction or completion entry after the test result is known. Do not edit this pending state into a success retroactively.

### Files and systems intentionally not changed

- Production Git branch and commit
- Production systemd working directory
- Production systemd command
- External provider keys
- Oracle Cloud Security List or NSG rules
- nginx, Caddy, or Apache configuration
- Canonical RTS repositories
- Live publishing or external system mutation

### Next safe action

1. Capture the completed candidate test result.
2. If successful, run the candidate temporarily on `127.0.0.1:18082`.
3. Verify authentication, health, model listing, and loopback-only binding.
4. Prepare a backup-backed production switch proposal.
