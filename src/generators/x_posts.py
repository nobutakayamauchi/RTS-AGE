"""Deterministic X post draft generator."""

from __future__ import annotations

from src.section_parser import ParsedDailyInput

EMPTY_VALUE = "未入力"
MAX_POST_LENGTH = 280


def _section(parsed: ParsedDailyInput, name: str) -> str:
    return parsed.sections.get(name, "").strip() or EMPTY_VALUE


def _first_line(value: str) -> str:
    for line in value.splitlines():
        stripped = line.strip(" -\t")
        if stripped:
            return stripped
    return EMPTY_VALUE


def _compact(value: str, limit: int = 90) -> str:
    normalized = " ".join(part.strip() for part in value.splitlines() if part.strip())
    if not normalized:
        return EMPTY_VALUE
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def _post(title: str, body: str, cta: str) -> str:
    draft = f"{title}\n{body}\n{cta}\n\n※下書き・要確認"
    if len(draft) <= MAX_POST_LENGTH:
        return draft
    available = MAX_POST_LENGTH - len(title) - len(cta) - len("\n\n※下書き・要確認") - 3
    shortened_body = _compact(body, max(30, available))
    return f"{title}\n{shortened_body}\n{cta}\n\n※下書き・要確認"


def build_x_posts(parsed: ParsedDailyInput) -> str:
    """Build at least three reviewable X post drafts without external calls."""
    situation = _compact(_section(parsed, "今日の現状"))
    done = _compact(_section(parsed, "今日やったこと"))
    blocker = _compact(_section(parsed, "詰まっていること"))
    next_action = _compact(_section(parsed, "次にやること"))
    material = _compact(_section(parsed, "使いたいネタ"))
    core_message = _compact(_section(parsed, "言いたいこと"))
    offer = _compact(_section(parsed, "売りたい商品・サービス"))
    cta = _compact(_section(parsed, "誘導したい行動"), limit=60)

    drafts = [
        _post(
            "【現状共有】",
            f"いまの状況: {situation}\n今日進めたこと: {done}",
            f"次はこれ: {next_action}",
        ),
        _post(
            "【詰まりのメモ】",
            f"詰まり: {blocker}\n使える材料: {material}",
            "ここを崩さず小さく進める。",
        ),
        _post(
            "【提案の芯】",
            f"伝えたいこと: {core_message}\n提案: {offer}",
            f"行動: {cta}",
        ),
    ]

    lines = ["# X Post Drafts", "", "All drafts require human review before posting.", ""]
    for index, draft in enumerate(drafts, start=1):
        lines.append(f"## Draft {index}")
        lines.append("")
        lines.append(draft)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
