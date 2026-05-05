# POSITION: RTS-AGE (RTS Agentic Gateway & Execution Lab)

## Role
RTS-AGE is an **implementation lab** for RTS ecosystem integration work.

This repository is intended to:
- Read canonical RTS artifacts (manifest / registry / drive / record template) from their upstream canonical repositories.
- Validate structural and referential consistency across those artifacts.
- Run dry-run workflows to test orchestration and gateway behavior.
- Execute adapter experiments that improve interoperability while keeping upstream contracts intact.

## Non-Role (Boundary)
RTS-AGE is **not** the canonical source of:
- RTS-Skills
- MCP-Packs
- Hermes
- Talent
- Signal

Canonical definitions must remain upstream. This repo may reference or consume them, but must not duplicate them as source-of-truth content.

## Operational Guardrails
- Keep existing `free-claude-code` implementation code unchanged unless explicitly requested for a separate task.
- Do not modify `LICENSE`.
- Do not introduce API keys or runtime credentials into version-controlled files.
- Do not add live execution pathways for SNS publish or trading execution.
- Keep validation, dry-run, and adapter work scoped to lab-safe experimentation.

## Upstream Attribution
See `UPSTREAM.md` for attribution and lineage.
