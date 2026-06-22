"""Smoke coverage for the parser-enabled RTS Adapt Engine command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_rts_adapt_engine_parser_command_reports_section_counts():
    result = subprocess.run(
        [sys.executable, "src/generate.py"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0
    assert "RTS Adapt Engine v0.1 context normalizer ready." in result.stdout
    assert "present_sections=" in result.stdout
    assert "missing_sections=" in result.stdout
    assert "unknown_sections=" in result.stdout
    assert "draft_generation_not_implemented=true" in result.stdout
    assert "external_api_calls=false" in result.stdout
    assert "publishing=false" in result.stdout
    assert Path("outputs/context_summary.md").is_file()
