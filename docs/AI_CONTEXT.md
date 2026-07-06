# RTS-AGE AI Context

This document defines how AI agents should treat this repository.

## Repository Identity

RTS-AGE means RTS Agentic Gateway & Execution Lab.

It receives data, work orders, external signals, and operator instructions, then produces reviewable implementation artifacts.

It is not RTS core.

It is not the canonical home of RTS-Skills, RTS-MCP-Packs, RTS-Hermes-Drive, RTS-Talent-Registry, RTS-Signal-Feeds, or RTS-Design-Research.

## Default Operating Mode

Default mode: proposal-first.

Agents should produce reviewable artifacts before performing irreversible changes.

Preferred outputs:

- implementation plan
- patch proposal
- dry-run result
- validation report
- risk report
- RTS record proposal
- small reviewable pull request

## Hard Guardrails

Do not perform these actions unless explicitly requested by the operator in the current task:

- direct push to canonical RTS repositories
- live publish
- live trading
- external API mutation
- external account mutation
- credential creation or storage
- dependency replacement
- architecture rewrite
- schema rewrite
- manifest format rewrite
- log format rewrite
- broad refactor
- migration across repositories

If any of these appear necessary, stop and write a proposal instead of implementing.

## Scope Rules

For normal tasks, prefer the smallest safe diff.

Do not improve unrelated files.

Do not generalize the architecture for hypothetical users.

Do not convert this repository into a generic beginner-friendly automation platform.

If usability improvements are needed, add wrappers, examples, or documentation. Do not weaken the core gateway boundaries.

## Unknown Handling

When an instruction is ambiguous, do not silently guess.

Classify the ambiguity as one of:

- product unknown
- architecture unknown
- data unknown
- runtime unknown
- security unknown
- operator intent unknown

Then either proceed with a safe minimal assumption or stop with a short blocking question/proposal.

## Relationship to Other Repositories

- RTS: canonical decision reconstructability protocol and structural ledger.
- RTS-Minimal-Runtime: smallest reference runtime for reconstructable RTS flow.
- RTS-AGE: gateway and execution lab for generating proposals and validation artifacts.
- RTS-minicompany: money-line MVP for solo business operations.
- RTS-Skills: reusable operational skills.
- RTS-MCP-Packs: connector pack definitions.
- RTS-Hermes-Drive: orchestration bridge.
- RTS-Design-Research: design research to RTS-compatible decision records.

Do not move responsibilities across repositories without a separate migration proposal.
