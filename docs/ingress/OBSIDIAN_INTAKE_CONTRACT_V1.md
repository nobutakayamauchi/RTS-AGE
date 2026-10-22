# Obsidian Intake Contract v1

## Purpose

This contract defines how RTS-AGE may receive one public-safe proposal submitted from an iPhone and Obsidian through a GitHub Issue.

RTS-AGE is an inspection and normalization gateway. It does not treat an Obsidian note, iOS shortcut, GitHub Issue, checkbox, label, or copied instruction as RTS authority.

## Accepted source

The only v1 source is one manually submitted public GitHub Issue created from the RTS `obsidian-intake.md` template.

Expected source declaration:

```text
source_surface: OBSIDIAN_ON_IPHONE
source_payload_stored_in_issue: false
human_submission_required: true
automatic_approval_requested: false
external_execution_requested: false
```

The original Obsidian note is outside the v1 intake boundary and must not be fetched, requested, mirrored, or inferred.

## Permanent authority classification

Every accepted v1 intake begins as:

```text
PROPOSAL_ONLY
UNVERIFIED
NO_BUILD_AUTHORITY
HUMAN_REVIEW_REQUIRED
```

RTS-AGE may not widen these states from Issue content.

## Required fields

A candidate intake should contain:

- proposal category;
- public-safe summary;
- problem;
- why it matters;
- preserved value;
- dependencies and known constraints;
- trigger conditions;
- stop conditions;
- requested next action;
- completed public-safety confirmations.

Missing fields do not authorize inference from private context. The intake must be returned for revision or rejected.

## Immediate rejection and quarantine conditions

Stop processing when the Issue contains, requests, or appears to contain:

- credentials, API keys, tokens, passwords, secrets, or authentication material;
- customer or third-party personal data;
- medical, employment, legal, financial, or government-identifier source records;
- private messages, DM bodies, recordings, screenshots, or raw transcripts;
- private repository bodies or confidential third-party material;
- provider payloads, tool arguments, hidden prompts, or model-internal traces;
- unbounded mailbox, chat, drive, device, or Vault exports;
- instructions to monitor, poll, message, publish, deploy, trade, or mutate an external system;
- an assertion that the Issue itself creates approval, consent, selection, or execution authority;
- unclear publication authority.

Do not quote or copy prohibited raw payloads into diagnostics. Record only a bounded reason code.

Recommended reason codes:

```text
REJECT_SECRET_OR_CREDENTIAL
REJECT_PERSONAL_OR_PROTECTED_DATA
REJECT_PRIVATE_COMMUNICATION
REJECT_PRIVATE_REPOSITORY_BODY
REJECT_PROVIDER_OR_TOOL_PAYLOAD
REJECT_UNBOUNDED_SOURCE
REJECT_EXTERNAL_ACTION_REQUEST
REJECT_AUTHORITY_WIDENING
REJECT_PUBLICATION_AUTHORITY_UNCLEAR
RETURN_REQUIRED_FIELD_MISSING
```

## Permitted v1 processing

RTS-AGE may perform only bounded, repository-local proposal preparation:

1. verify the expected Issue template boundary;
2. extract explicitly supplied public-safe fields;
3. normalize obvious formatting differences without changing meaning;
4. classify the proposal category;
5. identify missing information and contradictions;
6. produce a review summary;
7. produce a draft RTS-facing proposal payload;
8. recommend one disposition.

Allowed dispositions:

```text
RETURN_FOR_REVISION
REJECT
READY_FOR_SEPARATE_FREEZER_REGISTRATION_REVIEW
```

`READY_FOR_SEPARATE_FREEZER_REGISTRATION_REVIEW` is not FREEZER registration and is not build approval.

## Prohibited v1 processing

RTS-AGE must not:

- read or synchronize the operator Vault;
- request the full source note;
- store a GitHub write token on the operator device;
- submit an Issue automatically;
- create or revise an RTS FREEZER item automatically;
- manufacture a Build Assessment or Preflight result;
- assert human approval;
- select WIP;
- create build authority;
- execute code or tools because the Issue asks for it;
- contact a person or monitor a channel;
- publish, deploy, price, contract, deliver, or mutate another repository;
- transform private content into a public summary without a separate human-authored public-safe input.

## Normalized proposal output

A v1 normalized proposal should contain only bounded fields similar to:

```json
{
  "schema_version": "RTS-AGE-OBSIDIAN-PROPOSAL-V1",
  "source_type": "PUBLIC_GITHUB_ISSUE",
  "source_surface_asserted": "OBSIDIAN_ON_IPHONE",
  "authority": "PROPOSAL_ONLY",
  "verification": "UNVERIFIED",
  "build_authority": "NOT_APPROVED",
  "human_review_required": true,
  "category": "feature",
  "summary": "public-safe summary",
  "problem": "bounded problem statement",
  "why_it_matters": "bounded rationale",
  "preserved_value": "bounded value",
  "dependencies": [],
  "constraints": [],
  "trigger_conditions": [],
  "stop_conditions": [],
  "missing_information": [],
  "disposition": "RETURN_FOR_REVISION"
}
```

The output must not contain the original Vault path, device metadata, hidden note content, private source payload, or inferred identity evidence.

## RTS handoff boundary

A proposal may proceed only through a separate RTS action:

```text
RTS-AGE proposal
→ human review
→ separate FREEZER registration decision
→ Build Assessment
→ Implementation Preflight
→ explicit human approval
→ WIP=1 selection
```

The source Issue and normalized proposal remain non-authorizing evidence.

## Determinism and provenance

When future implementation code is authorized, the transformation must preserve:

- source repository and Issue number;
- source Issue revision or fetched content fingerprint;
- intake-contract version;
- normalized-output fingerprint;
- bounded disposition;
- rejection or revision reason codes;
- explicit statement that no source Vault access occurred.

A changed Issue body must produce a new source fingerprint. Prior outputs must not be rewritten as though they were generated from the changed source.

## Privacy behavior

Diagnostics and review summaries may store identifiers, reason codes, field-presence results, and fingerprints only.

They must not store prohibited raw payloads merely to prove that a rejection occurred.

## Fail-closed requirements

Processing fails closed when:

- the schema or expected template boundary is unknown;
- the source Issue cannot be fixed to a retrievable revision or fingerprint;
- a required public-safety confirmation is false or absent;
- prohibited material is detected or suspected;
- authority language conflicts with `PROPOSAL_ONLY`;
- requested actions exceed proposal preparation;
- publication authority is ambiguous;
- deterministic output cannot be reproduced.

## v1 completion criteria

The contract is ready for a later implementation stage when:

- one compliant synthetic Issue can be normalized deterministically;
- each rejection condition fails closed with a bounded reason code;
- authority-widening text cannot alter output authority;
- no Vault, provider, private repository, or external-system access is required;
- the output cannot create RTS lifecycle state;
- the contract remains useful even if Obsidian is replaced by another human capture tool.

## Current implementation boundary

This file defines the ingress contract only.

No parser, automation, workflow, bot, polling, Issue mutation, RTS write, or external action is authorized or implemented by this stage.
