# AGENTIC DIRECTIVE

> `AGENTS.md` and `CLAUDE.md` must contain the same operational directives.

## Repository role
RTS-AGE is the **RTS Agentic Gateway & Execution Lab**: an implementation lab/factory for validation reports, dry-runs, patch proposals, adapter prototypes, and RTS record proposals.

It is **not** the canonical source for RTS records, RTS-Skills, RTS-MCP-Packs, RTS-Hermes-Drive, RTS-Talent-Registry, or RTS-Signal-Feeds. Canonical definitions remain in their designated repositories.

## Current mode
**RESCUE / GATEWAY STABILIZATION / PROPOSAL-FIRST**

The goal is to make the existing repository safe to resume, not to broaden or redesign it.

Allowed by default:
- read/inspect/validate
- documentation
- local tests
- dry-run outputs
- validation reports
- patch bundles/proposals
- adapter prototypes
- RTS record proposals

Forbidden without explicit operator approval:
- direct push/mutation of canonical repositories
- live publishing
- live trading/order execution
- external API/account mutation
- credential creation/storage
- dependency replacement
- broad refactor or architecture/schema rewrite
- cross-repository migration
- automatic deployment

## Canonical load order
Before implementation work, read in this order:
1. `docs/STATUS.md`
2. `docs/AI_CONTEXT.md`
3. `docs/NEXT.md`
4. only the code/tests directly relevant to the task
5. `README.md` **only when repository/upstream background is actually needed**

### README context guard
The root README contains substantial upstream **Free Claude Code** documentation. Do **not** ingest that large upstream body by default. For ordinary RTS-AGE work, treat it as historical/provider background and use the RTS-AGE positioning/status documents above as the entrypoint. Read upstream/provider sections only when the task specifically concerns those internals.

## Context budget
- Do not scan the whole repository before acting.
- Start from the active responsibility and load the narrowest code/test path that can answer it.
- Do not recursively load other RTS repositories; follow only the canonical repo needed for the active boundary.
- Historical logs, generated artifacts, and upstream docs are reference-only unless diagnosis/reconstruction requires them.
- If the task can be completed from STATUS + AI_CONTEXT + NEXT + targeted code/tests, stop loading context there.

## Source of truth
Current status/boundary documents and verified code/tests outrank stale README/upstream prose. Preserve explicit `UNKNOWN` and `CONFLICT`; do not convert missing proof into success.

## Change scope
Use strict minimal-patch mode. Before editing, identify intended files, assumptions, risks, and stop conditions. Do not improve unrelated files.

## Coding/validation
- Use `uv` and Python 3.14 as defined by the repository environment.
- Prefer `uv run` over global Python.
- Do not add type-ignore escapes; fix underlying type issues.
- Add/update tests for behavior changes.
- Run the relevant checks; when the full suite applies, use: `uv run ruff format`, `uv run ruff check`, `uv run ty check`, `uv run pytest`.
- Failing required checks block completion claims.

## Stop conditions
Stop and report instead of guessing when:
- status/AI context/task instructions conflict;
- canonical ownership is unclear;
- the task crosses a forbidden external/destructive boundary;
- required runtime/deployment evidence is missing;
- the requested work would broaden RESCUE mode without an explicit decision.

## Completion report
Report changed files, logic altered, verification performed, residual risks, and the next safe task.