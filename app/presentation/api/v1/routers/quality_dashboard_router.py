from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_quality_dashboard_summary_use_case
from app.presentation.api.v1.schemas.quality_dashboard_schemas import (
    QualityDashboardSummaryResponse,
    SeverityBreakdownResponse,
    MonthlyAuditStatResponse,
)

# Bilinçli olarak "quality-dashboard" prefix'i — /tvs, /production* gibi
# hiçbir üretim endpoint'iyle aynı kök altında değil, tamamen ayrı bir modül.
router = APIRouter(prefix="/quality-dashboard", tags=["Quality Dashboard"])


@router.get("/summary", response_model=QualityDashboardSummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    use_case = get_quality_dashboard_summary_use_case(db)
    result = use_case.execute()

    return QualityDashboardSummaryResponse(
        total_audits=result.total_audits,
        total_findings=result.total_findings,
        avg_findings_per_audit=result.avg_findings_per_audit,
        severity_breakdown=SeverityBreakdownResponse(
            low=result.severity_breakdown.low,
            medium=result.severity_breakdown.medium,
            high=result.severity_breakdown.high,
            critical=result.severity_breakdown.critical,
        ),
        monthly=[
            MonthlyAuditStatResponse(audit_month=m.audit_month, audit_count=m.audit_count, finding_count=m.finding_count)
            for m in result.monthly
        ],
    )
