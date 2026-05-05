from __future__ import annotations

import argparse
import datetime as dt
import glob
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DANGEROUS_KEYWORDS = ("publish", "live", "trade", "credential", "secret")
HIGH_RISK_KEYWORDS = ("social.publish",)


class SimpleYAMLParseError(ValueError):
    """Raised when the minimal YAML parser cannot parse the input."""


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]
    confirmed_facts: list[str]
    assumptions: list[str]
    unverified: list[str]
    risks: list[str]

    @property
    def status(self) -> str:
        return "error" if self.errors else "ok"


class MinimalYAMLParser:
    """Very small YAML subset parser for RTS manifests."""

    def parse(self, text: str) -> dict[str, Any]:
        lines = self._preprocess(text)
        root: dict[str, Any] = {}
        stack: list[tuple[int, Any]] = [(-1, root)]

        for index, (indent, content) in enumerate(lines):
            while len(stack) > 1 and indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]

            if content.startswith("- "):
                if not isinstance(parent, list):
                    raise SimpleYAMLParseError("List item found without list parent")
                parent.append(self._parse_scalar(content[2:].strip()))
                continue

            if ":" not in content:
                raise SimpleYAMLParseError(f"Invalid line: {content}")
            key, raw_val = content.split(":", 1)
            key = key.strip()
            raw_val = raw_val.strip()

            if not isinstance(parent, dict):
                raise SimpleYAMLParseError("Key/value found without dict parent")

            if raw_val:
                parent[key] = self._parse_scalar(raw_val)
                continue

            next_container: Any = {}
            if index + 1 < len(lines):
                next_indent, next_content = lines[index + 1]
                if next_indent > indent and next_content.startswith("- "):
                    next_container = []

            parent[key] = next_container
            stack.append((indent, next_container))

        return root

    def _preprocess(self, text: str) -> list[tuple[int, str]]:
        lines: list[tuple[int, str]] = []
        for raw_line in text.splitlines():
            without_comment = raw_line.split("#", 1)[0].rstrip()
            if not without_comment.strip():
                continue
            indent = len(without_comment) - len(without_comment.lstrip(" "))
            lines.append((indent, without_comment.lstrip(" ")))
        return lines

    def _parse_scalar(self, raw: str) -> Any:
        lowered = raw.lower()
        if lowered in {"null", "none", "~"}:
            return None
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if raw.isdigit():
            return int(raw)
        try:
            return float(raw)
        except ValueError:
            pass
        if (raw.startswith('"') and raw.endswith('"')) or (
            raw.startswith("'") and raw.endswith("'")
        ):
            return raw[1:-1]
        return raw


def _ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def _load_manifest(path: Path, parser: MinimalYAMLParser) -> dict[str, Any]:
    return parser.parse(path.read_text(encoding="utf-8"))


def run_validation(
    skills_root: Path, packs_root: Path, drives_root: Path
) -> ValidationResult:
    parser = MinimalYAMLParser()
    errors: list[str] = []
    warnings: list[str] = []
    confirmed_facts: list[str] = []
    assumptions: list[str] = [
        "Manifest YAML uses minimal mapping/list subset.",
        "skill_id/pack_id/drive_id fields are the canonical IDs for this check.",
    ]
    unverified: list[str] = [
        "Schema-level validation beyond required fields is out of scope."
    ]
    risks: list[str] = ["Minimal YAML parser may reject advanced YAML constructs."]

    skills: dict[str, dict[str, Any]] = {}
    packs: dict[str, dict[str, Any]] = {}
    drives: dict[str, dict[str, Any]] = {}

    try:
        skill_paths = sorted(
            glob.glob(str(skills_root / "rts-skills" / "manifests" / "*.skill.yaml"))
        )
        pack_paths = sorted(glob.glob(str(packs_root / "manifests" / "*.pack.yaml")))
        drive_paths = sorted(glob.glob(str(drives_root / "manifests" / "*.drive.yaml")))
    except OSError as exc:
        raise RuntimeError(f"Failed to read manifest paths: {exc}") from exc

    for path_str in skill_paths:
        doc = _load_manifest(Path(path_str), parser)
        sid = str(doc.get("skill_id", "")).strip()
        if sid:
            skills[sid] = doc

    for path_str in pack_paths:
        doc = _load_manifest(Path(path_str), parser)
        pid = str(doc.get("pack_id", "")).strip()
        if pid:
            packs[pid] = doc

    for path_str in drive_paths:
        doc = _load_manifest(Path(path_str), parser)
        did = str(doc.get("drive_id", "")).strip()
        if did:
            drives[did] = doc

    for sid, skill in skills.items():
        errors.extend(
            [
                f"skill '{sid}' requires missing pack '{pack_id}'"
                for pack_id in _ensure_list(skill.get("required_packs"))
                if pack_id not in packs
            ]
        )

    for pid, pack in packs.items():
        errors.extend(
            [
                f"pack '{pid}' supports unknown skill '{sid}'"
                for sid in _ensure_list(pack.get("supports_skills"))
                if sid not in skills
            ]
        )

    for did, drive in drives.items():
        drive_skill = drive.get("skill", {})
        skill_id = ""
        if isinstance(drive_skill, dict):
            skill_id = str(drive_skill.get("id", "")).strip()
        if not skill_id or skill_id not in skills:
            errors.append(f"drive '{did}' references unknown skill '{skill_id}'")

        errors.extend(
            [
                f"drive '{did}' references unknown pack '{pack_id}'"
                for pack_id in _ensure_list(drive.get("packs"))
                if pack_id not in packs
            ]
        )

        if "outputs_to_rts" not in drive:
            errors.append(f"drive '{did}' is missing outputs_to_rts")

    for pid, pack in packs.items():
        perms = _ensure_list(pack.get("permissions"))
        for perm in perms:
            perm_lower = perm.lower()
            if any(k in perm_lower for k in HIGH_RISK_KEYWORDS):
                warnings.append(f"HIGH-RISK pack '{pid}' permission '{perm}'")
            elif any(k in perm_lower for k in DANGEROUS_KEYWORDS):
                warnings.append(
                    f"pack '{pid}' potentially dangerous permission '{perm}'"
                )

    confirmed_facts.extend(
        [
            f"skills_found={len(skills)}",
            f"packs_found={len(packs)}",
            f"drives_found={len(drives)}",
        ]
    )

    return ValidationResult(
        errors, warnings, confirmed_facts, assumptions, unverified, risks
    )


def _write_report(
    path: Path,
    result: ValidationResult,
    skills_root: Path,
    packs_root: Path,
    drives_root: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.UTC).isoformat()
    content = f"""# RTS Alignment Report

## Summary
- checked_at: {now}
- status: {result.status}
- errors: {len(result.errors)}
- warnings: {len(result.warnings)}

## Checked repositories
- skills_root: `{skills_root}`
- packs_root: `{packs_root}`
- drives_root: `{drives_root}`

## Skills found
- {next((f for f in result.confirmed_facts if f.startswith("skills_found=")), "skills_found=0")}

## Packs found
- {next((f for f in result.confirmed_facts if f.startswith("packs_found=")), "packs_found=0")}

## Drives found
- {next((f for f in result.confirmed_facts if f.startswith("drives_found=")), "drives_found=0")}

## Errors
"""
    content += "\n".join(f"- {e}" for e in result.errors) if result.errors else "- none"
    content += "\n\n## Warnings\n"
    content += (
        "\n".join(f"- {w}" for w in result.warnings) if result.warnings else "- none"
    )
    content += "\n\n## Confirmed facts\n" + "\n".join(
        f"- {x}" for x in result.confirmed_facts
    )
    content += "\n\n## Assumptions\n" + "\n".join(f"- {x}" for x in result.assumptions)
    content += "\n\n## Unverified\n" + "\n".join(f"- {x}" for x in result.unverified)
    content += "\n\n## Risks\n" + "\n".join(f"- {x}" for x in result.risks)
    content += "\n\n## Recommended next actions\n"
    content += "- Resolve all alignment errors before proposal promotion.\n"
    content += (
        "- Review warning permissions and confirm policy exceptions where needed.\n"
    )
    path.write_text(content, encoding="utf-8")


def _write_record(
    path: Path,
    result: ValidationResult,
    skills_root: Path,
    packs_root: Path,
    drives_root: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.UTC).isoformat()
    lines = [
        "record_type: rts_alignment_check",
        f"checked_at: {now}",
        f"skills_root: {skills_root}",
        f"packs_root: {packs_root}",
        f"drives_root: {drives_root}",
        f"status: {result.status}",
    ]
    for key, values in (
        ("errors", result.errors),
        ("warnings", result.warnings),
        ("confirmed_facts", result.confirmed_facts),
        ("assumptions", result.assumptions),
        ("unverified", result.unverified),
        ("risks", result.risks),
    ):
        lines.append(f"{key}:")
        if values:
            lines.extend([f"  - {v}" for v in values])
        else:
            lines.append("  []")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="RTS Skill/Pack/Drive alignment validator"
    )
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
    args = parser.parse_args(argv)

    skills_root = Path(args.skills_root)
    packs_root = Path(args.packs_root)
    drives_root = Path(args.drives_root)

    for root in (skills_root, packs_root, drives_root):
        if not root.exists() or not root.is_dir():
            print(f"Invalid repository path: {root}", file=sys.stderr)
            return 2

    try:
        result = run_validation(skills_root, packs_root, drives_root)
        _write_report(
            Path(args.report_out), result, skills_root, packs_root, drives_root
        )
        _write_record(
            Path(args.record_out), result, skills_root, packs_root, drives_root
        )
    except (OSError, RuntimeError, SimpleYAMLParseError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 2

    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
