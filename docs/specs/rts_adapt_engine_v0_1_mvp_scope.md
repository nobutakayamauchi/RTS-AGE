# RTS Adapt Engine v0.1 MVP Scope Extraction

## Purpose

This document extracts the v0.1 MVP implementation scope from the fixed RTS Adapt Engine v0.2 product specification.

Source specification:

```text
docs/specs/rts_adapt_engine_v0_2_fixed.md
```

This scope document exists so AGE can plan implementation without treating the full product specification as an instruction to build every future feature at once.

---

## v0.1 MVP Goal

Build the smallest useful RTS Adapt Engine loop:

```text
inputs/daily_input.md
-> local generation command
-> multiple Markdown outputs
-> review checklist
-> execution log
```

The v0.1 MVP should prove that messy human input can be converted into useful draft artifacts while preserving a human approval boundary.

---

## v0.1 Required Input

### Primary input file

```text
inputs/daily_input.md
```

### Required sections

The MVP should support these sections when present:

```text
# 今日の現状
# 今日やったこと
# 詰まっていること
# 次にやること
# 使いたいネタ
# 参考URL
# 言いたいこと
# 言ってはいけないこと
# 出力したい媒体
# 今日の温度感
# 売りたい商品・サービス
# 誘導したい行動
# LINE公式でやりたいこと
# 無料配布物
# 相談導線
# 注意事項
```

The MVP may tolerate missing sections. Missing sections should be treated as empty or unknown, not as fatal errors.

---

## v0.1 Required Outputs

The MVP must generate these files:

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

---

## v0.1 Required Modules

### 1. Input Reader

Reads `inputs/daily_input.md` and preserves the raw input for the current run.

Minimum behavior:

- load Markdown input
- detect known sections
- tolerate missing sections
- return structured section data

### 2. Context Normalizer

Transforms raw sections into a compact summary.

Minimum output:

```text
outputs/context_summary.md
```

Must summarize:

- current situation
- done items
- blockers
- next actions
- usable content material
- constraints
- warnings

### 3. X Post Generator

Generates short post drafts from the input.

Minimum output:

```text
outputs/x_posts.md
```

Minimum acceptance:

- at least 3 draft posts
- no automatic posting
- each draft should be easy to review manually

### 4. Note Draft Generator

Generates a longer-form note-style draft.

Minimum output:

```text
outputs/note_draft.md
```

Minimum acceptance:

- title candidate
- body draft
- closing or CTA candidate
- manual review reminder

### 5. LINE Message Generator

Generates a LINE-style message draft.

Minimum output:

```text
outputs/line_message.md
```

Minimum acceptance:

- friendly short message
- clear next action
- no API send
- no automatic broadcast

### 6. Video Script Generator

Generates a short video or voice script draft.

Minimum output:

```text
outputs/video_script.md
```

Minimum acceptance:

- hook
- main points
- closing
- suggested title

### 7. Review Checklist Generator

Extracts human review points.

Minimum output:

```text
outputs/review_checklist.md
```

Must check for:

- factual uncertainty
- overstatement
- sensitive information
- private information
- unclear claims
- harsh wording
- publishing risk
- missing CTA

### 8. Summary Generator

Summarizes the run and next recommended action.

Minimum output:

```text
outputs/summary.md
```

### 9. Execution Logger

Writes a JSONL execution record.

Minimum output:

```text
logs/execution_log.jsonl
```

Minimum fields:

```json
{"run_id":"...","input_file":"inputs/daily_input.md","generated_files":[],"review_required":true,"next_action":"..."}
```

---

## v0.1 CLI Target

The first runnable command should be simple:

```bash
python src/generate.py
```

Future CLI names may be introduced later. v0.1 only needs one stable local path.

---

## v0.1 Directory Target

Minimal scaffold:

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
│  ├─ normalizer.py
│  ├─ generators/
│  ├─ review/
│  └─ logging/
├─ tests/
├─ README.md
└─ pyproject.toml
```

The exact Python package layout may be refined during implementation, but the MVP should preserve the input -> output -> log path.

---

## Explicit v0.1 Non-Goals

The following are out of scope for v0.1:

```text
LINE公式API連携
X自動投稿
Threads自動投稿
Bluesky自動投稿
Mastodon自動投稿
note自動投稿
動画生成
音声生成
DB
Web UI
認証
課金
自動返信
完全自動配信
外部API呼び出し
credential handling
production connector wiring
```

---

## Deferred to v0.1.5

LINE official account outer-box specification generation:

```text
outputs/line_flow/line_flow_spec.md
outputs/line_flow/rich_menu_spec.md
outputs/line_flow/auto_reply_spec.md
outputs/line_flow/welcome_message.md
outputs/line_flow/delivery_sequence.md
outputs/line_flow/consultation_flow.md
```

Still no API connection at v0.1.5.

---

## Deferred to v0.2

SNS and platform extensibility:

```text
Canonical Content Model
Platform Adapter
Capability Matrix
platforms.yaml
manual output for X / Threads / Bluesky / Mastodon / note / LINE
manual export formats
```

---

## Deferred to v0.3

Approval and RTS logging upgrades:

```text
approval_log.jsonl
approval status management
RTS session generation
decision_log generation
reconstruction notes
accepted / rejected output tracking
```

---

## Deferred to v0.4+

Connector implementation:

```text
Markdown Connector
GitHub Connector
Google Drive Connector
LINE manual setting export
note draft support
X posting support
Threads / Bluesky / Mastodon posting support
LINE API Connector
```

---

## Suggested PR Breakdown

AGE should split v0.1 implementation into small PRs.

### PR-A: Add project scaffold

Adds minimal directories, README, and empty sample input.

### PR-B: Add input reader and section parser

Reads `inputs/daily_input.md` and extracts known sections.

### PR-C: Add context normalizer

Generates `outputs/context_summary.md`.

### PR-D: Add draft output generators

Generates:

```text
outputs/x_posts.md
outputs/note_draft.md
outputs/line_message.md
outputs/video_script.md
```

### PR-E: Add review checklist generator

Generates `outputs/review_checklist.md`.

### PR-F: Add execution logger and summary

Generates:

```text
outputs/summary.md
logs/execution_log.jsonl
```

### PR-G: Add smoke test

Runs the full local path with sample input.

---

## v0.1 Smoke Test Target

The minimal smoke path should prove:

```text
input exists
known sections are parsed
required outputs are generated
review checklist is generated
execution log is appended
no external API is called
```

Expected command:

```bash
python src/generate.py
```

Expected generated files:

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

---

## Acceptance Criteria

v0.1 is complete when:

- `inputs/daily_input.md` can be read locally
- all required output files are generated
- at least 3 X post drafts are generated
- a note draft is generated
- a LINE message draft is generated
- a video script draft is generated
- a review checklist is generated
- an execution log entry is written
- no external APIs are called
- no automatic publishing happens
- all generated outputs remain human-reviewable drafts

---

## Human Approval Boundary

All v0.1 outputs are drafts.

The system must preserve the distinction between:

```text
generated draft
human-reviewed draft
approved output
published output
```

v0.1 only produces generated drafts and review checklists.

---

## AGE Planning Requirement

Before implementation starts, AGE should read this file and produce:

```text
outputs/age/v0_1_scope_summary.md
outputs/age/pr_plan.md
outputs/age/scaffold_plan.md
outputs/age/smoke_test_plan.md
outputs/age/review_checklist.md
logs/age_builder_execution_log.jsonl
```

This keeps RTS Adapt Engine implementation bounded, inspectable, and small enough for PR-by-PR work.
