# AGE Planning Output Contract

## Purpose

This document defines the required planning outputs AGE must produce before RTS Adapt Engine implementation begins.

AGE must not jump from a broad product specification directly into code. It must first produce bounded, reviewable planning artifacts that can be inspected by a human and then converted into small implementation PRs.

Source inputs:

```text
docs/age_builder_adapt_engine_input_target.md
docs/specs/rts_adapt_engine_v0_2_fixed.md
docs/specs/rts_adapt_engine_v0_1_mvp_scope.md
```

---

## Planning Run Goal

Given the fixed Adapt Engine specification and the v0.1 MVP scope, AGE must produce a complete implementation planning package.

The output package must answer:

```text
What are we building first?
What are we explicitly not building yet?
What files should exist?
What PRs should be created?
How do we smoke test the result?
Where must a human review before execution?
What did AGE decide and defer?
```

---

## Required Output Files

AGE must produce these files before any implementation PRs are started:

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

## 1. Spec Intake Summary Contract

Output file:

```text
outputs/age/spec_intake_summary.md
```

Required sections:

```markdown
# Spec Intake Summary

## Source Documents
## Product Goal
## Upper-Bound Scope
## MVP Scope Source
## Key Constraints
## Safety Boundaries
## Human Approval Boundary
## Next Planning Step
```

Minimum requirements:

- list all source documents
- identify that the v0.2 spec is an upper-bound document
- identify that v0.1 is the active implementation target
- preserve the human approval boundary
- state that no external APIs should be used during v0.1

---

## 2. v0.1 Scope Summary Contract

Output file:

```text
outputs/age/v0_1_scope_summary.md
```

Required sections:

```markdown
# RTS Adapt Engine v0.1 Scope Summary

## Build Now
## Do Not Build Yet
## Required Input
## Required Outputs
## Required Local Modules
## Required Smoke Path
## Acceptance Criteria
## Open Questions
```

Minimum requirements:

- include `inputs/daily_input.md` as the only required input
- include the required Markdown outputs
- include `logs/execution_log.jsonl`
- explicitly exclude external APIs, connectors, DB, Web UI, auth, billing, and auto-publishing
- keep all generated artifacts as human-reviewable drafts

---

## 3. PR Plan Contract

Output file:

```text
outputs/age/pr_plan.md
```

The PR plan must split implementation into small reviewable steps.

Required top-level sections:

```markdown
# RTS Adapt Engine v0.1 PR Plan

## PR-01: Add project scaffold
## PR-02: Add input reader and section parser
## PR-03: Add context normalizer
## PR-04: Add draft output generators
## PR-05: Add review checklist generator
## PR-06: Add execution logger and summary
## PR-07: Add smoke test
## Deferred PRs
## Review Notes
```

Each PR section must include:

```markdown
### Goal
### Files to add or update
### Acceptance criteria
### Tests or smoke checks
### Non-goals
### Risk notes
```

Minimum requirements:

- each PR must be independently reviewable
- each PR must have explicit non-goals
- no PR may introduce external API calls in v0.1
- no PR may introduce automatic publishing in v0.1
- PR-07 must verify the full local path

---

## 4. Scaffold Plan Contract

Output file:

```text
outputs/age/scaffold_plan.md
```

Required sections:

```markdown
# RTS Adapt Engine v0.1 Scaffold Plan

## Directory Tree
## Input Files
## Output Files
## Source Modules
## Test Files
## Log Files
## Files Deferred
## Notes
```

Minimum directory target:

```text
rts-adapt-engine/
├─ inputs/
│  └─ daily_input.md
├─ outputs/
│  ├─ context_summary.md
│  ├─ x_posts.md
│  ├─ note_draft.md
│  ├─ line_message.md
│  ├─ video_script.md
│  ├─ review_checklist.md
│  └─ summary.md
├─ logs/
│  └─ execution_log.jsonl
├─ src/
│  ├─ generate.py
│  ├─ normalizer.py
│  ├─ generators/
│  ├─ review/
│  └─ logging/
├─ tests/
├─ README.md
└─ pyproject.toml
```

The exact package structure may be refined, but the local input -> output -> log path must remain stable.

---

## 5. Smoke Test Plan Contract

Output file:

```text
outputs/age/smoke_test_plan.md
```

Required sections:

```markdown
# RTS Adapt Engine v0.1 Smoke Test Plan

## Command
## Test Input
## Expected Generated Files
## Required Assertions
## Safety Assertions
## Failure Conditions
```

Required command:

```bash
python src/generate.py
```

Required assertions:

- input file exists
- known sections are parsed
- required output files are generated
- review checklist is generated
- execution log is appended
- no external API is called
- no automatic publishing happens

---

## 6. Review Checklist Contract

Output file:

```text
outputs/age/review_checklist.md
```

Required sections:

```markdown
# AGE Planning Review Checklist

## Scope Review
## Safety Review
## File Plan Review
## PR Plan Review
## Smoke Test Review
## Human Approval Review
## Blockers
## Approval Decision
```

Minimum checklist items:

- Does the plan only cover v0.1?
- Are v0.1.5+ features deferred?
- Are external APIs excluded?
- Are credentials excluded?
- Are all generated outputs draft-only?
- Is human review still the final gate?
- Are the PRs small enough to review?
- Is there a smoke test path?

---

## 7. Execution Log Contract

Output file:

```text
logs/age_builder_execution_log.jsonl
```

Each line must be valid JSONL.

Minimum fields:

```json
{
  "run_id": "age-plan-YYYYMMDD-HHMMSS",
  "input_documents": [],
  "active_scope": "rts-adapt-engine-v0.1",
  "generated_files": [],
  "deferred_features": [],
  "safety_boundary": "planning_only_no_external_api_no_auto_publish",
  "review_required": true,
  "next_action": "human_review"
}
```

Requirements:

- do not log credentials
- do not log private tokens
- record that the run is planning-only
- record all generated planning artifacts
- record the next action for the human

---

## Required Planning-Only Boundary

The planning run must not:

```text
write implementation code
call external APIs
publish content
send messages
create credentials
store tokens
run production connectors
```

AGE may only create planning artifacts and logs for human review.

---

## Completion Criteria

This planning output contract is satisfied when AGE can produce:

- one spec intake summary
- one v0.1 scope summary
- one PR plan
- one scaffold plan
- one smoke test plan
- one planning review checklist
- one JSONL execution log entry

The planning package must be sufficient for a human to decide whether to start the first implementation PR.

---

## Next Step After This Contract

After this contract is merged, AGE can perform a planning dry-run against the fixed Adapt Engine inputs.

That dry-run should not produce implementation code yet. It should produce the planning package described here.
