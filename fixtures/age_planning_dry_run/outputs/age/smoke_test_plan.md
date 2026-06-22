# RTS Adapt Engine v0.1 Smoke Test Plan

## Command

```bash
python src/generate.py
```

## Test Input

Use a local Markdown input file:

```text
inputs/daily_input.md
```

The smoke input should include at least:

```text
# 今日の現状
# 今日やったこと
# 詰まっていること
# 次にやること
# 使いたいネタ
# 言ってはいけないこと
# 出力したい媒体
# 誘導したい行動
# 注意事項
```

## Expected Generated Files

```text
outputs/context_summary.md
outputs/x_posts.md
outputs/note_draft.md
outputs/line_message.md
outputs/video_script.md
outputs/review_checklist.md
outputs/summary.md
logs/execution_log.jsonl
```

## Required Assertions

The smoke test should verify:

- `inputs/daily_input.md` exists
- known sections are parsed
- missing sections do not crash the run
- `outputs/context_summary.md` is generated
- `outputs/x_posts.md` contains at least 3 draft posts
- `outputs/note_draft.md` is generated
- `outputs/line_message.md` is generated
- `outputs/video_script.md` is generated
- `outputs/review_checklist.md` is generated
- `outputs/summary.md` is generated
- `logs/execution_log.jsonl` receives one valid JSONL entry

## Safety Assertions

The smoke test should verify or preserve:

- no external API calls
- no publishing
- no sending messages
- no credentials required
- no tokens printed
- outputs remain draft-only
- human review is required

## Failure Conditions

The smoke test should fail if:

- a required output file is missing
- the execution log is invalid JSONL
- review checklist is not generated
- generated output claims to be published
- any external API connector is required for the local run
- credentials or tokens are required

## Expected Run Summary

The run should end with a human-readable summary similar to:

```text
RTS Adapt Engine v0.1 local generation complete.
Generated 7 draft outputs.
Review required before publishing or sending anything.
```
