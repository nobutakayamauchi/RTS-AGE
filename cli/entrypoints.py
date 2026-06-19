"""CLI entry points for the installed package."""

DEFAULT_OBSERVER_LOG_PATH = "logs/observer_decisions.jsonl"


def _load_env_template() -> str:
    """Load the canonical root env template from package resources or source."""
    import importlib.resources
    from pathlib import Path

    packaged = importlib.resources.files("cli").joinpath("env.example")
    if packaged.is_file():
        return packaged.read_text("utf-8")

    source_template = Path(__file__).resolve().parents[1] / ".env.example"
    if source_template.is_file():
        return source_template.read_text(encoding="utf-8")

    raise FileNotFoundError("Could not find bundled or source .env.example template.")


def serve() -> None:
    """Start the FastAPI server (registered as `free-claude-code` script)."""
    import uvicorn

    from cli.process_registry import kill_all_best_effort
    from config.settings import get_settings

    settings = get_settings()
    try:
        uvicorn.run(
            "api.app:create_app",
            factory=True,
            host=settings.host,
            port=settings.port,
            log_level="debug",
            timeout_graceful_shutdown=5,
        )
    finally:
        kill_all_best_effort()


def init() -> None:
    """Scaffold config at ~/.config/free-claude-code/.env (registered as `fcc-init`)."""
    from pathlib import Path

    config_dir = Path.home() / ".config" / "free-claude-code"
    env_file = config_dir / ".env"

    if env_file.exists():
        print(f"Config already exists at {env_file}")
        print("Delete it first if you want to reset to defaults.")
        return

    config_dir.mkdir(parents=True, exist_ok=True)
    template = _load_env_template()
    env_file.write_text(template, encoding="utf-8")
    print(f"Config created at {env_file}")
    print(
        "Edit it to set your API keys and model preferences, then run: free-claude-code"
    )


def observer_log() -> None:
    """Print recent observer decision log entries."""
    import argparse

    from core.observer_gate.log_reader import (
        format_observer_decision_log_entries,
        read_observer_decision_log,
    )
    from core.observer_gate.report import (
        format_observer_decision_report,
        summarize_observer_decisions,
    )

    parser = argparse.ArgumentParser(
        prog="observer-log",
        description="Show recent observer gate decision log entries.",
    )
    parser.add_argument(
        "--path",
        default=DEFAULT_OBSERVER_LOG_PATH,
        help="Path to observer decision JSONL log.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of latest entries to show.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show aggregate observer decision metrics instead of raw entries.",
    )
    args = parser.parse_args()

    entries = read_observer_decision_log(args.path, limit=args.limit)
    if args.summary:
        report = summarize_observer_decisions(entries)
        print(format_observer_decision_report(report))
        return

    print(format_observer_decision_log_entries(entries))
