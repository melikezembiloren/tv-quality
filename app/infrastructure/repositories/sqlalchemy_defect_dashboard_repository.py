from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.infrastructure.db.models.inspection import InspectionModel
from app.application.dto.defect_dashboard_dto import DefectDashboardSummary, PeriodStat, ReasonFrequency


class SqlAlchemyDefectDashboardRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_summary(self) -> DefectDashboardSummary:
        total_inspected = self._session.query(func.count(InspectionModel.id)).scalar() or 0
        total_defective = (
            self._session.query(func.count(InspectionModel.id))
            .filter(InspectionModel.result == "FAIL")
            .scalar()
            or 0
        )
        overall_rate = round(total_defective / total_inspected * 100, 2) if total_inspected else 0.0

        defective_case = case((InspectionModel.result == "FAIL", 1), else_=0)

        daily = self._period_stats(func.to_char(InspectionModel.inspected_at, "YYYY-MM-DD"), defective_case)
        weekly = self._period_stats(func.to_char(InspectionModel.inspected_at, "IYYY-\"W\"IW"), defective_case)
        monthly = self._period_stats(func.to_char(InspectionModel.inspected_at, "YYYY-MM"), defective_case)

        reason_rows = (
            self._session.query(InspectionModel.defect_reason, func.count(InspectionModel.id))
            .filter(InspectionModel.result == "FAIL", InspectionModel.defect_reason.isnot(None))
            .group_by(InspectionModel.defect_reason)
            .order_by(func.count(InspectionModel.id).desc())
            .limit(8)
            .all()
        )
        top_reasons = [ReasonFrequency(reason=r, count=c) for r, c in reason_rows]

        return DefectDashboardSummary(
            total_inspected=total_inspected,
            total_defective=total_defective,
            overall_defect_rate=overall_rate,
            daily=daily,
            weekly=weekly,
            monthly=monthly,
            top_reasons=top_reasons,
        )

    def _period_stats(self, period_expr, defective_case) -> list[PeriodStat]:
        rows = (
            self._session.query(
                period_expr.label("period"),
                func.count(InspectionModel.id),
                func.sum(defective_case),
            )
            .group_by("period")
            .order_by("period")
            .all()
        )
        return [PeriodStat(period=p, inspected=i, defective=int(d or 0)) for p, i, d in rows]
