# RTS-AGE Status

Status: RESCUE / GATEWAY

RTS-AGE is the RTS Agentic Gateway & Execution Lab.

This repository is not the RTS core. It is a controlled implementation lab for receiving work orders, external signals, experimental data, and operator instructions, then producing implementation artifacts, validation reports, dry-run outputs, patch bundles, and RTS record proposals.

## Current Position

RTS-AGE should be treated as a proposal-first execution gateway.

Allowed by default:

- Read repository context
- Prepare implementation plans
- Produce patch proposals
- Produce validation reports
- Produce dry-run outputs
- Produce RTS record proposals
- Prepare local or reviewable artifacts

Prohibited by default:

- Direct push to canonical RTS repositories
- Live publish
- Live trading
- External system mutation
- Credential handling
- Automatic deployment
- Silent architecture rewrites
- Silent schema changes

## Rescue Reason

This repository currently contains both RTS-AGE positioning and Free Claude Code implementation material. That is useful, but it creates a risk that future AI agents will treat this repository as a generic Claude Code proxy project rather than the RTS execution gateway.

The rescue goal is not to complete or redesign the repository.

The rescue goal is to make the current role explicit enough that GPT, Fable, Codex, Claude Code, or future AI agents can safely continue work without confusing RTS core, RTS-AGE, and provider/proxy implementation details.

## Current Decision

Keep this repository.

Do not merge it into RTS core.

Do not expand it into a general automation platform until its gateway role, boundaries, and AI execution rules are stable.

## Minimum Alive Definition

This repository is considered Minimum Alive when:

1. Its role is clearly documented as RTS Agentic Gateway & Execution Lab.
2. It has an AI context document defining safe and unsafe agent behavior.
3. It has a NEXT document with the next smallest safe tasks.
4. It has AGENTS.md to constrain Codex and other coding agents.
5. No runtime behavior is changed by the rescue documentation itself.
