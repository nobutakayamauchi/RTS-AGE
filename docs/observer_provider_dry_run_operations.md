# Observer Provider Dry-Run Operations

## Purpose

This guide describes how to run the local observer provider dry-run from the command line.

The command is intended to verify the completed Phase 2 local provider boundary:

```text
provider config loader
-> provider registry builder
-> local provider adapter
-> provider result report helper
-> CLI output
```

## Command

```bash
observer-provider-dry-run
```

For source-tree usage, the same flow can also be run directly:

```bash
uv run python smoke/observer_provider_dry_run.py
```

## Expected output shape

```text
Observer provider dry-run complete.

status=ok | provider_id=local | observer_name=default | model=local-deterministic-v0 | output=local_observation task_id=smoke-provider-local task_type=memo_cleanup
```

The exact formatting is intentionally plain text so it can be copied into logs, tickets, or reconstruction notes.

## Success criteria

A successful run should show:

- `Observer provider dry-run complete.`
- `status=ok`
- `provider_id=local`
- `observer_name=default`
- `model=local-deterministic-v0`
- `task_id=smoke-provider-local`
- `task_type=memo_cleanup`

## Safety expectations

This dry-run remains local-only.

It should not:

- call a remote runtime
- call a model
- execute a user task
- use production credentials
- wire Observer Gate into automatic runtime execution
- print the private prompt text

The dry-run uses deterministic local output so it can be executed safely in CI and local development.

## When to run

Run this command when:

- validating a fresh checkout
- checking packaging entry points
- confirming Phase 2 local provider wiring
- preparing a release note or demo
- debugging local adapter configuration changes

## Troubleshooting

### Command not found

Install or run through the project environment first.

```bash
uv sync
```

Then retry:

```bash
uv run observer-provider-dry-run
```

### Import error for `smoke`

Confirm that the `smoke` package is included in the wheel package list in `pyproject.toml`.

### Output does not include `status=ok`

Confirm that the smoke script still uses the provider result report helper.

### Prompt text appears in output

Treat this as a safety regression. The local dry-run output must not print the private prompt text.

## Related files

```text
cli/entrypoints.py
smoke/observer_provider_dry_run.py
core/observer_gate/provider_report.py
core/observer_gate/local_adapter.py
core/observer_gate/provider_registry_builder.py
core/observer_gate/provider_config_loader.py
tests/cli/test_observer_provider_dry_run_cli.py
tests/smoke/test_observer_provider_dry_run.py
```
