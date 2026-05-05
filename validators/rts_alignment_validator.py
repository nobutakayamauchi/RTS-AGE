from __future__ import annotations

import argparse
import datetime as dt
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ParsedEntities:
    skills: dict[str, dict[str, Any]]
    packs: dict[str, dict[str, Any]]
    drives: dict[str, dict[str, Any]]


DANGEROUS_TERMS = ("publish", "live", "trade", "trading", "credential", "secret", "key")
HIGH_RISK_TERMS = ("social.publish", "sns.publish", "publish.social", "social_post")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RTS Skill/Pack/Drive alignment validator")
    parser.add_argument("--skills-root", required=True)
    parser.add_argument("--packs-root", required=True)
    parser.add_argument("--drives-root", required=True)
    parser.add_argument(
        "--report-out", default="outputs/reports/rts-alignment-report.md"
    )
    parser.add_argument(
        "--record-out",
        default="outputs/rts-record-proposals/rts-alignment-check.record.yaml",
    )
    return parser.parse_args()


def parse_scalar(value: str) -> Any:
    raw = value.strip()
    if raw in ("", "null", "~"):
        return None
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return raw[1:-1]
    return raw


def parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"invalid indentation at line {line_number}")
        parent = stack[-1][1]

        if line.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"list item without list parent at line {line_number}")
            item_body = line[2:].strip()
            if not item_body:
                new_item: Any = {}
                parent.append(new_item)
                stack.append((indent, new_item))
                continue
            if ":" in item_body:
                key, remainder = item_body.split(":", 1)
                key = key.strip()
                remainder = remainder.strip()
                node: dict[str, Any] = {key: parse_scalar(remainder) if remainder else {}}
                parent.append(node)
                if not remainder:
                    stack.append((indent, node[key]))
                else:
                    stack.append((indent, node))
            else:
                parent.append(parse_scalar(item_body))
            continue

        if ":" not in line:
            raise ValueError(f"invalid key/value format at line {line_number}")

        key, remainder = line.split(":", 1)
        key = key.strip()
        remainder = remainder.strip()

        if not isinstance(parent, dict):
            raise ValueError(f"key/value entry under non-dict parent at line {line_number}")

        if remainder:
            parent[key] = parse_scalar(remainder)
        else:
            next_line = ""
            for candidate in text.splitlines()[line_number:]:
                if candidate.strip() and not candidate.lstrip().startswith("#"):
                    next_line = candidate
                    break
            if next_line.strip().startswith("- "):
                parent[key] = []
            else:
                parent[key] = {}
            stack.append((indent, parent[key]))

    return root


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    if value is None:
        return []
    return [str(value)]


def flatten_permissions(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    if value is None:
        return []
    return [str(value)]


def read_manifest(path: Path) -> dict[str, Any]:
    try:
        return parse_simple_yaml(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"read error: {exc}") from exc


def collect_entities(skills_root: Path, packs_root: Path, drives_root: Path) -> tuple[ParsedEntities, list[str]]:
    errors: list[str] = []
    skills: dict[str, dict[str, Any]] = {}
    packs: dict[str, dict[str, Any]] = {}
    drives: dict[str, dict[str, Any]] = {}

    for file_path in sorted((skills_root / "rts-skills" / "manifests").glob("*.skill.yaml")):
        try:
            data = read_manifest(file_path)
            skill_id = str(data.get("skill_id", "")).strip()
            if not skill_id:
                errors.append(f"{file_path}: missing skill_id")
                continue
            skills[skill_id] = {
                "skill_id": skill_id,
                "required_packs": safe_list(data.get("required_packs")),
                "outputs_to_rts": data.get("outputs_to_rts"),
            }
        except ValueError as exc:
            errors.append(f"{file_path}: {exc}")

    for file_path in sorted((packs_root / "manifests").glob("*.pack.yaml")):
        try:
            data = read_manifest(file_path)
            pack_id = str(data.get("pack_id", "")).strip()
            if not pack_id:
                errors.append(f"{file_path}: missing pack_id")
                continue
            packs[pack_id] = {
                "pack_id": pack_id,
                "supports_skills": safe_list(data.get("supports_skills")),
                "permissions": flatten_permissions(data.get("permissions")),
            }
        except ValueError as exc:
            errors.append(f"{file_path}: {exc}")

    for file_path in sorted((drives_root / "manifests").glob("*.drive.yaml")):
        try:
            data = read_manifest(file_path)
            drive_id = str(data.get("drive_id", "")).strip()
            if not drive_id:
                errors.append(f"{file_path}: missing drive_id")
                continue
            skill_block = data.get("skill") if isinstance(data.get("skill"), dict) else {}
            drives[drive_id] = {
                "drive_id": drive_id,
                "skill_id": str(skill_block.get("id", "")).strip(),
                "packs": safe_list(data.get("packs")),
                "outputs_to_rts": data.get("outputs_to_rts"),
            }
        except ValueError as exc:
            errors.append(f"{file_path}: {exc}")

    return ParsedEntities(skills=skills, packs=packs, drives=drives), errors


def validate_alignment(entities: ParsedEntities) -> tuple[list[str], list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    high_risk: list[str] = []
    facts: list[str] = []

    for skill_id, skill in entities.skills.items():
        for required_pack in skill["required_packs"]:
            if required_pack not in entities.packs:
                errors.append(f"skill '{skill_id}' requires missing pack '{required_pack}'")

    for pack_id, pack in entities.packs.items():
        for supported_skill in pack["supports_skills"]:
            if supported_skill not in entities.skills:
                errors.append(f"pack '{pack_id}' supports missing skill '{supported_skill}'")

        normalized_permissions = [p.lower() for p in pack["permissions"]]
        for permission in normalized_permissions:
            if any(term in permission for term in DANGEROUS_TERMS):
                warnings.append(
                    f"pack '{pack_id}' permission '{permission}' contains dangerous keyword"
                )
            if any(term in permission for term in HIGH_RISK_TERMS) or (
                "social" in permission and "publish" in permission
            ):
                high_risk.append(
                    f"pack '{pack_id}' permission '{permission}' indicates social publish risk"
                )

    for drive_id, drive in entities.drives.items():
        if drive["skill_id"] not in entities.skills:
            errors.append(
                f"drive '{drive_id}' references missing skill '{drive['skill_id']}'"
            )
        for pack_id in drive["packs"]:
            if pack_id not in entities.packs:
                errors.append(f"drive '{drive_id}' references missing pack '{pack_id}'")
        if drive["outputs_to_rts"] in (None, "", []):
            errors.append(f"drive '{drive_id}' missing outputs_to_rts")

    facts.append(f"skills_loaded={len(entities.skills)}")
    facts.append(f"packs_loaded={len(entities.packs)}")
    facts.append(f"drives_loaded={len(entities.drives)}")
    return errors, warnings, high_risk, facts


def write_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "# RTS Alignment Validation Report",
        "",
        "## Summary",
        f"- Status: **{payload['status']}**",
        f"- Errors: {len(payload['errors'])}",
        f"- Warnings: {len(payload['warnings'])}",
        f"- High-risk warnings: {len(payload['high_risk_warnings'])}",
        "",
        "## Checked repositories",
        f"- skills_root: `{payload['skills_root']}`",
        f"- packs_root: `{payload['packs_root']}`",
        f"- drives_root: `{payload['drives_root']}`",
        "",
        "## Skills found",
    ]
    lines.extend([f"- {sid}" for sid in payload["skills_found"]] or ["- (none)"])
    lines.append("")
    lines.append("## Packs found")
    lines.extend([f"- {pid}" for pid in payload["packs_found"]] or ["- (none)"])
    lines.append("")
    lines.append("## Drives found")
    lines.extend([f"- {did}" for did in payload["drives_found"]] or ["- (none)"])
    for section in (
        "errors",
        "warnings",
        "high_risk_warnings",
        "confirmed_facts",
        "assumptions",
        "unverified",
        "risks",
    ):
        title = section.replace("_", " ").title()
        lines.append("")
        lines.append(f"## {title}")
        values = payload[section]
        lines.extend([f"- {v}" for v in values] or ["- (none)"])

    lines.append("")
    lines.append("## Recommended next actions")
    if payload["status"] == "success":
        lines.append("- Proceed with dry-run adapter execution using this aligned baseline.")
    else:
        lines.append("- Fix alignment errors and rerun validator before adapter experiments.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def yaml_list(items: list[str], indent: int = 0) -> list[str]:
    prefix = " " * indent
    if not items:
        return [f"{prefix}[]"]
    return [f"{prefix}- {item!r}" for item in items]


def write_record(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "record_type: rts_alignment_check",
        f"checked_at: {payload['checked_at']!r}",
        f"skills_root: {payload['skills_root']!r}",
        f"packs_root: {payload['packs_root']!r}",
        f"drives_root: {payload['drives_root']!r}",
        f"status: {payload['status']!r}",
    ]
    for key in (
        "errors",
        "warnings",
        "high_risk_warnings",
        "confirmed_facts",
        "assumptions",
        "unverified",
        "risks",
    ):
        lines.append(f"{key}:")
        lines.extend(yaml_list(payload[key], indent=2))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    skills_root = Path(args.skills_root)
    packs_root = Path(args.packs_root)
    drives_root = Path(args.drives_root)

    for root in (skills_root, packs_root, drives_root):
        if not root.exists() or not root.is_dir():
            print(f"input path error: {root}", file=sys.stderr)
            return 2

    entities, parse_errors = collect_entities(skills_root, packs_root, drives_root)
    errors, warnings, high_risk, facts = validate_alignment(entities)
    all_errors = [*parse_errors, *errors]
    status = "success" if not all_errors else "alignment_error"

    payload = {
        "checked_at": dt.datetime.now(dt.UTC).isoformat(),
        "skills_root": str(skills_root),
        "packs_root": str(packs_root),
        "drives_root": str(drives_root),
        "status": status,
        "skills_found": sorted(entities.skills.keys()),
        "packs_found": sorted(entities.packs.keys()),
        "drives_found": sorted(entities.drives.keys()),
        "errors": all_errors,
        "warnings": warnings,
        "high_risk_warnings": high_risk,
        "confirmed_facts": facts,
        "assumptions": [
            "Validator uses a minimal YAML subset parser suitable for current RTS manifests.",
            "Only requested manifest paths are evaluated.",
        ],
        "unverified": [
            "Canonical repositories were not modified or queried remotely by this tool.",
        ],
        "risks": [
            "Manifests using advanced YAML features may fail parsing in this minimal parser.",
        ],
    }

    write_report(Path(args.report_out), payload)
    write_record(Path(args.record_out), payload)

    if parse_errors:
        return 2
    return 0 if status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
