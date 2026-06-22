# RTS Adapt Engine v0.1 Scaffold Plan

## Directory Tree

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
│  ├─ input_reader.py
│  ├─ section_parser.py
│  ├─ normalizer.py
│  ├─ summary.py
│  ├─ generators/
│  │  ├─ x_posts.py
│  │  ├─ note_draft.py
│  │  ├─ line_message.py
│  │  └─ video_script.py
│  ├─ review/
│  │  └─ checklist.py
│  └─ logging/
│     └─ execution_logger.py
├─ tests/
│  ├─ test_section_parser.py
│  ├─ test_normalizer.py
│  ├─ test_generators.py
│  ├─ test_review_checklist.py
│  ├─ test_execution_logger.py
│  └─ test_v0_1_smoke.py
├─ sample_inputs/
│  └─ daily_input.md
├─ README.md
└─ pyproject.toml
```

## Input Files

```text
inputs/daily_input.md
sample_inputs/daily_input.md
```

## Output Files

```text
outputs/context_summary.md
outputs/x_posts.md
outputs/note_draft.md
outputs/line_message.md
outputs/video_script.md
outputs/review_checklist.md
outputs/summary.md
```

## Source Modules

```text
src/generate.py
src/input_reader.py
src/section_parser.py
src/normalizer.py
src/summary.py
src/generators/x_posts.py
src/generators/note_draft.py
src/generators/line_message.py
src/generators/video_script.py
src/review/checklist.py
src/logging/execution_logger.py
```

## Test Files

```text
tests/test_section_parser.py
tests/test_normalizer.py
tests/test_generators.py
tests/test_review_checklist.py
tests/test_execution_logger.py
tests/test_v0_1_smoke.py
```

## Log Files

```text
logs/execution_log.jsonl
```

## Files Deferred

```text
outputs/line_flow/
configs/platforms.yaml
configs/publishing_policy.yaml
configs/api_budget.yaml
logs/approval_log.jsonl
logs/api_call_log.jsonl
rts/sessions/
rts/manifests/
connectors/
web/
auth/
billing/
```

## Notes

The v0.1 scaffold should preserve the local input -> output -> log path.

The implementation may choose to keep the package inside the existing repository instead of a nested `rts-adapt-engine/` directory, but the required file roles should remain stable.
