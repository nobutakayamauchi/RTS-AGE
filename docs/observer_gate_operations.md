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
api/models/observer_gate.py
api/routes.py
cli/entrypoints.py
```

## Operational checklist

Before enabling in a real workflow:

1. Confirm the policy file exists.
2. Confirm `RTS_AGE_OBSERVER_GATE_ENABLED=true` is intentional.
3. Confirm logging is off unless needed.
4. If logging is enabled, confirm the log path is acceptable.
5. Confirm no request text is written to the log.
6. Inspect decisions with `uv run observer-log`.
7. Keep external provider or Fusion calls behind a separate explicit adapter.

## Future work

Recommended next steps:

1. Add a real provider adapter only behind explicit configuration.
2. Add a dry-run smoke test for the proposal endpoint.
3. Add log rotation or retention policy if logs grow.
4. Add a small report generator for observer decisions.
5. Keep all future provider additions adapter-based, not hardcoded.
