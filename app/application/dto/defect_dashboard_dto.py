from dataclasses import dataclass, field


@dataclass
class PeriodStat:
    period: str  # gün: "2026-08-12", hafta: "2026-W32", ay: "2026-08"
    inspected: int
    defective: int


@dataclass
class ReasonFrequency:
    reason: str
    count: int


@dataclass
class DefectDashboardSummary:
    total_inspected: int
    total_defective: int
    overall_defect_rate: float
    daily: list[PeriodStat] = field(default_factory=list)
    weekly: list[PeriodStat] = field(default_factory=list)
    monthly: list[PeriodStat] = field(default_factory=list)
    top_reasons: list[ReasonFrequency] = field(default_factory=list)
