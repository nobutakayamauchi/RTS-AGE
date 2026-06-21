# RTS Adapt Engine v0.1 Scaffold

## Purpose

This scaffold creates the first implementation boundary for RTS Adapt Engine v0.1.

It does not generate final content yet. It only establishes the local input, output, log, command, and smoke-test structure.

---

## Added Files

```text
inputs/daily_input.md
src/generate.py
outputs/.gitkeep
logs/.gitkeep
tests/smoke/test_rts_adapt_engine_scaffold.py
```

---

## Local Command

```bash
python src/generate.py
```

Expected output:

```text
RTS Adapt Engine v0.1 scaffold ready.
input_path=inputs/daily_input.md
output_dir=outputs
log_dir=logs
generation_not_implemented=true
external_api_calls=false
publishing=false
```

---

## Scope Boundary

This PR may:

```text
add input sample
add local scaffold command
add output/log directories
add smoke test
```

This PR must not:

```text
add real generators
call model APIs
call external APIs
execute connectors
publish content
send messages
store credentials
```

---

## Next Implementation Step

After this scaffold is reviewed and merged, the next PR should be:

```text
PR-02: Add input reader and section parser
```

That next PR should read `inputs/daily_input.md`, parse supported sections, tolerate missing sections, and avoid output generation.
