from pydantic import BaseModel


class SeverityBreakdownResponse(BaseModel):
    low: int
    medium: int
    high: int
    critical: int


class MonthlyAuditStatResponse(BaseModel):
    audit_month: str
    audit_count: int
    finding_count: int


class QualityDashboardSummaryResponse(BaseModel):
    total_audits: int
    total_findings: int
    avg_findings_per_audit: float
    severity_breakdown: SeverityBreakdownResponse
    monthly: list[MonthlyAuditStatResponse]
