#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$HERE"

PYTHON_BIN="${LLH_PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  else
    printf '%s\n' 'Neither python3 nor python is available. Stop without changing anything.' >&2
    exit 1
  fi
fi

INITIALIZE_ENV=0
if [[ ! -f .env ]]; then
  INITIALIZE_ENV=1
elif grep -q '^LLH_ADMIN_PASSWORD=replace-me$' .env \
  && grep -q '^LLH_ADMIN_ACTION_TOKEN=replace-me$' .env; then
  printf '%s\n' 'Incomplete placeholder .env detected; regenerating test secrets.'
  INITIALIZE_ENV=1
fi

if [[ "$INITIALIZE_ENV" -eq 1 ]]; then
  cp .env.example .env
  ADMIN_PASSWORD="$("$PYTHON_BIN" -c 'import secrets; print(secrets.token_urlsafe(18))')"
  ACTION_TOKEN="$("$PYTHON_BIN" -c 'import secrets; print(secrets.token_urlsafe(32))')"
  "$PYTHON_BIN" - "$ADMIN_PASSWORD" "$ACTION_TOKEN" <<'PY'
from pathlib import Path
import sys
path = Path('.env')
text = path.read_text(encoding='utf-8')
text = text.replace('LLH_ADMIN_PASSWORD=replace-me', f'LLH_ADMIN_PASSWORD={sys.argv[1]}')
text = text.replace('LLH_ADMIN_ACTION_TOKEN=replace-me', f'LLH_ADMIN_ACTION_TOKEN={sys.argv[2]}')
path.write_text(text, encoding='utf-8')
PY
  chmod 600 .env
  printf '%s\n' "Generated test admin password: $ADMIN_PASSWORD"
else
  printf '%s\n' '.env already exists; preserving it.'
fi

mkdir -p data run
"$PYTHON_BIN" -m py_compile app.py kit_app.py

if [[ -f run/limit-lead-hub.pid ]] && kill -0 "$(cat run/limit-lead-hub.pid)" 2>/dev/null; then
  printf '%s\n' 'Limit Lead Hub test process is already running.'
else
  if command -v ss >/dev/null 2>&1 && ss -ltn | grep -q ':8090 '; then
    printf '%s\n' 'Port 8090 is already in use. Stop here without changing anything.' >&2
    exit 1
  fi

  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a

  if [[ -n "${LLH_UVICORN_BIN:-}" && -x "$LLH_UVICORN_BIN" ]]; then
    RUNNER=("$LLH_UVICORN_BIN")
  elif [[ -x "$ROOT/.venv/bin/uvicorn" ]]; then
    RUNNER=("$ROOT/.venv/bin/uvicorn")
  elif [[ -x /home/ubuntu/RTS-AGE/.venv/bin/uvicorn ]]; then
    RUNNER=(/home/ubuntu/RTS-AGE/.venv/bin/uvicorn)
  else
    RUNNER=(uv run uvicorn)
  fi

  nohup "${RUNNER[@]}" kit_app:app --host 127.0.0.1 --port 8090 \
    > run/limit-lead-hub.log 2>&1 &
  echo $! > run/limit-lead-hub.pid
fi

for _ in $(seq 1 20); do
  if curl -fsS http://127.0.0.1:8090/healthz > run/health.json; then
    break
  fi
  sleep 0.5
done

if ! curl -fsS http://127.0.0.1:8090/healthz; then
  printf '\nStartup failed. Last log lines:\n' >&2
  tail -n 80 run/limit-lead-hub.log >&2 || true
  exit 1
fi

cat <<'EOF'

Loopback test is running.

Public form:
  http://127.0.0.1:8090/lead/apply

Starter kit:
  http://127.0.0.1:8090/kit

Privacy policy:
  http://127.0.0.1:8090/lead/privacy

Admin:
  http://127.0.0.1:8090/lead/admin

The service is bound to 127.0.0.1 only. No public route, reverse proxy, or systemd unit was changed.
EOF
