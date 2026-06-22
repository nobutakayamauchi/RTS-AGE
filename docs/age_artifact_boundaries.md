# AGE Artifact Boundaries

## Purpose

This document defines where AGE-related files should live in this repository.

AGE is the builder. Generated products and runtime outputs should not become indistinguishable from AGE source code.

---

## Repository Roles

```text
AGE source code
AGE specifications
AGE fixtures
runtime outputs
generated products
```

Each role has a different lifecycle.

---

## AGE Source Code

AGE source code belongs in source-oriented directories such as:

```text
src/
smoke/
cli/
tests/
```

These files are maintained by normal code review.

---

## AGE Specifications

Stable specs and planning documents belong in:

```text
docs/
docs/specs/
```

These files describe intended behavior and implementation boundaries.

---

## AGE Fixtures

Checked-in generated examples belong in:

```text
fixtures/
```

For AGE planning dry-runs, the checked-in fixture package is:

```text
fixtures/age_planning_dry_run/
```

Fixtures are committed because they are reviewable examples and test references.

They are not live runtime output.

---

## Runtime Outputs

Runtime-generated files belong in:

```text
outputs/
logs/
runs/
```

These paths are ignored by default, except for `.gitkeep` placeholders.

Runtime outputs may be produced locally by commands and smoke tests, but they should not be committed as normal source files.

---

## Generated Products

If AGE creates a product that becomes large enough to maintain independently, it should be moved into a product namespace or a separate repository.

Recommended intermediate in-repo location:

```text
products/<product-name>/
```

Possible future split:

```text
RTS-AGE              = builder
RTS-Adapt-Engine     = generated/maintained product
```

Do not split too early. First separate fixture, runtime, and product roles inside this repository.

---

## Current Boundary Decision

For the current RTS Adapt Engine v0.1 work:

```text
fixtures/age_planning_dry_run/  = checked-in planning sample
outputs/                        = runtime-generated files
logs/                           = runtime-generated logs
src/                            = current implementation source
```

The draft-output generator work can continue after this boundary cleanup.

---

## Safety Rule

Generated runtime artifacts must not contain or require:

```text
production credentials
API tokens
connector secrets
auto-publishing state
auto-send state
```

Human review remains the approval gate before anything is published or sent.
