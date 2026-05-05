from __future__ import annotations

from pathlib import Path

from validators.rts_alignment_validator import run_validation


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _setup_roots(tmp_path: Path) -> tuple[Path, Path, Path]:
    skills = tmp_path / "RTS-Skills-"
    packs = tmp_path / "RTS-MCP-Packs"
    drives = tmp_path / "RTS-Hermes-Drive"
    return skills, packs, drives


def test_validation_ok(tmp_path: Path) -> None:
    skills, packs, drives = _setup_roots(tmp_path)
    _write(
        skills / "rts-skills/manifests/a.skill.yaml",
        """skill_id: skill.a
required_packs:
  - pack.a
outputs_to_rts: true
""",
    )
    _write(
        packs / "manifests/a.pack.yaml",
        """pack_id: pack.a
supports_skills:
  - skill.a
permissions:
  - read
""",
    )
    _write(
        drives / "manifests/a.drive.yaml",
        """drive_id: drive.a
skill:
  id: skill.a
packs:
  - pack.a
outputs_to_rts: true
""",
    )

    result = run_validation(skills, packs, drives)

    assert result.errors == []
    assert result.status == "ok"


def test_missing_required_pack_error(tmp_path: Path) -> None:
    skills, packs, drives = _setup_roots(tmp_path)
    _write(
        skills / "rts-skills/manifests/a.skill.yaml",
        """skill_id: skill.a
required_packs:
  - pack.missing
""",
    )
    _write(packs / "manifests/a.pack.yaml", "pack_id: pack.a\n")
    _write(
        drives / "manifests/a.drive.yaml",
        """drive_id: drive.a
skill:
  id: skill.a
packs:
  - pack.a
outputs_to_rts: true
""",
    )

    result = run_validation(skills, packs, drives)

    assert any("requires missing pack 'pack.missing'" in e for e in result.errors)


def test_drive_unknown_skill_error(tmp_path: Path) -> None:
    skills, packs, drives = _setup_roots(tmp_path)
    _write(skills / "rts-skills/manifests/a.skill.yaml", "skill_id: skill.a\n")
    _write(packs / "manifests/a.pack.yaml", "pack_id: pack.a\n")
    _write(
        drives / "manifests/a.drive.yaml",
        """drive_id: drive.a
skill:
  id: skill.unknown
packs:
  - pack.a
outputs_to_rts: true
""",
    )

    result = run_validation(skills, packs, drives)

    assert any("references unknown skill 'skill.unknown'" in e for e in result.errors)


def test_social_publish_high_risk_warning(tmp_path: Path) -> None:
    skills, packs, drives = _setup_roots(tmp_path)
    _write(skills / "rts-skills/manifests/a.skill.yaml", "skill_id: skill.a\n")
    _write(
        packs / "manifests/a.pack.yaml",
        """pack_id: pack.a
supports_skills:
  - skill.a
permissions:
  - social.publish
""",
    )
    _write(
        drives / "manifests/a.drive.yaml",
        """drive_id: drive.a
skill:
  id: skill.a
packs:
  - pack.a
outputs_to_rts: true
""",
    )

    result = run_validation(skills, packs, drives)

    assert any("HIGH-RISK" in w and "social.publish" in w for w in result.warnings)
