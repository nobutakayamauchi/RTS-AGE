# RTS Adapt Engine v0.1 Scope Summary

## Build Now

Build the smallest local generation loop:

```text
inputs/daily_input.md
-> python src/generate.py
-> outputs/*.md
-> logs/execution_log.jsonl
```

v0.1 should generate these files:

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

## Do Not Build Yet

Do not implement:

```text
LINE API connector
X API connector
Threads connector
Bluesky connector
Mastodon connector
note connector
Google Drive connector
Gmail connector
DB
Web UI
authentication
billing
auto-publishing
auto-replying
production credential handling
```

## Required Input

```text
inputs/daily_input.md
```

The input reader should tolerate missing sections.

## Required Outputs

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

## Required Local Modules

```text
input reader
section parser
context normalizer
draft output generators
review checklist generator
summary generator
execution logger
```

## Required Smoke Path

```bash
python src/generate.py
```

Required smoke assertions:

- input file exists
- known sections are parsed
- all required output files are generated
- review checklist is generated
- execution log is appended
- no external API is called
- no automatic publishing happens

## Acceptance Criteria

v0.1 is complete when:

- `inputs/daily_input.md` can be read locally
- all required Markdown output files are generated
- at least 3 X post drafts are generated
- a note draft is generated
- a LINE message draft is generated
- a video script draft is generated
- a review checklist is generated
- a JSONL execution log entry is written
- all outputs remain human-reviewable drafts

## Open Questions

- Should the v0.1 package live in a nested `rts-adapt-engine/` directory or within the current repository's root package structure?
- Should generated output files be committed as samples or ignored after smoke tests?
- Should the first generator use deterministic templates only, or allow pluggable local prompt templates?
