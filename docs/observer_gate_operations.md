# Observer Gate Operations

This guide explains how to operate the RTS-AGE observer gate safely.

The observer gate is designed to treat AI providers as observers, not as a
single final authority. It classifies work, scores risk, proposes a routing
choice, optionally logs the decision, and lets operators inspect those logs.

## Current flow

```text
specs/multi_observer_v0.yaml
-> load_observer_policy()
-> evaluate_observer_gate()
-> route_observer()
-> ObserverDecision
-> optional JSONL logging
-> observer-log
-> optional observer decision report
```

## Safety defaults

The observer gate is safe by default.

- It is disabled unless explicitly enabled.
- It does not call external AI providers.
- It does not call Fusion.
- It does not change the provider registry.
- It does not execute tasks.
- It does not log request text.
- It returns or records routing metadata only.

## Configuration

### Enable observer gate evaluation

```bash
RTS_AGE_OBSERVER_GATE_ENABLED=true
```

When this variable is not set, the entrypoint returns a default disabled
decision.

```text
selected_observer=default
score=0
should_use_fusion=false
task_type=observer_gate_disabled
```

### Enable JSONL logging

```bash
RTS_AGE_OBSERVER_GATE_LOG_ENABLED=true
```

Logging is off by default. When enabled, only decision metadata is written.
Request text is not logged.

### Configure log path

```bash
RTS_AGE_OBSERVER_GATE_LOG_PATH=logs/observer_decisions.jsonl
```

If not configured, the default path is:

```text
logs/observer_decisions.jsonl
```

## Proposal endpoint

The internal proposal endpoint returns a routing proposal only.

```text
POST /internal/observer-gate/proposal
```

The endpoint is protected by the existing API key dependency.

Example request:

```json
{
  "task_id": "demo-1",
  "text": "顧客納品用の公開営業LPをレビューして"
}
```

Example response shape:

```json
{
  "mode": "proposal",
  "observer_gate_enabled": true,
  "task_id": "demo-1",
  "task_type": "paid_delivery",
  "selected_observer": "fusion",
  "score": 7,
  "should_use_fusion": true,
  "reasons": ["paid_delivery: +3", "public_release: +2"]
}
```

## Log inspection

Use the CLI to inspect recent observer decisions.

```bash
uv run observer-log
```

Show a custom file and limit:

```bash
uv run observer-log --path logs/observer_decisions.jsonl --limit 5
```

If no log exists, the command prints a friendly empty-state message.

The output intentionally excludes request text and metadata.

## Summary report

Use summary mode to inspect aggregate observer routing behavior.

```bash
uv run observer-log --summary
```

Summary mode supports the same path and limit options:

```bash
uv run observer-log --path logs/observer_decisions.jsonl --limit 50 --summary
```

The summary report includes:

- total decisions
- Fusion decisions
- default observer decisions
- average score
- task type counts
- observer counts
- top reasons

The summary report is read-only and does not expose request text or metadata.

## Dry-run smoke

Use the dry-run smoke script to exercise the local observer gate loop without
calling external services.

```bash
python smoke/observer_gate_dry_run.py
```

The dry-run flow is:

```text
TaskInput
-> evaluate_observer_gate(enabled=True, log_decision=True)
-> dry-run JSONL log
-> read_observer_decision_log()
-> format_observer_decision_log_entries()
```

The dry-run script writes to:

```text
logs/observer_decisions.dry_run.jsonl
```

It does not call external AI providers, Fusion, the provider registry, or task
execution.

## Decision report helper

The report helper lives at:

```text
core/observer_gate/report.py
```

It summarizes already-read observer decision entries into aggregate metrics.
It is intended for CLI, smoke, and future reporting integrations.

## Fusion policy

Fusion is treated as a special observer, not as the core engine.

Use Fusion-style review for:

- high-risk work
- high-uncertainty work
- public releases
- paid deliverables
- legal, security, or financial review
- tasks with high failure cost

Do not use it for:

- trivial rewrites
- memo cleanup
- X post generation
- draft-only work
- small code edits
- low-cost reversible work

## Files

```text
docs/architecture/multi_observer_architecture.md
specs/multi_observer_v0.yaml
core/observer_gate/models.py
core/observer_gate/classifier.py
core/observer_gate/scorer.py
core/observer_gate/router.py
core/observer_gate/policy_loader.py
core/observer_gate/entrypoint.py
core/observer_gate/logger.py
core/observer_gate/log_reader.py
core/observer_gate/report.py
api/models/observer_gate.py
api/routes.py
cli/entrypoints.py
smoke/observer_gate_dry_run.py
```

## Operational checklist

Before enabling in a real workflow:

1. Confirm the policy file exists.
2. Confirm `RTS_AGE_OBSERVER_GATE_ENABLED=true` is intentional.
3. Confirm logging is off unless needed.
4. If logging is enabled, confirm the log path is acceptable.
5. Confirm no request text is written to the log.
6. Inspect decisions with `uv run observer-log`.
7. Inspect aggregate behavior with `uv run observer-log --summary`.
8. Use `python smoke/observer_gate_dry_run.py` before wiring real adapters.
9. Keep external provider or Fusion calls behind a separate explicit adapter.

## Future work

Recommended next steps:

1. Add a real provider adapter only behind explicit configuration.
2. Add log rotation or retention policy if logs grow.
3. Add Markdown export for observer decision reports.
4. Keep all future provider additions adapter-based, not hardcoded.
