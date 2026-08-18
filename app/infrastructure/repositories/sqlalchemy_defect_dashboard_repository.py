from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.infrastructure.db.models.inspection import InspectionModel
from app.infrastructure.db.models.defect_category import DefectCategoryModel
from app.infrastructure.db.models.tv import TVModel
from app.application.dto.defect_dashboard_dto import (
    DefectDashboardSummary,
    PeriodStat,
    ReasonFrequency,
    CategorySlice,
)


class SqlAlchemyDefectDashboardRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_summary(self, production_line_id: int | None = None) -> DefectDashboardSummary:
        total_inspected = self._base_query(production_line_id, func.count(InspectionModel.id)).scalar() or 0
        total_defective = (
            self._base_query(production_line_id, func.count(InspectionModel.id))
            .filter(InspectionModel.result == "FAIL")
            .scalar()
            or 0
        )
        overall_rate = round(total_defective / total_inspected * 100, 2) if total_inspected else 0.0

        defective_case = case((InspectionModel.result == "FAIL", 1), else_=0)

        daily = self._period_stats(func.to_char(InspectionModel.inspected_at, "YYYY-MM-DD"), defective_case, production_line_id)
        weekly = self._period_stats(func.to_char(InspectionModel.inspected_at, "IYYY-\"W\"IW"), defective_case, production_line_id)
        monthly = self._period_stats(func.to_char(InspectionModel.inspected_at, "YYYY-MM"), defective_case, production_line_id)

        reason_q = (
            self._base_query(production_line_id, DefectCategoryModel.name, func.count(InspectionModel.id))
            .join(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(InspectionModel.result == "FAIL")
            .group_by(DefectCategoryModel.name)
            .order_by(func.count(InspectionModel.id).desc())
            .limit(8)
        )
        top_reasons = [ReasonFrequency(reason=r, count=c) for r, c in reason_q.all()]

        return DefectDashboardSummary(
            total_inspected=total_inspected,
            total_defective=total_defective,
            overall_defect_rate=overall_rate,
            daily=daily,
            weekly=weekly,
            monthly=monthly,
            top_reasons=top_reasons,
            category_breakdown_daily=self._category_breakdown("day", production_line_id),
            category_breakdown_weekly=self._category_breakdown("week", production_line_id),
            category_breakdown_monthly=self._category_breakdown("month", production_line_id),
        )

    def _base_query(self, production_line_id: int | None, *select_exprs):
        """
        Hangi kolonlar sorgulanırsa sorgulansın, hat filtresi verildiğinde
        tvs tablosuna JOIN atıp o hatta ait olmayan kayıtları eler.
        """
        query = self._session.query(*select_exprs)
        if production_line_id is not None:
            query = query.join(TVModel, TVModel.id == InspectionModel.tv_id).filter(
                TVModel.line_id == production_line_id
            )
        return query

    def _period_stats(self, period_expr, defective_case, production_line_id: int | None) -> list[PeriodStat]:
        rows = (
            self._base_query(
                production_line_id, period_expr.label("period"), func.count(InspectionModel.id), func.sum(defective_case)
            )
            .group_by("period")
            .order_by("period")
            .all()
        )
        return [PeriodStat(period=p, inspected=i, defective=int(d or 0)) for p, i, d in rows]

    def _category_breakdown(self, trunc_unit: str, production_line_id: int | None) -> list[CategorySlice]:
        """trunc_unit: 'day' | 'week' | 'month' — o anki pencere (bugün/bu hafta/bu ay) için hata türü dağılımı."""
        window_start = func.date_trunc(trunc_unit, func.now())
        rows = (
            self._base_query(production_line_id, DefectCategoryModel.name, func.count(InspectionModel.id))
            .join(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(InspectionModel.result == "FAIL", InspectionModel.inspected_at >= window_start)
            .group_by(DefectCategoryModel.name)
            .order_by(func.count(InspectionModel.id).desc())
            .all()
        )
        return [CategorySlice(category_name=r, count=c) for r, c in rows]
