# RTS Adapt Engine v0.1 Parser Acceptance

## Acceptance Criteria

The parser layer is acceptable when:

- `inputs/daily_input.md` is read as UTF-8 text
- supported Markdown headings are parsed into `sections`
- missing supported sections are tolerated
- unknown headings are preserved separately
- preamble text before the first heading is preserved
- the local command reports section counts
- the local command still does not generate draft outputs
- the local command still does not call external APIs
- the local command still does not publish content

## Explicit Non-goals

This PR must not implement:

- context normalization
- draft generation
- note generation
- X post generation
- LINE message generation
- video script generation
- execution logging
- external API calls
- connector execution
- publishing

## Next PR

After this PR is reviewed and merged, continue with:

```text
PR-03: Add context normalizer
```
