# Observer Gate Phase 2 MVP

## Status

Phase 2 MVP is complete.

This phase establishes a safe local provider boundary for Observer Gate without connecting a remote runtime.

## Completed path

```text
provider config loader
-> provider registry builder
-> local provider adapter
-> provider dry-run smoke
-> provider result report helper
```

## Capability map

| Capability | Status | Notes |
| --- | --- | --- |
| Provider adapter interface | Complete | Defines request, success result, error result, and adapter protocol. |
| Provider adapter registry | Complete | Stores adapters by provider ID. |
| Provider adapter config model | Complete | Stores enabled adapter configuration. |
| Provider config loader | Complete | Loads config from mapping or JSON file. |
| Provider registry builder | Complete | Builds enabled local adapters from config. |
| Local provider adapter | Complete | Deterministic local adapter for dry-runs. |
| Provider dry-run smoke | Complete | Exercises config -> registry -> local adapter -> report output. |
| Provider result report helper | Complete | Formats success and error results for safe display. |

## Safety boundary

Phase 2 MVP remains local-only.

It does not add:

- remote runtime calls
- model calls
- task execution
- automatic Observer Gate runtime wiring
- production provider credentials

The local provider adapter returns deterministic output and does not include prompt text in its output.

## Smoke command

```bash
uv run python smoke/observer_provider_dry_run.py
```

Expected high-level output:

```text
Observer provider dry-run complete.

status=ok | provider_id=local | observer_name=default | model=local-deterministic-v0 | output=local_observation task_id=smoke-provider-local task_type=memo_cleanup
```

## User-facing follow-up artifacts

The local provider boundary is now linked to user-facing operator materials:

```text
cli/entrypoints.py
docs/observer_provider_dry_run_operations.md
docs/observer_provider_dry_run_sample_output.txt
tests/cli/test_observer_provider_dry_run_cli.py
```

Use `docs/observer_provider_dry_run_sample_output.txt` as the stable reference output when comparing future CLI/report changes.

## Files added in Phase 2

```text
core/observer_gate/provider_adapter.py
core/observer_gate/provider_registry.py
core/observer_gate/provider_config.py
core/observer_gate/local_adapter.py
core/observer_gate/provider_config_loader.py
core/observer_gate/provider_registry_builder.py
core/observer_gate/provider_report.py
smoke/observer_provider_dry_run.py
```

## Next candidates

The next phase can connect this safe local boundary to AGE builder capability planning.

Recommended next steps:

1. Add an AGE builder capability target for RTS Adapt Engine.
2. Add a fixed RTS Adapt Engine spec document.
3. Add a v0.1 MVP scope extraction document.
4. Keep any remote adapter work behind explicit configuration and tests.
