from .models import TaskClassification

_KEYWORDS: dict[str, tuple[str, ...]] = {
    'paid_delivery': ('納品', 'delivery', 'deliverable', 'client work'),
    'public_release': ('公開', 'public release', 'publish', 'release'),
    'legal_or_money': ('見積', '契約', '補助金', 'クラファン', '法務', '申請', 'estimate', 'contract', 'subsidy', 'crowdfunding', 'legal', 'money'),
    'security': ('セキュリティ', 'security', 'vulnerability', 'auth', 'credential', 'secret'),
    'simple_rewrite': ('書き換え', '文章修正', 'rewrite', 'rephrase'),
    'memo_cleanup': ('メモ整理', 'memo cleanup', 'organize memo'),
    'x_post_generation': ('X投稿', 'tweet', 'x post'),
    'draft_only': ('下書き', 'draft'),
    'trivial_code_edit': ('小さなコード修正', '軽微な修正', 'trivial code edit', 'small code edit'),
    'unclear_requirements': ('曖昧', '不明確', 'unclear', 'ambiguous'),
    'multi_domain': ('営業LP', '法務', 'セキュリティ', 'UX', '技術', 'sales lp', 'legal', 'security', 'technical'),
    'high_failure_cost': ('失敗コスト', '高リスク', 'high risk', 'high failure cost'),
}

_BLOCKLIST_PRIORITY = (
    'simple_rewrite',
    'memo_cleanup',
    'x_post_generation',
    'draft_only',
    'trivial_code_edit',
)

_RISK_PRIORITY = (
    'security',
    'legal_or_money',
    'paid_delivery',
    'public_release',
    'high_failure_cost',
    'multi_domain',
    'unclear_requirements',
)


def classify_task(task_id: str, text: str) -> TaskClassification:
    normalized = text.lower()
    flags: set[str] = set()
    reasons: list[str] = []

    for flag, keywords in _KEYWORDS.items():
        matched = [keyword for keyword in keywords if keyword.lower() in normalized]
        if matched:
            flags.add(flag)
            reasons.append(f"matched {flag}: {', '.join(matched)}")

    task_type = 'general'
    for candidate in _BLOCKLIST_PRIORITY:
        if candidate in flags:
            task_type = candidate
            break
    else:
        for candidate in _RISK_PRIORITY:
            if candidate in flags:
                task_type = candidate
                break

    return TaskClassification(
        task_id=task_id,
        task_type=task_type,
        flags=flags,
        reasons=reasons,
    )
