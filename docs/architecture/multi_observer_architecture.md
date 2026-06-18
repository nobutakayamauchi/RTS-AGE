# Multi Observer Architecture

## Philosophy

AI is treated as an observer, not a single final authority.

## Purpose

- Multiple observation
- Provider independence
- Easy adapter addition
- Rollback-friendly design

## Flow

User Request
-> Task Classification
-> Cheap Observer
-> Observer Gate
-> Optional Fusion Review
-> Execution
-> RTS Logging

## Fusion Role

Fusion is a Special Observer, not the core engine.

Use for:
- High-risk tasks
- High-uncertainty tasks
- Public releases
- Paid deliverables
- Legal, security, or financial review

Do not use for:
- Trivial rewrites
- Memo cleanup
- X post generation
- Draft-only work
- Small code edits

## Future Provider Policy

New providers should be added through adapters and configuration, not hardcoded into core logic.

## Logging Policy

Every routing decision should be JSONL-loggable with reason, score, selected observer, and task type.
