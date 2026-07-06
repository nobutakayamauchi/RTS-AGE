# RTS-AGE Next Actions

This document lists the next smallest safe actions for rescuing RTS-AGE.

Do not treat this as a full roadmap.

The immediate goal is Minimum Alive, not completion.

## Priority 1: Stabilize Identity

Confirm that RTS-AGE is consistently described as:

> RTS Agentic Gateway & Execution Lab

Required checks:

- README top positioning is clear.
- docs/STATUS.md is present.
- docs/AI_CONTEXT.md is present.
- AGENTS.md is present.

## Priority 2: Separate Gateway Role from Provider Implementation

The repository currently includes Free Claude Code provider/proxy material.

Next task:

- Identify which parts are gateway-level RTS-AGE responsibilities.
- Identify which parts are provider/proxy implementation details.
- Do not delete or rewrite implementation code during this pass.
- Produce a short separation proposal before moving files.

Suggested output:

```text
docs/proposals/provider_boundary_review.md
```

## Priority 3: Validate Safe Execution Commands

Identify the smallest non-mutating commands that prove the repository can be inspected safely.

Examples:

- list files
- run existing tests if available
- run lint/type check only if dependencies are already defined
- avoid installing or changing dependencies unless explicitly approved

Suggested output:

```text
docs/validation/minimum_alive_validation.md
```

## Priority 4: Prepare Codex Task Contracts

Before asking Codex to edit implementation code, prepare a task contract containing:

- target files
- files not to touch
- allowed changes
- prohibited changes
- validation command
- stop conditions

Suggested output:

```text
docs/contracts/task_contract_template.md
```

## Do Not Do Yet

Do not:

- refactor the repository
- move provider code
- change runtime behavior
- add external integrations
- add deployment flows
- add credential handling
- connect live accounts
- publish anything automatically

## Next Recommended Task

Create `docs/proposals/provider_boundary_review.md`.

That file should classify current repository responsibilities into:

1. RTS-AGE gateway responsibilities
2. Free Claude Code provider/proxy responsibilities
3. Shared support utilities
4. Unknown / needs review
