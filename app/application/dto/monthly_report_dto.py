from dataclasses import dataclass, field


@dataclass
class MonthlyReportLineStat:
    line_code: str
    line_name: str
    inspected: int
    defective: int


@dataclass
class MonthlyReportReasonStat:
    reason: str
    count: int


@dataclass
class MonthlyReportStationStat:
    station: str
    count: int


@dataclass
class MonthlyReportTrendPoint:
    period: str  # "2026-08"
    inspected: int
    defective: int


@dataclass
class MonthlyReportSeverityBreakdown:
    low: int = 0
    medium: int = 0
    high: int = 0
    critical: int = 0


@dataclass
class MonthlyReportData:
    month: str  # "2026-08"
    total_inspected: int
    total_defective: int
    defect_rate: float
    by_line: list[MonthlyReportLineStat] = field(default_factory=list)
    top_reasons: list[MonthlyReportReasonStat] = field(default_factory=list)
    by_station: list[MonthlyReportStationStat] = field(default_factory=list)
    trend_last_months: list[MonthlyReportTrendPoint] = field(default_factory=list)
    total_audits: int = 0
    total_findings: int = 0
    severity_breakdown: MonthlyReportSeverityBreakdown = field(default_factory=MonthlyReportSeverityBreakdown)
