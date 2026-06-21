# AGE Planning Dry-run Operations

## Purpose

This document explains how to run and review the AGE planning dry-run for the RTS Adapt Engine v0.1 preparation flow.

The dry-run exists to generate planning artifacts locally before implementation starts.

It is not an implementation run. It is not a publishing run. It is not a connector run.

---

## Command

Run from the repository root:

```bash
age-planning-dry-run
```

Optional output root:

```bash
age-planning-dry-run --output-root /tmp/age-planning-dry-run
```

The optional output root is useful when checking generated files without overwriting repository-local samples.

---

## Generated Files

The dry-run writes these files under the selected output root:

```text
outputs/age/spec_intake_summary.md
outputs/age/v0_1_scope_summary.md
outputs/age/pr_plan.md
outputs/age/scaffold_plan.md
outputs/age/smoke_test_plan.md
outputs/age/review_checklist.md
logs/age_builder_execution_log.jsonl
```

---

## Expected Console Output

A successful run should print a short report similar to:

```text
AGE planning dry-run complete.
generated_files=6
log_path=logs/age_builder_execution_log.jsonl
review_required=true
```

---

## Review Procedure

After running the dry-run, review the generated files in this order.

### 1. Spec intake summary

```text
outputs/age/spec_intake_summary.md
```

Check:

- source documents are listed
- v0.2 is treated as the upper-bound spec
- v0.1 is treated as the active implementation target
- human approval remains required
- no external API requirement appears

### 2. v0.1 scope summary

```text
outputs/age/v0_1_scope_summary.md
```

Check:

- build-now scope is local-only
- do-not-build-yet section excludes connectors and publishing
- required input is `inputs/daily_input.md`
- required outputs match the v0.1 scope document

### 3. PR plan

```text
outputs/age/pr_plan.md
```

Check:

- PRs are small enough to review
- each PR has non-goals
- no PR introduces external API calls
- no PR introduces automatic publishing
- PR-01 is only the scaffold

### 4. Scaffold plan

```text
outputs/age/scaffold_plan.md
```

Check:

- input, output, log, source, and test paths are separated
- deferred files are not included in v0.1 build-now scope
- the local input -> output -> log path is preserved

### 5. Smoke test plan

```text
outputs/age/smoke_test_plan.md
```

Check:

- the command is local
- required files are asserted
- JSONL log validation is included
- safety assertions exclude external APIs and credentials

### 6. Review checklist

```text
outputs/age/review_checklist.md
```

Check:

- scope review exists
- safety review exists
- file plan review exists
- PR plan review exists
- smoke test review exists
- human approval review exists

### 7. Execution log

```text
logs/age_builder_execution_log.jsonl
```

Check the latest line is valid JSONL and includes:

```text
active_scope=rts-adapt-engine-v0.1
review_required=true
safety_boundary=planning_only_no_external_api_no_auto_publish
next_action=human_review_then_start_pr_01_scaffold_if_approved
```

---

## Safety Boundary

The dry-run may:

```text
write local Markdown planning files
append a local JSONL planning log
print a local completion report
```

The dry-run must not:

```text
call model APIs
call external platform APIs
execute connectors
publish content
send messages
read credentials
write credentials
start background jobs
```

---

## Troubleshooting

### Command not found

Run through Python module/import path during local development or ensure the package scripts are installed in the active environment.

### Output files not found

Check the selected `--output-root`. Files are written relative to that root.

### JSONL log has multiple lines

This is expected. The log is append-only. Review the latest line.

### Existing sample files changed

Use `--output-root /tmp/age-planning-dry-run` when testing without touching repository-local samples.

---

## When This Dry-run Is Acceptable

The dry-run is acceptable when:

- all required planning files are generated
- the execution log is valid JSONL
- the safety boundary remains local-only
- review_required remains true
- the human can decide whether to start implementation PR-01

---

## Next Action

After reviewing the dry-run outputs, the next implementation step is:

```text
PR-01: Add project scaffold
```

That PR should remain scaffold-only and must not introduce generators, connectors, external APIs, or publishing.
