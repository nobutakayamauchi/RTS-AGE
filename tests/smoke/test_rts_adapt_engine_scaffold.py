"""Smoke tests for the RTS Adapt Engine v0.1 scaffold."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_rts_adapt_engine_scaffold_files_exist():
    """The scaffold PR adds the required local input and command files."""
    assert Path("inputs/daily_input.md").is_file()
    assert Path("src/generate.py").is_file()
    assert Path("outputs").is_dir()
    assert Path("logs").is_dir()


def test_rts_adapt_engine_scaffold_command_runs():
    """The scaffold command runs locally without generation side effects."""
    result = subprocess.run(
        [sys.executable, "src/generate.py"],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0
    assert "RTS Adapt Engine v0.1 scaffold ready." in result.stdout
    assert "generation_not_implemented=true" in result.stdout
    assert "external_api_calls=false" in result.stdout
    assert "publishing=false" in result.stdout
