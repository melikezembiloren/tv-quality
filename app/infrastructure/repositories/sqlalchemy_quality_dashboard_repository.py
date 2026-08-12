from sqlalchemy import func
from sqlalchemy.orm import Session

from app.infrastructure.db.models.audit import AuditModel, AuditFindingModel
from app.application.dto.quality_dashboard_dto import (
    QualityDashboardSummary,
    SeverityBreakdown,
    MonthlyAuditStat,
)


class SqlAlchemyQualityDashboardRepository:
    """
    Sadece audits/audit_findings tablolarını okur — production_lines, tvs,
    defects gibi üretim tablolarına hiç sorgu atmaz. Bu, kalite dashboard'unun
    üretimden bağımsız olmasının veri katmanındaki karşılığı.
    """

    def __init__(self, session: Session):
        self._session = session

    def get_summary(self) -> QualityDashboardSummary:
        total_audits = self._session.query(func.count(AuditModel.id)).scalar() or 0
        total_findings = self._session.query(func.count(AuditFindingModel.id)).scalar() or 0

        avg = round(total_findings / total_audits, 2) if total_audits else 0.0

        severity_rows = (
            self._session.query(AuditFindingModel.severity, func.count(AuditFindingModel.id))
            .group_by(AuditFindingModel.severity)
            .all()
        )
        severity_map = {sev: count for sev, count in severity_rows}
        breakdown = SeverityBreakdown(
            low=severity_map.get("LOW", 0),
            medium=severity_map.get("MEDIUM", 0),
            high=severity_map.get("HIGH", 0),
            critical=severity_map.get("CRITICAL", 0),
        )

        monthly_rows = (
            self._session.query(
                AuditModel.audit_month,
                func.count(func.distinct(AuditModel.id)),
                func.count(AuditFindingModel.id),
            )
            .outerjoin(AuditFindingModel, AuditFindingModel.audit_id == AuditModel.id)
            .group_by(AuditModel.audit_month)
            .order_by(AuditModel.audit_month.asc())
            .all()
        )
        monthly = [
            MonthlyAuditStat(audit_month=month, audit_count=audit_count, finding_count=finding_count)
            for month, audit_count, finding_count in monthly_rows
        ]

        return QualityDashboardSummary(
            total_audits=total_audits,
            total_findings=total_findings,
            avg_findings_per_audit=avg,
            severity_breakdown=breakdown,
            monthly=monthly,
        )
