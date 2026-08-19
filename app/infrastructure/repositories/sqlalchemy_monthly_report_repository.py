from datetime import date

from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.infrastructure.db.models.inspection import InspectionModel
from app.infrastructure.db.models.defect_category import DefectCategoryModel
from app.infrastructure.db.models.tv import TVModel
from app.infrastructure.db.models.production_line import ProductionLineModel
from app.infrastructure.db.models.audit import AuditModel, AuditFindingModel
from app.infrastructure.repositories.defect_station_mapping import STATION_BY_CATEGORY_CODE
from app.application.dto.monthly_report_dto import (
    MonthlyReportData,
    MonthlyReportLineStat,
    MonthlyReportReasonStat,
    MonthlyReportStationStat,
    MonthlyReportTrendPoint,
    MonthlyReportSeverityBreakdown,
)


def _month_bounds(month: str) -> tuple[date, date]:
    year, mon = (int(p) for p in month.split("-"))
    start = date(year, mon, 1)
    end = date(year + 1, 1, 1) if mon == 12 else date(year, mon + 1, 1)
    return start, end


class SqlAlchemyMonthlyReportRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_report(self, month: str) -> MonthlyReportData:
        start, end = _month_bounds(month)
        in_month = (InspectionModel.inspected_at >= start) & (InspectionModel.inspected_at < end)

        total_inspected = self._session.query(func.count(InspectionModel.id)).filter(in_month).scalar() or 0
        total_defective = (
            self._session.query(func.count(InspectionModel.id))
            .filter(in_month, InspectionModel.result == "FAIL")
            .scalar()
            or 0
        )
        defect_rate = round(total_defective / total_inspected * 100, 2) if total_inspected else 0.0

        by_line = self._by_line(in_month)
        top_reasons = self._top_reasons(in_month)
        by_station = self._by_station(in_month)
        trend = self._trend_last_months(month, months=6)
        total_audits, total_findings, severity = self._audit_summary(month)

        return MonthlyReportData(
            month=month,
            total_inspected=total_inspected,
            total_defective=total_defective,
            defect_rate=defect_rate,
            by_line=by_line,
            top_reasons=top_reasons,
            by_station=by_station,
            trend_last_months=trend,
            total_audits=total_audits,
            total_findings=total_findings,
            severity_breakdown=severity,
        )

    def _by_line(self, in_month) -> list[MonthlyReportLineStat]:
        defective_case = case((InspectionModel.result == "FAIL", 1), else_=0)
        rows = (
            self._session.query(
                ProductionLineModel.code,
                ProductionLineModel.name,
                func.count(InspectionModel.id),
                func.sum(defective_case),
            )
            .join(TVModel, TVModel.line_id == ProductionLineModel.id)
            .join(InspectionModel, InspectionModel.tv_id == TVModel.id)
            .filter(in_month)
            .group_by(ProductionLineModel.id, ProductionLineModel.code, ProductionLineModel.name)
            .order_by(func.sum(defective_case).desc())
            .all()
        )
        return [
            MonthlyReportLineStat(line_code=code, line_name=name, inspected=insp, defective=int(defv or 0))
            for code, name, insp, defv in rows
        ]

    def _top_reasons(self, in_month) -> list[MonthlyReportReasonStat]:
        rows = (
            self._session.query(DefectCategoryModel.name, func.count(InspectionModel.id))
            .join(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(in_month, InspectionModel.result == "FAIL")
            .group_by(DefectCategoryModel.name)
            .order_by(func.count(InspectionModel.id).desc())
            .limit(8)
            .all()
        )
        return [MonthlyReportReasonStat(reason=r, count=c) for r, c in rows]

    def _by_station(self, in_month) -> list[MonthlyReportStationStat]:
        rows = (
            self._session.query(DefectCategoryModel.code, func.count(InspectionModel.id))
            .join(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(in_month, InspectionModel.result == "FAIL")
            .group_by(DefectCategoryModel.code)
            .all()
        )
        totals: dict[str, int] = {}
        for code, count in rows:
            # DefectCategory kodları bizde "ISIM_SLUG_XXXX" şeklinde (rastgele 4 haneli
            # sonek ile) otomatik üretiliyor — bu yüzden tam eşleşme yerine, eşleme
            # tablosundaki anahtarla BAŞLAYIP başlamadığına bakıyoruz.
            station = next(
                (v for k, v in STATION_BY_CATEGORY_CODE.items() if code.startswith(k)),
                "Diğer",
            )
            totals[station] = totals.get(station, 0) + count
        return [
            MonthlyReportStationStat(station=s, count=c)
            for s, c in sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
        ]

    def _trend_last_months(self, month: str, months: int) -> list[MonthlyReportTrendPoint]:
        """Rapor ayı dahil, geriye dönük son `months` ayın tüm zamanlar trendinden bir kesit."""
        defective_case = case((InspectionModel.result == "FAIL", 1), else_=0)
        period_expr = func.to_char(InspectionModel.inspected_at, "YYYY-MM")
        rows = (
            self._session.query(period_expr.label("period"), func.count(InspectionModel.id), func.sum(defective_case))
            .filter(period_expr <= month)
            .group_by("period")
            .order_by("period")
            .all()
        )
        points = [MonthlyReportTrendPoint(period=p, inspected=i, defective=int(d or 0)) for p, i, d in rows]
        return points[-months:]

    def _audit_summary(self, month: str) -> tuple[int, int, MonthlyReportSeverityBreakdown]:
        total_audits = (
            self._session.query(func.count(AuditModel.id)).filter(AuditModel.audit_month == month).scalar() or 0
        )
        total_findings = (
            self._session.query(func.count(AuditFindingModel.id))
            .join(AuditModel, AuditModel.id == AuditFindingModel.audit_id)
            .filter(AuditModel.audit_month == month)
            .scalar()
            or 0
        )
        severity_rows = (
            self._session.query(AuditFindingModel.severity, func.count(AuditFindingModel.id))
            .join(AuditModel, AuditModel.id == AuditFindingModel.audit_id)
            .filter(AuditModel.audit_month == month)
            .group_by(AuditFindingModel.severity)
            .all()
        )
        severity_map = {sev: count for sev, count in severity_rows}
        breakdown = MonthlyReportSeverityBreakdown(
            low=severity_map.get("LOW", 0),
            medium=severity_map.get("MEDIUM", 0),
            high=severity_map.get("HIGH", 0),
            critical=severity_map.get("CRITICAL", 0),
        )
        return total_audits, total_findings, breakdown
