# Spec Intake Summary

## Source Documents

```text
docs/age_builder_adapt_engine_input_target.md
docs/specs/rts_adapt_engine_v0_2_fixed.md
docs/specs/rts_adapt_engine_v0_1_mvp_scope.md
docs/specs/age_planning_output_contract.md
```

## Product Goal

RTS Adapt Engine converts messy human input into multiple reviewable Markdown draft outputs while preserving human approval as the final gate.

## Upper-Bound Scope

`docs/specs/rts_adapt_engine_v0_2_fixed.md` is an upper-bound product specification.

It includes future platform adapters, LINE flow building, approval logging, RTS integration, connector work, and API policies. These are not all part of the first implementation.

## MVP Scope Source

The active implementation target is v0.1 as defined in:

```text
docs/specs/rts_adapt_engine_v0_1_mvp_scope.md
```

## Key Constraints

- v0.1 must use `inputs/daily_input.md` as the only required input.
- v0.1 must generate Markdown outputs and a JSONL execution log.
- v0.1 must remain local-only.
- v0.1 must not call external APIs.
- v0.1 must not publish, broadcast, or send messages.

## Safety Boundaries

The first implementation must not include:

```text
external API calls
production credentials
auto-publishing
auto-replying
connectors
DB
Web UI
authentication
billing
```

## Human Approval Boundary

All outputs are generated drafts.

The system must preserve the distinction between:

```text
generated draft
human-reviewed draft
approved output
published output
```

v0.1 only reaches the generated draft stage.

## Next Planning Step

Generate the v0.1 scope summary, PR plan, scaffold plan, smoke test plan, review checklist, and execution log entry.
