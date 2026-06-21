# RTS Adapt Engine v0.1 PR Plan

## PR-01: Add project scaffold

### Goal

Add the minimal directory and file structure for RTS Adapt Engine v0.1.

### Files to add or update

```text
inputs/daily_input.md
outputs/.gitkeep
logs/.gitkeep
src/generate.py
README.md
pyproject.toml
```

### Acceptance criteria

- project has a runnable local entry point placeholder
- sample input exists
- output and log directories exist
- no external APIs are wired

### Tests or smoke checks

- verify `python src/generate.py` can run and print a placeholder message

### Non-goals

- no generators
- no connectors
- no API calls

### Risk notes

Keep the scaffold boring. Do not over-design package structure yet.

## PR-02: Add input reader and section parser

### Goal

Read `inputs/daily_input.md` and extract known sections.

### Files to add or update

```text
src/input_reader.py
src/section_parser.py
tests/test_section_parser.py
```

### Acceptance criteria

- known sections are parsed
- missing sections are tolerated
- unknown content is preserved

### Tests or smoke checks

- parser unit test with complete input
- parser unit test with missing sections

### Non-goals

- no output generation
- no model calls

### Risk notes

Do not make missing sections fatal.

## PR-03: Add context normalizer

### Goal

Generate `outputs/context_summary.md` from parsed input.

### Files to add or update

```text
src/normalizer.py
src/generate.py
tests/test_normalizer.py
```

### Acceptance criteria

- context summary includes current situation, done items, blockers, next actions, constraints, and warnings
- output is deterministic enough for smoke tests

### Tests or smoke checks

- unit test for normalizer
- smoke run creates `outputs/context_summary.md`

### Non-goals

- no SNS draft generation yet

### Risk notes

The normalizer should summarize, not invent missing context.

## PR-04: Add draft output generators

### Goal

Generate draft outputs for X, note, LINE, and video.

### Files to add or update

```text
src/generators/x_posts.py
src/generators/note_draft.py
src/generators/line_message.py
src/generators/video_script.py
src/generate.py
tests/test_generators.py
```

### Acceptance criteria

- at least 3 X post drafts are generated
- note draft includes title, body, and CTA
- LINE message remains short and reviewable
- video script includes hook, main points, and closing

### Tests or smoke checks

- generator unit tests
- smoke run creates all four output files

### Non-goals

- no automatic posting
- no API calls
- no media generation

### Risk notes

All outputs must remain draft-only.

## PR-05: Add review checklist generator

### Goal

Generate `outputs/review_checklist.md`.

### Files to add or update

```text
src/review/checklist.py
src/generate.py
tests/test_review_checklist.py
```

### Acceptance criteria

- checklist includes factual uncertainty, overstatement, sensitive information, private information, unclear claims, harsh wording, publishing risk, and missing CTA

### Tests or smoke checks

- unit test for checklist generation
- smoke run creates review checklist

### Non-goals

- no automated approval
- no publishing decision automation

### Risk notes

The checklist should surface risks, not decide on behalf of the user.

## PR-06: Add execution logger and summary

### Goal

Generate `outputs/summary.md` and append `logs/execution_log.jsonl`.

### Files to add or update

```text
src/logging/execution_logger.py
src/summary.py
src/generate.py
tests/test_execution_logger.py
```

### Acceptance criteria

- summary includes generated files and next action
- execution log line is valid JSONL
- log records review_required=true

### Tests or smoke checks

- logger unit test
- smoke run appends log entry

### Non-goals

- no approval log yet
- no RTS session generation yet

### Risk notes

Do not log credentials, tokens, or private secrets.

## PR-07: Add smoke test

### Goal

Verify the full v0.1 local path.

### Files to add or update

```text
tests/test_v0_1_smoke.py
sample_inputs/daily_input.md
```

### Acceptance criteria

- smoke test runs the full local path
- all required files are generated
- no external API call path exists

### Tests or smoke checks

```bash
python src/generate.py
```

### Non-goals

- no connector integration
- no remote runtime

### Risk notes

The smoke path should remain deterministic.

## Deferred PRs

```text
LINE flow builder
Canonical Content Model
Platform adapters
Approval log
RTS session generation
Connectors
External API wiring
Web UI
```

## Review Notes

Human review is required before starting PR-01 implementation.

Review focus:

- v0.1 scope is narrow enough
- PRs are small enough
- no external API work leaked into v0.1
- generated outputs stay draft-only
