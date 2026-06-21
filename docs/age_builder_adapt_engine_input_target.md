# AGE Builder Adapt Engine Input Target

## Purpose

This document defines the minimum AGE builder capability target required before using AGE to build RTS Adapt Engine.

RTS Adapt Engine should not be built by giving an implementation agent the entire product specification at once. AGE must first be able to read the specification, extract the v0.1 scope, split the work into small implementation tasks, and produce reviewable plans before any code-generation-heavy workflow is attempted.

## Target outcome

AGE should be able to turn the fixed RTS Adapt Engine specification into a bounded v0.1 implementation plan.

The first successful AGE run should produce:

```text
v0.1 scope summary
v0.1 non-goals
file scaffold plan
PR-sized implementation plan
smoke test plan
review checklist
execution log entry
```

## Input specification

Primary input:

```text
docs/specs/rts_adapt_engine_v0_2_fixed.md
```

The source specification defines the full product direction. AGE must treat it as an upper-bound document, not as a request to implement every feature at once.

## Required AGE capabilities

### 1. Spec Intake

AGE must load a Markdown specification and preserve the source path in its execution record.

Expected output:

```text
outputs/age/spec_intake_summary.md
```

### 2. Scope Extractor

AGE must extract only the v0.1 implementation scope.

It must separate:

```text
v0.1 required items
v0.1.5 items
v0.2 items
v0.3+ items
explicit non-goals
```

Expected output:

```text
outputs/age/v0_1_scope_summary.md
```

### 3. Task Decomposer

AGE must split the v0.1 scope into small implementation tasks.

Each task should include:

```text
task id
title
input files
output files
acceptance criteria
non-goals
suggested tests
risk notes
```

Expected output:

```text
outputs/age/pr_plan.md
```

### 4. Scaffold Planner

AGE must propose a minimal file and directory structure before code is written.

The scaffold must favor Markdown and JSONL output first.

Expected output:

```text
outputs/age/scaffold_plan.md
```

### 5. Smoke Test Planner

AGE must define a minimal smoke test path for the v0.1 engine.

The first smoke path should be:

```text
inputs/daily_input.md
-> python src/generate.py
-> outputs/*.md
-> logs/execution_log.jsonl
```

Expected output:

```text
outputs/age/smoke_test_plan.md
```

### 6. Review Extractor Target

AGE must identify the human review points that any generated Adapt Engine plan needs.

Expected output:

```text
outputs/age/review_checklist.md
```

### 7. Execution Logger Target

AGE must record what it decided, what it deferred, and what the next step should be.

Expected output:

```text
logs/age_builder_execution_log.jsonl
```

## Required first-run behavior

When AGE is given the RTS Adapt Engine specification, it must not start by implementing every module.

It should first produce planning artifacts only:

```text
outputs/age/spec_intake_summary.md
outputs/age/v0_1_scope_summary.md
outputs/age/pr_plan.md
outputs/age/scaffold_plan.md
outputs/age/smoke_test_plan.md
outputs/age/review_checklist.md
logs/age_builder_execution_log.jsonl
```

## Explicit non-goals for the first AGE run

AGE must not generate or wire:

```text
LINE API connector
X API connector
Threads connector
Bluesky connector
Mastodon connector
note connector
Google Drive connector
Gmail connector
DB
Web UI
authentication
billing
auto-publishing
auto-replying
production credentials
```

## Acceptance criteria

The AGE builder capability target is satisfied when AGE can produce a bounded v0.1 implementation plan that includes:

- a v0.1-only scope summary
- a list of deferred features
- a PR-sized task plan
- a minimal scaffold plan
- a smoke test plan
- a review checklist
- an execution log entry

The plan must clearly preserve human approval as the final gate.

## Safety boundary

AGE may prepare implementation tasks, generate draft plans, and propose scaffolds.

AGE must not:

- publish content externally
- call external platform APIs
- bypass human approval
- store credentials in generated files
- erase the distinction between planning and execution

## Next step after this target

After this target is present, the next document should add the fixed RTS Adapt Engine specification and then a v0.1 MVP scope extraction document.
