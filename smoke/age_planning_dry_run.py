"""Local dry-run generator for AGE planning output artifacts.

This module stays on the safe local path. It writes deterministic planning
artifacts for the RTS Adapt Engine v0.1 target and appends a JSONL execution
record. It does not call models, external APIs, connectors, or publishing paths.
"""

from __future__ import annotations

import json
from pathlib import Path

SOURCE_DOCUMENTS = (
    "docs/age_builder_adapt_engine_input_target.md",
    "docs/specs/rts_adapt_engine_v0_2_fixed.md",
    "docs/specs/rts_adapt_engine_v0_1_mvp_scope.md",
    "docs/specs/age_planning_output_contract.md",
)

AGE_OUTPUTS: dict[str, str] = {
    "outputs/age/spec_intake_summary.md": """# Spec Intake Summary

## Source Documents

- docs/age_builder_adapt_engine_input_target.md
- docs/specs/rts_adapt_engine_v0_2_fixed.md
- docs/specs/rts_adapt_engine_v0_1_mvp_scope.md
- docs/specs/age_planning_output_contract.md

## Product Goal

Generate a bounded RTS Adapt Engine v0.1 implementation plan.

## Upper-Bound Scope

The v0.2 fixed specification is the upper-bound product direction.

## MVP Scope Source

The active implementation scope is v0.1.

## Key Constraints

- local-only planning
- Markdown outputs first
- JSONL execution log
- human approval required

## Safety Boundaries

No external APIs, credentials, connectors, publishing, or sending.

## Human Approval Boundary

All outputs are drafts until reviewed by a human.

## Next Planning Step

Review the planning package and then start PR-01 if approved.
""",
    "outputs/age/v0_1_scope_summary.md": """# RTS Adapt Engine v0.1 Scope Summary

## Build Now

Build the local input -> output -> log path.

## Do Not Build Yet

Do not build external APIs, connectors, DB, Web UI, auth, billing, or publishing.

## Required Input

- inputs/daily_input.md

## Required Outputs

- outputs/context_summary.md
- outputs/x_posts.md
- outputs/note_draft.md
- outputs/line_message.md
- outputs/video_script.md
- outputs/review_checklist.md
- outputs/summary.md
- logs/execution_log.jsonl

## Required Local Modules

Input reader, section parser, normalizer, draft generators, review checklist,
summary generator, and execution logger.

## Required Smoke Path

python src/generate.py

## Acceptance Criteria

All required draft outputs and the execution log are generated locally.

## Open Questions

Decide final package layout before implementation PR-01.
""",
    "outputs/age/pr_plan.md": """# RTS Adapt Engine v0.1 PR Plan

## PR-01: Add project scaffold

### Goal

Add minimal local project structure.

### Files to add or update

inputs/daily_input.md, outputs/.gitkeep, logs/.gitkeep, src/generate.py,
README.md, and pyproject.toml.

### Acceptance criteria

The local placeholder command runs without external APIs.

### Tests or smoke checks

Run python src/generate.py.

### Non-goals

No generators, connectors, or API calls.

### Risk notes

Keep the scaffold small.

## PR-02: Add input reader and section parser

### Goal

Read and parse inputs/daily_input.md.

### Files to add or update

src/input_reader.py, src/section_parser.py, and tests/test_section_parser.py.

### Acceptance criteria

Known sections are parsed and missing sections are tolerated.

### Tests or smoke checks

Parser tests for complete and partial input.

### Non-goals

No output generation.

### Risk notes

Do not make missing sections fatal.

## PR-03: Add context normalizer

### Goal

Generate outputs/context_summary.md.

### Files to add or update

src/normalizer.py and tests/test_normalizer.py.

### Acceptance criteria

The summary includes current state, blockers, next actions, and constraints.

### Tests or smoke checks

Normalizer test and local smoke.

### Non-goals

No platform output generation.

### Risk notes

Do not invent missing context.

## Deferred PRs

LINE flow builder, platform adapters, approval log, RTS sessions, connectors,
external API wiring, and Web UI.

## Review Notes

Human review is required before implementation starts.
""",
    "outputs/age/scaffold_plan.md": """# RTS Adapt Engine v0.1 Scaffold Plan

## Directory Tree

```text
inputs/
outputs/
logs/
src/
tests/
sample_inputs/
```

## Input Files

- inputs/daily_input.md
- sample_inputs/daily_input.md

## Output Files

- outputs/context_summary.md
- outputs/x_posts.md
- outputs/note_draft.md
- outputs/line_message.md
- outputs/video_script.md
- outputs/review_checklist.md
- outputs/summary.md

## Source Modules

- src/generate.py
- src/input_reader.py
- src/section_parser.py
- src/normalizer.py
- src/summary.py

## Test Files

- tests/test_v0_1_smoke.py

## Log Files

- logs/execution_log.jsonl

## Files Deferred

Connectors, approval logs, RTS sessions, Web UI, auth, billing, and API config.

## Notes

Preserve the local input -> output -> log path.
""",
    "outputs/age/smoke_test_plan.md": """# RTS Adapt Engine v0.1 Smoke Test Plan

## Command

python src/generate.py

## Test Input

inputs/daily_input.md

## Expected Generated Files

context summary, X posts, note draft, LINE message, video script, review
checklist, summary, and execution log.

## Required Assertions

All required files are generated and the log is valid JSONL.

## Safety Assertions

No external APIs, no publishing, no credentials, and review is required.

## Failure Conditions

Missing outputs, invalid JSONL, or any required external connector.
""",
    "outputs/age/review_checklist.md": """# AGE Planning Review Checklist

## Scope Review

- [ ] Does the plan target only v0.1?
- [ ] Are future features deferred?

## Safety Review

- [ ] Are external APIs excluded?
- [ ] Are credentials excluded?
- [ ] Are outputs draft-only?

## File Plan Review

- [ ] Is the scaffold small?
- [ ] Is the input -> output -> log path preserved?

## PR Plan Review

- [ ] Are PRs small and independently reviewable?
- [ ] Does each PR have non-goals?

## Smoke Test Review

- [ ] Is there a local smoke path?
- [ ] Does it avoid external APIs?

## Human Approval Review

- [ ] Is human review required before implementation?

## Blockers

Decide final package layout before PR-01.

## Approval Decision

status: needs_human_review
""",
}

LOG_PATH = "logs/age_builder_execution_log.jsonl"


def _write_text(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _append_jsonl(root: Path, relative_path: str, record: dict[str, object]) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def run_age_planning_dry_run(output_root: str | Path = ".") -> str:
    """Write deterministic AGE planning artifacts and return a short report."""
    root = Path(output_root)
    generated_files = tuple(AGE_OUTPUTS)

    for relative_path, content in AGE_OUTPUTS.items():
        _write_text(root, relative_path, content)

    _append_jsonl(
        root,
        LOG_PATH,
        {
            "active_scope": "rts-adapt-engine-v0.1",
            "deferred_features": [
                "external_api_connectors",
                "auto_publishing",
                "db",
                "web_ui",
                "auth",
                "billing",
            ],
            "generated_files": list(generated_files),
            "input_documents": list(SOURCE_DOCUMENTS),
            "next_action": "human_review_then_start_pr_01_scaffold_if_approved",
            "review_required": True,
            "run_id": "age-plan-dry-run-local",
            "safety_boundary": "planning_only_no_external_api_no_auto_publish",
        },
    )

    return "\n".join(
        [
            "AGE planning dry-run complete.",
            f"generated_files={len(generated_files)}",
            f"log_path={LOG_PATH}",
            "review_required=true",
        ]
    )
