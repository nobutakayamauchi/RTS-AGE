#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"

PID_FILE="run/limit-lead-hub.pid"
if [[ ! -f "$PID_FILE" ]]; then
  echo 'No PID file; nothing to stop.'
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  for _ in $(seq 1 20); do
    if ! kill -0 "$PID" 2>/dev/null; then
      break
    fi
    sleep 0.25
  done
fi

rm -f "$PID_FILE"
echo 'Limit Lead Hub loopback test stopped.'
