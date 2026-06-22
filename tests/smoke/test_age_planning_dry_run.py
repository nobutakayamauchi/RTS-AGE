"""Tests for the AGE planning dry-run scaffold."""

from __future__ import annotations

import json
from pathlib import Path

from smoke.age_planning_dry_run import LOG_PATH, run_age_planning_dry_run

FIXTURE_ROOT = Path("fixtures/age_planning_dry_run")


def test_age_planning_dry_run_writes_expected_artifacts(tmp_path):
    """The dry-run writes runtime artifacts under the requested root."""
    report = run_age_planning_dry_run(tmp_path)

    assert "AGE planning dry-run complete." in report
    assert "review_required=true" in report

    expected_files = [
        "outputs/age/spec_intake_summary.md",
        "outputs/age/v0_1_scope_summary.md",
        "outputs/age/pr_plan.md",
        "outputs/age/scaffold_plan.md",
        "outputs/age/smoke_test_plan.md",
        "outputs/age/review_checklist.md",
        LOG_PATH,
    ]

    for relative_path in expected_files:
        assert (tmp_path / relative_path).is_file()

    log_lines = (tmp_path / LOG_PATH).read_text(encoding="utf-8").splitlines()
    assert len(log_lines) == 1

    log_entry = json.loads(log_lines[0])
    assert log_entry["active_scope"] == "rts-adapt-engine-v0.1"
    assert log_entry["review_required"] is True
    assert log_entry["safety_boundary"] == (
        "planning_only_no_external_api_no_auto_publish"
    )
    assert "outputs/age/pr_plan.md" in log_entry["generated_files"]


def test_age_planning_dry_run_pr_plan_preserves_no_api_boundary(tmp_path):
    """The sample PR plan keeps v0.1 implementation local-only."""
    run_age_planning_dry_run(tmp_path)

    pr_plan = (tmp_path / "outputs/age/pr_plan.md").read_text(encoding="utf-8")

    assert "PR-01: Add project scaffold" in pr_plan
    assert "No generators, connectors, or API calls." in pr_plan
    assert "Human review is required before implementation starts." in pr_plan


def test_age_planning_fixture_package_is_checked_in():
    """Checked-in samples live under fixtures, not runtime output paths."""
    expected_fixture_files = [
        "outputs/age/spec_intake_summary.md",
        "outputs/age/v0_1_scope_summary.md",
        "outputs/age/pr_plan.md",
        "outputs/age/scaffold_plan.md",
        "outputs/age/smoke_test_plan.md",
        "outputs/age/review_checklist.md",
        "logs/age_builder_execution_log.jsonl",
    ]

    for relative_path in expected_fixture_files:
        assert (FIXTURE_ROOT / relative_path).is_file()
