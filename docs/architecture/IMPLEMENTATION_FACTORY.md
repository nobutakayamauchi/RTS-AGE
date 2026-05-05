# IMPLEMENTATION FACTORY MODEL

RTS-AGE defines a proposal-first implementation flow for RTS integration work.

## Processing Flow

data / work order / signal input
  -> classify
  -> generate
  -> validate
  -> package as patch proposal
  -> route to canonical repo
  -> produce RTS record proposal

## Canonical Repo Routing

- RTS records/templates -> RTS
- skill manifests -> RTS-Skills-
- pack manifests -> RTS-MCP-Packs
- drive manifests -> RTS-Hermes-Drive
- talent entries/scorecards -> RTS-Talent-Registry
- feed entries/digests -> RTS-Signal-Feeds
- sandbox tests -> codex-connector-test

## Operating Constraints

- Default output mode is proposal-only (drafts, reports, bundles, dry-runs).
- Direct repository mutation is disabled by default.
- External side-effect operations require explicit human approval outside this repository.
