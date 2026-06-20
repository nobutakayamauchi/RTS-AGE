"""Dry-run smoke script for local observer provider flow.

This script stays on the safe local path. It loads config, builds a registry, and
uses the deterministic local adapter only.
"""

from __future__ import annotations

from core.observer_gate.provider_adapter import (
    ObserverProviderRequest,
    ObserverProviderResponse,
)
from core.observer_gate.provider_config_loader import (
    load_observer_provider_config_from_mapping,
)
from core.observer_gate.provider_registry_builder import (
    build_observer_provider_registry_from_config,
)
from core.observer_gate.provider_report import format_observer_provider_result


def run_observer_provider_dry_run() -> str:
    """Run a safe local observer provider dry-run and return a report."""
    config = load_observer_provider_config_from_mapping(
        {
            "adapters": [
                {
                    "provider_id": "local",
                    "observer_name": "default",
                    "enabled": True,
                    "adapter_kind": "local",
                    "model": "local-deterministic-v0",
                }
            ]
        }
    )
    registry = build_observer_provider_registry_from_config(config)
    request = ObserverProviderRequest(
        task_id="smoke-provider-local",
        task_type="memo_cleanup",
        prompt="private prompt text",
    )

    response = registry.require("local").observe(request)
    assert isinstance(response, ObserverProviderResponse)

    return "\n".join(
        [
            "Observer provider dry-run complete.",
            "",
            format_observer_provider_result(response),
        ]
    )


def main() -> None:
    """Run the provider dry-run smoke script."""
    print(run_observer_provider_dry_run())


if __name__ == "__main__":
    main()
