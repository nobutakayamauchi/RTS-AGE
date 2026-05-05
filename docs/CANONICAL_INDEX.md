# CANONICAL INDEX (Lab View)

This document tracks how RTS-AGE relates to upstream canonical repositories.

## Canonical Ownership
The following domains are canonical **outside** this repository:
- RTS-Skills
- MCP-Packs
- Hermes
- Talent
- Signal

RTS-AGE consumes these definitions for validation and experimentation only.

## Repository Positioning
- RTS-AGE is an implementation lab, not a canonical registry.
- Local changes here must not be interpreted as authoritative updates to canonical RTS specs.
- Any contract or schema evolution should be proposed to canonical upstream repositories first.

## Intended Lab Workloads
- Cross-artifact consistency checks (manifest/registry/drive/record template).
- Dry-run execution of gateway and adapter flows.
- Adapter compatibility experiments with strict non-production boundaries.

## Explicit Exclusions
- No canonical definition copies for RTS-Skills / MCP-Packs / Hermes / Talent / Signal.
- No embedded credentials.
- No live SNS publish or trading execution capabilities.
