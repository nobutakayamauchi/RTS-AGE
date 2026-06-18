import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from .models import ObserverDecision


def append_observer_decision(decision: ObserverDecision, path: str | Path) -> None:
    """Append an observer routing decision as one JSONL record.

    This function does not log task text or metadata to avoid leaking secrets.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        'timestamp': datetime.now(UTC).isoformat(),
        **asdict(decision),
    }

    with output_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
        f.write('\n')
