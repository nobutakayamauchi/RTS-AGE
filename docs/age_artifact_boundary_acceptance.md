# AGE Artifact Boundary Acceptance

## Acceptance Summary

This cleanup separates checked-in AGE dry-run samples from runtime-generated artifacts.

## Expected Repository Layout

```text
fixtures/age_planning_dry_run/   checked-in planning sample package
outputs/                         runtime-generated output only
logs/                            runtime-generated logs only
runs/                            optional runtime run directories
```

## Required Checks

- Fixture samples remain committed under `fixtures/age_planning_dry_run/`.
- Runtime outputs are ignored by `.gitignore` except `.gitkeep` placeholders.
- Runtime logs are ignored by `.gitignore` except `.gitkeep` placeholders.
- AGE dry-run tests can still write outputs under a temporary output root.
- No external APIs, connectors, credentials, publishing, or sending paths are introduced.

## Review Note

This is an optional route PR before returning to the main RTS Adapt Engine generator implementation path.

The next mainline implementation PR should resume with draft output generator work.
