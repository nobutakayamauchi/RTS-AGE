"""Smoke tests for the RTS Adapt Engine v0.1 scaffold."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_rts_adapt_engine_scaffold_files_exist():
    """The scaffold includes the local input, parser, and normalizer files."""
    assert Path("inputs/daily_input.md").is_file()
    assert Path("src/generate.py").is_file()
    assert Path("src/input_reader.py").is_file()
    assert Path("src/section_parser.py").is_file()
    assert Path("src/normalizer.py").is_file()
    assert Path("outputs").is_dir()
    assert Path("logs").is_dir()


def test_rts_adapt_engine_scaffold_command_runs():
    """The command runs locally and writes a context summary."""
    result = subprocess.run(
        [sys.executable, "src/generate.py"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0
    assert "RTS Adapt Engine v0.1 context normalizer ready." in result.stdout
    assert "context_summary_path=outputs/context_summary.md" in result.stdout
    assert "present_sections=" in result.stdout
    assert "missing_sections=" in result.stdout
    assert "unknown_sections=" in result.stdout
    assert "draft_generation_not_implemented=true" in result.stdout
    assert "external_api_calls=false" in result.stdout
    assert "publishing=false" in result.stdout
    assert Path("outputs/context_summary.md").is_file()
