"""Loader for observer provider adapter configuration.

This module converts plain data into provider adapter configuration models. It
never creates adapters, calls providers, calls Fusion, or executes tasks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from core.observer_gate.provider_config import (
    ObserverProviderAdapterConfig,
    ObserverProviderConfig,
)


class ObserverProviderConfigError(ValueError):
    """Raised when observer provider adapter configuration is invalid."""


def load_observer_provider_config_from_mapping(
    data: dict[str, object],
) -> ObserverProviderConfig:
    """Load observer provider config from a plain mapping."""
    adapters_value = data.get("adapters", ())
    if not isinstance(adapters_value, list | tuple):
        raise ObserverProviderConfigError("adapters must be a list")

    config = ObserverProviderConfig()
    for index, adapter_value in enumerate(adapters_value):
        if not isinstance(adapter_value, dict):
            raise ObserverProviderConfigError(f"adapters[{index}] must be an object")
        adapter_config = _load_adapter_config(
            cast(dict[str, object], adapter_value), index
        )
        config = config.with_adapter_config(adapter_config)

    return config


def load_observer_provider_config_from_json_file(
    path: str | Path,
) -> ObserverProviderConfig:
    """Load observer provider config from a JSON file."""
    raw_data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw_data, dict):
        raise ObserverProviderConfigError("provider config root must be an object")
    return load_observer_provider_config_from_mapping(cast(dict[str, object], raw_data))


def _load_adapter_config(
    data: dict[str, object],
    index: int,
) -> ObserverProviderAdapterConfig:
    provider_id = _require_string(data, "provider_id", index)
    observer_name = _require_string(data, "observer_name", index)
    enabled = _optional_bool(data, "enabled", index, default=False)
    adapter_kind = _optional_string(data, "adapter_kind", index, default="stub")
    model = _optional_nullable_string(data, "model", index)

    return ObserverProviderAdapterConfig(
        provider_id=provider_id,
        observer_name=observer_name,
        enabled=enabled,
        adapter_kind=adapter_kind,
        model=model,
    )


def _require_string(data: dict[str, object], key: str, index: int) -> str:
    value = data.get(key)
    if not isinstance(value, str) or value == "":
        raise ObserverProviderConfigError(f"adapters[{index}].{key} must be a string")
    return value


def _optional_string(
    data: dict[str, object],
    key: str,
    index: int,
    *,
    default: str,
) -> str:
    value = data.get(key, default)
    if not isinstance(value, str) or value == "":
        raise ObserverProviderConfigError(f"adapters[{index}].{key} must be a string")
    return value


def _optional_nullable_string(
    data: dict[str, object],
    key: str,
    index: int,
) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or value == "":
        raise ObserverProviderConfigError(
            f"adapters[{index}].{key} must be a string or null"
        )
    return value


def _optional_bool(
    data: dict[str, object],
    key: str,
    index: int,
    *,
    default: bool,
) -> bool:
    value = data.get(key, default)
    if not isinstance(value, bool):
        raise ObserverProviderConfigError(f"adapters[{index}].{key} must be a bool")
    return value
