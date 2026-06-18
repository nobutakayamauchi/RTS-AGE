from dataclasses import dataclass, field


@dataclass
class TaskInput:
    task_id: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class TaskClassification:
    task_id: str
    task_type: str
    flags: set[str] = field(default_factory=set)
    reasons: list[str] = field(default_factory=list)


@dataclass
class ObserverPolicy:
    fusion_trigger_score: int
    risk_weights: dict[str, int] = field(default_factory=dict)
    blocklist: set[str] = field(default_factory=set)
    default_observer: str = 'default'
    fusion_observer: str = 'fusion'

    def is_blocklisted(self, task_type: str) -> bool:
        return task_type in self.blocklist

    def weight_for(self, flag: str) -> int:
        return self.risk_weights.get(flag, 0)


@dataclass
class ObserverDecision:
    task_id: str
    task_type: str
    selected_observer: str
    score: int
    should_use_fusion: bool
    reasons: list[str] = field(default_factory=list)
