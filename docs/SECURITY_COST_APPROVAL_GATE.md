# RTS-AGE Security → Cost → Approval Gate

Status: GATEWAY CONTRACT / PROPOSAL-FIRST

RTS-AGE may prepare validation reports, dry-run outputs, patch proposals, and execution plans. It must not treat untrusted input, provider availability, or operator intent as permission to execute.

## Required gateway order

```text
UNTRUSTED REQUEST OR ARTIFACT
→ SECURITY VALIDATION
→ COST / CONSEQUENCE ESTIMATE
→ EXPLICIT SINGLE-USE OPERATOR APPROVAL
→ BOUNDED EXECUTION
→ OUTPUT VERIFICATION AND RTS RECORD PROPOSAL
```

## Security validation

The gateway must treat media, documents, archives, code, prompts, manifests, URLs, filenames, metadata, tool arguments, and environment references as untrusted.

Before provider routing or tool execution it must:

- enforce allowlisted schema and media types
- reject ambiguous or structurally invalid inputs
- apply hard size, duration, recursion, decompression, and runtime limits
- normalize paths and names
- prevent command, template, URL, and path injection
- disable unnecessary network access during inspection
- remove active content and nonessential metadata when practical
- produce a SECURITY_PASS bound to exact content hashes

Unknown or uninspectable input fails closed.

## Cost and consequence

Only a valid SECURITY_PASS may enter provider selection or cost estimation.

The estimate must include provider, account/project, model or compute class, transfer, storage, runtime, concurrency, retries, monetary ceiling, and external side effects.

There is no automatic paid fallback. Emergency overflow compute is manual and exceptional.

## Approval

Approval is one-shot, time-limited, hash-bound, provider-bound, parameter-bound, and consequence-bound. Any change requires a new gate cycle.

## Execution enforcement

Execution adapters must reject:

- missing or expired approval
- security hash mismatch
- widened parameters
- additional inputs
- increased concurrency, retries, runtime, or resource size
- external mutation or publication not explicitly approved
- duplicate use of a consumed approval

## Output

RTS-AGE records the validation evidence and generates an RTS decision/boundary proposal containing the inspected hashes, estimate, approval, provider operation ID, result, known cost, cleanup, and residual uncertainty.
