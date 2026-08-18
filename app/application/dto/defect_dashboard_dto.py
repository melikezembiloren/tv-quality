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
class CategorySlice:
    category_name: str
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
    # hata türü dağılımı, üç ayrı zaman penceresi için (bugün / bu hafta / bu ay)
    category_breakdown_daily: list[CategorySlice] = field(default_factory=list)
    category_breakdown_weekly: list[CategorySlice] = field(default_factory=list)
    category_breakdown_monthly: list[CategorySlice] = field(default_factory=list)
