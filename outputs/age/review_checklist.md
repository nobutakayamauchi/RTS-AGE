# AGE Planning Review Checklist

## Scope Review

- [ ] Does the planning package target only RTS Adapt Engine v0.1?
- [ ] Are v0.1.5, v0.2, v0.3, and v0.4+ features deferred?
- [ ] Is `inputs/daily_input.md` the only required input for v0.1?
- [ ] Are the required Markdown outputs listed?
- [ ] Is `logs/execution_log.jsonl` included?

## Safety Review

- [ ] Are external API calls excluded?
- [ ] Are production credentials excluded?
- [ ] Is auto-publishing excluded?
- [ ] Is auto-replying excluded?
- [ ] Are all outputs treated as drafts?
- [ ] Is human approval preserved as the final gate?

## File Plan Review

- [ ] Is the scaffold small enough for incremental implementation?
- [ ] Are inputs, outputs, logs, source files, and tests separated?
- [ ] Are deferred files clearly separated from v0.1 files?
- [ ] Does the scaffold preserve local input -> output -> log execution?

## PR Plan Review

- [ ] Is each proposed PR independently reviewable?
- [ ] Does each PR include explicit non-goals?
- [ ] Does each PR include acceptance criteria?
- [ ] Does each PR include a test or smoke check?
- [ ] Does no PR introduce external API calls in v0.1?

## Smoke Test Review

- [ ] Does the smoke test run with a local command?
- [ ] Does it verify required output files?
- [ ] Does it verify the execution log?
- [ ] Does it verify review checklist generation?
- [ ] Does it preserve the no-external-API boundary?

## Human Approval Review

- [ ] Does the planning package require human review before implementation?
- [ ] Does the implementation plan avoid automatic publishing?
- [ ] Does the plan preserve generated draft vs approved output distinction?

## Blockers

No blockers identified for planning-only output.

Implementation blockers to resolve before code begins:

- decide whether the implementation lives under a nested `rts-adapt-engine/` directory or the existing repository package layout
- decide whether sample generated outputs are committed or ignored after smoke tests
- decide whether generator output is purely deterministic templates for v0.1

## Approval Decision

```text
status: needs_human_review
recommended_next_action: review planning package, then start PR-01 scaffold if approved
```
