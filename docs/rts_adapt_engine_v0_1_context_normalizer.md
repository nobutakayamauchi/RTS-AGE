# RTS Adapt Engine v0.1 Context Normalizer

## Purpose

This PR adds the first context normalization layer for RTS Adapt Engine v0.1.

It transforms parsed `inputs/daily_input.md` sections into:

```text
outputs/context_summary.md
```

This is still not a platform draft generation PR.

---

## Added Module

```text
src/normalizer.py
```

---

## Updated Command

```bash
python src/generate.py
```

The command now:

```text
reads inputs/daily_input.md
parses supported Markdown sections
builds a deterministic context summary
writes outputs/context_summary.md
prints section coverage and safety status
```

---

## Generated File

```text
outputs/context_summary.md
```

The context summary includes:

```text
input coverage
current situation
completed work
blockers
next actions
source material
reference URLs
core message
do-not-say boundary
requested outputs
tone
offer
call to action
LINE intent
free resource
consultation path
cautions
preamble, when present
unknown sections, when present
safety boundary
```

---

## Safety Boundary

This PR may:

```text
read local Markdown
parse sections
write a local context summary
print local status
```

This PR must not:

```text
generate X posts
generate note drafts
generate LINE messages
generate video scripts
call model APIs
call external APIs
execute connectors
publish content
send messages
read credentials
write credentials
```

---

## Expected Status Output

A successful command should include:

```text
RTS Adapt Engine v0.1 context normalizer ready.
context_summary_path=outputs/context_summary.md
present_sections=<count>
missing_sections=<count>
unknown_sections=<count>
draft_generation_not_implemented=true
external_api_calls=false
publishing=false
```

---

## Tests

The tests cover:

```text
context summary generation
input coverage reporting
safety boundary reporting
unknown section preservation
preamble preservation
command smoke output
context_summary.md file creation
```

---

## Next Implementation Step

After this PR is reviewed and merged, continue with:

```text
PR-04: Add draft output generators
```

That next PR should generate local draft outputs for X, note, LINE, and video script while preserving the no-external-API and no-publishing boundary.
