from dataclasses import dataclass, field


@dataclass
class SeverityBreakdown:
    low: int = 0
    medium: int = 0
    high: int = 0
    critical: int = 0


@dataclass
class MonthlyAuditStat:
    audit_month: str
    audit_count: int
    finding_count: int


@dataclass
class QualityDashboardSummary:
    total_audits: int
    total_findings: int
    avg_findings_per_audit: float
    severity_breakdown: SeverityBreakdown
    monthly: list[MonthlyAuditStat] = field(default_factory=list)
