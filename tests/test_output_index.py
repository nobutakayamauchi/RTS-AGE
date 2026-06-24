"""Tests for RTS Adapt Engine output manifest generation."""

from __future__ import annotations

import json

from src.output_index import build_output_manifest, sha256_file, write_output_manifest


def test_sha256_file_returns_stable_digest(tmp_path):
    output_path = tmp_path / "outputs" / "context_summary.md"
    output_path.parent.mkdir(parents=True)
    output_path.write_text("hello\n", encoding="utf-8")

    assert sha256_file(output_path) == "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"


def test_build_output_manifest_lists_generated_files_and_safety_flags(tmp_path):
    input_path = tmp_path / "inputs" / "daily_input.md"
    context_path = tmp_path / "outputs" / "context_summary.md"
    draft_path = tmp_path / "outputs" / "x_posts.md"
    checklist_path = tmp_path / "outputs" / "review_checklist.md"
    log_path = tmp_path / "logs" / "execution_log.jsonl"

    for path, content in (
        (input_path, "input\n"),
        (context_path, "context\n"),
        (draft_path, "draft\n"),
        (checklist_path, "review\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    record = build_output_manifest(
        input_path=input_path,
        generated_paths=(context_path, draft_path, checklist_path),
        execution_log_path=log_path,
        created_at="2026-06-23T00:00:00Z",
    )

    assert record["schema_version"] == "rts-adapt-engine.output-manifest.v0.1"
    assert record["created_at"] == "2026-06-23T00:00:00Z"
    assert record["input_file"] == str(input_path)
    assert record["generated_file_count"] == 3
    assert [entry["path"] for entry in record["generated_files"]] == [
        str(context_path),
        str(draft_path),
        str(checklist_path),
    ]
    assert all("sha256" in entry for entry in record["generated_files"])
    assert all("bytes" in entry for entry in record["generated_files"])
    assert record["execution_log_file"] == str(log_path)
    assert record["external_api_calls"] is False
    assert record["publishing"] is False
    assert record["sending"] is False
    assert record["credentials_required"] is False
    assert record["review_required"] is True


def test_write_output_manifest_writes_stable_json(tmp_path):
    output_path = tmp_path / "outputs" / "context_summary.md"
    output_path.parent.mkdir(parents=True)
    output_path.write_text("context\n", encoding="utf-8")
    record = build_output_manifest(
        input_path=tmp_path / "inputs" / "daily_input.md",
        generated_paths=(output_path,),
        created_at="2026-06-23T00:00:00Z",
    )
    manifest_path = tmp_path / "outputs" / "output_manifest.json"

    written_path = write_output_manifest(manifest_path, record)

    assert written_path == manifest_path
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert loaded["schema_version"] == "rts-adapt-engine.output-manifest.v0.1"
    assert loaded["generated_file_count"] == 1
