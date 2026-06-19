from pathlib import Path
from typing import Any

from .models import ObserverPolicy


class ObserverPolicyLoadError(ValueError):
    """Raised when an observer policy file cannot be parsed."""


def load_observer_policy(path: str | Path) -> ObserverPolicy:
    """Load ObserverPolicy from the v0 YAML policy file.

    This intentionally supports only the small YAML subset used by
    specs/multi_observer_v0.yaml. It avoids adding a runtime dependency while
    keeping the policy outside core routing logic.
    """
    policy_path = Path(path)
    return observer_policy_from_text(policy_path.read_text(encoding="utf-8"))


def observer_policy_from_text(text: str) -> ObserverPolicy:
    data = _parse_v0_policy(text)

    try:
        trigger_score = int(data["fusion_trigger_score"])
        risk_weights = {
            str(key): int(value) for key, value in data["risk_weights"].items()
        }
        blocklist = {str(item) for item in data["blocklist"]}
    except (AttributeError, KeyError, TypeError, ValueError) as e:
        raise ObserverPolicyLoadError("invalid observer policy fields") from e

    return ObserverPolicy(
        fusion_trigger_score=trigger_score,
        risk_weights=risk_weights,
        blocklist=blocklist,
    )


def _parse_v0_policy(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_section: str | None = None
    current_nested: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))

        if indent == 0:
            current_nested = None
            if stripped.endswith(":"):
                current_section = stripped[:-1]
                if current_section == "blocklist":
                    result[current_section] = []
                else:
                    result[current_section] = {}
                continue

            key, value = _split_key_value(stripped)
            result[key] = _parse_scalar(value)
            current_section = None
            continue

        if current_section is None:
            raise ObserverPolicyLoadError(f"unexpected indented line: {stripped}")

        if stripped.startswith("- "):
            section_value = result.setdefault(current_section, [])
            if not isinstance(section_value, list):
                raise ObserverPolicyLoadError(
                    f"section is not a list: {current_section}"
                )
            section_value.append(stripped[2:].strip())
            continue

        if stripped.endswith(":"):
            current_nested = stripped[:-1]
            section_value = result.setdefault(current_section, {})
            if not isinstance(section_value, dict):
                raise ObserverPolicyLoadError(
                    f"section is not a mapping: {current_section}"
                )
            section_value[current_nested] = {}
            continue

        key, value = _split_key_value(stripped)

        if current_nested is not None and indent >= 4:
            section_value = result[current_section]
            if not isinstance(section_value, dict):
                raise ObserverPolicyLoadError(
                    f"section is not a mapping: {current_section}"
                )
            nested_value = section_value[current_nested]
            if not isinstance(nested_value, dict):
                raise ObserverPolicyLoadError(
                    f"nested section is not a mapping: {current_nested}"
                )
            nested_value[key] = _parse_scalar(value)
            continue

        section_value = result[current_section]
        if not isinstance(section_value, dict):
            raise ObserverPolicyLoadError(
                f"section is not a mapping: {current_section}"
            )
        section_value[key] = _parse_scalar(value)

    return result


def _split_key_value(text: str) -> tuple[str, str]:
    if ":" not in text:
        raise ObserverPolicyLoadError(f"expected key/value line: {text}")
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value
