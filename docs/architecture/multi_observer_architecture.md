# Multi Observer Architecture

## Philosophy

AI is treated as an observer, not a single final authority.

The core system should decide when observation is needed, what kind of observer
is appropriate, and what evidence should be recorded. Individual AI providers
must remain replaceable implementation details.

## Purpose

- Multiple observation
- Provider independence
- Easy adapter addition
- Rollback-friendly design
- Deterministic routing metadata
- Safe default operation with no external calls

## Phase 1 status

Observer Gate Phase 1 is the safe foundation layer.

Phase 1 is complete when the repository has:

- policy-based classification and scoring
- a feature-flagged observer gate entrypoint
- an internal proposal endpoint
- optional JSONL decision logging
- log reading and CLI inspection
- aggregate decision reports
- Markdown report formatting
- dry-run smoke scripts
- provider adapter interface boundaries
- provider adapter registry boundaries
- provider adapter configuration models
- operations documentation

Phase 1 intentionally does not include live provider execution.

## Current flow

```text
User request
-> Task classification
-> Risk scoring
-> Observer Gate
-> ObserverDecision
-> optional JSONL logging
-> observer-log CLI
-> optional summary or Markdown report
```

## Provider boundary flow

```text
Observer Gate
-> ObserverProviderAdapterConfig
-> ObserverProviderRegistry
-> ObserverProviderAdapter interface
-> future provider implementation
```

The provider boundary exists so future adapters can be added without hardcoding
OpenAI, Claude, local models, Fusion, or any other provider into the gate core.

## Safety boundary

The current architecture does not:

- call external AI providers
- call Fusion
- create provider adapters from configuration
- execute tasks
- log request text
- treat provider output as final authority

The current architecture does:

- classify task type
- score routing risk
- select a proposed observer
- write safe routing metadata when logging is enabled
- summarize observer decisions
- expose typed boundaries for later provider adapters

## Fusion role

Fusion is a Special Observer, not the core engine.

Use Fusion-style review for:

- high-risk tasks
- high-uncertainty tasks
- public releases
- paid deliverables
- legal, security, or financial review
- tasks with high failure cost

Do not use Fusion-style review for:

- trivial rewrites
- memo cleanup
- X post generation
- draft-only work
- small code edits
- low-cost reversible work

## Future provider policy

New providers must be added through adapters and configuration, not hardcoded
into core logic.

Provider additions should follow this order:

1. adapter interface compliance
2. adapter registration
3. explicit configuration
4. dry-run validation
5. logging and report inspection
6. runtime wiring behind a separate feature flag

## Logging policy

Every routing decision should be JSONL-loggable with:

- reason
- score
- selected observer
- task type
- whether Fusion-style review was proposed

Logs must not include request text or sensitive metadata.

## Phase 2 candidates

The next phase should be incremental and still reversible:

1. local dummy adapter
2. adapter config loader
3. adapter registry construction from config
4. dry-run provider smoke
5. real provider adapter behind explicit opt-in configuration
6. Fusion special observer integration behind explicit opt-in configuration
