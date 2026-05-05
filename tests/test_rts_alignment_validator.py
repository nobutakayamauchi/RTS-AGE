from __future__ import annotations

import subprocess


def _write(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def _run_validator(tmp_path, skill: str, pack: str, drive: str):
    skills_root = tmp_path / "RTS-Skills-"
    packs_root = tmp_path / "RTS-MCP-Packs"
    drives_root = tmp_path / "RTS-Hermes-Drive"

    _write(skills_root / "rts-skills" / "manifests" / "a.skill.yaml", skill)
    _write(packs_root / "manifests" / "a.pack.yaml", pack)
    _write(drives_root / "manifests" / "a.drive.yaml", drive)

    report_out = tmp_path / "outputs" / "reports" / "report.md"
    record_out = tmp_path / "outputs" / "rts-record-proposals" / "record.yaml"

    cmd = [
        "uv",
        "run",
        "python",
        "validators/rts_alignment_validator.py",
        "--skills-root",
        str(skills_root),
        "--packs-root",
        str(packs_root),
        "--drives-root",
        str(drives_root),
        "--report-out",
        str(report_out),
        "--record-out",
        str(record_out),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return completed, report_out, record_out


def test_alignment_success(tmp_path):
    completed, report_out, record_out = _run_validator(
        tmp_path,
        skill="""
        skill_id: skill.alpha
        required_packs:
          - pack.alpha
        outputs_to_rts:
          target: record
        """,
        pack="""
        pack_id: pack.alpha
        supports_skills:
          - skill.alpha
        permissions:
          - read.data
        """,
        drive="""
        drive_id: drive.alpha
        skill:
          id: skill.alpha
        packs:
          - pack.alpha
        outputs_to_rts:
          sink: rts
        """,
    )
    assert completed.returncode == 0
    assert report_out.exists()
    assert record_out.exists()
    assert "Status: **success**" in report_out.read_text(encoding="utf-8")


def test_missing_required_pack_causes_error(tmp_path):
    completed, report_out, _ = _run_validator(
        tmp_path,
        skill="""
        skill_id: skill.alpha
        required_packs:
          - pack.missing
        outputs_to_rts:
          target: record
        """,
        pack="""
        pack_id: pack.alpha
        supports_skills:
          - skill.alpha
        permissions:
          - read.data
        """,
        drive="""
        drive_id: drive.alpha
        skill:
          id: skill.alpha
        packs:
          - pack.alpha
        outputs_to_rts:
          sink: rts
        """,
    )
    assert completed.returncode == 1
    report = report_out.read_text(encoding="utf-8")
    assert "requires missing pack 'pack.missing'" in report


def test_missing_drive_skill_causes_error(tmp_path):
    completed, report_out, _ = _run_validator(
        tmp_path,
        skill="""
        skill_id: skill.alpha
        required_packs:
          - pack.alpha
        outputs_to_rts:
          target: record
        """,
        pack="""
        pack_id: pack.alpha
        supports_skills:
          - skill.alpha
        permissions:
          - read.data
        """,
        drive="""
        drive_id: drive.alpha
        skill:
          id: skill.missing
        packs:
          - pack.alpha
        outputs_to_rts:
          sink: rts
        """,
    )
    assert completed.returncode == 1
    assert "references missing skill 'skill.missing'" in report_out.read_text(encoding="utf-8")


def test_high_risk_social_publish_permission(tmp_path):
    completed, report_out, _ = _run_validator(
        tmp_path,
        skill="""
        skill_id: skill.alpha
        required_packs:
          - pack.alpha
        outputs_to_rts:
          target: record
        """,
        pack="""
        pack_id: pack.alpha
        supports_skills:
          - skill.alpha
        permissions:
          - social.publish
        """,
        drive="""
        drive_id: drive.alpha
        skill:
          id: skill.alpha
        packs:
          - pack.alpha
        outputs_to_rts:
          sink: rts
        """,
    )
    assert completed.returncode == 0
    report = report_out.read_text(encoding="utf-8")
    assert "High-risk warnings" in report
    assert "social publish risk" in report


def test_high_risk_social_publish_permission_dict(tmp_path):
    completed, report_out, _ = _run_validator(
        tmp_path,
        skill="""
        skill_id: skill.alpha
        required_packs:
          - pack.alpha
        outputs_to_rts:
          target: record
        """,
        pack="""
        pack_id: pack.alpha
        supports_skills:
          - skill.alpha
        permissions:
          social.publish: draft
        """,
        drive="""
        drive_id: drive.alpha
        skill:
          id: skill.alpha
        packs:
          - pack.alpha
        outputs_to_rts:
          sink: rts
        """,
    )
    assert completed.returncode == 0
    report = report_out.read_text(encoding="utf-8")
    assert "High-risk warnings" in report
    assert "social publish risk" in report
