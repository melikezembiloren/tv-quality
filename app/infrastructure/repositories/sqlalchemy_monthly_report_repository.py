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

    def get_report(self, month: str, production_line_id: int | None = None) -> MonthlyReportData:
        start, end = _month_bounds(month)
        in_month = (InspectionModel.inspected_at >= start) & (InspectionModel.inspected_at < end)

        total_q = self._session.query(func.count(InspectionModel.id)).filter(in_month)
        total_q = self._with_line_filter(total_q, production_line_id)
        total_inspected = total_q.scalar() or 0

        defective_q = (
            self._session.query(func.count(InspectionModel.id))
            .filter(in_month, InspectionModel.result == "FAIL")
        )
        defective_q = self._with_line_filter(defective_q, production_line_id)
        total_defective = defective_q.scalar() or 0

        defect_rate = round(total_defective / total_inspected * 100, 2) if total_inspected else 0.0

        by_line = self._by_line(in_month, production_line_id)
        top_reasons = self._top_reasons(in_month, production_line_id)
        by_station = self._by_station(in_month, production_line_id)
        trend = self._trend_last_months(month, months=6, production_line_id=production_line_id)
        total_audits, total_findings, severity = self._audit_summary(month, production_line_id)

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

    def _with_line_filter(self, query, production_line_id: int | None):
        """InspectionModel'e dayanan bir sorguya, verildiyse tvs üzerinden hat filtresi ekler."""
        if production_line_id is None:
            return query
        return query.join(TVModel, TVModel.id == InspectionModel.tv_id).filter(
            TVModel.line_id == production_line_id
        )

    def _by_line(self, in_month, production_line_id: int | None) -> list[MonthlyReportLineStat]:
        defective_case = case((InspectionModel.result == "FAIL", 1), else_=0)
        query = (
            self._session.query(
                ProductionLineModel.code,
                ProductionLineModel.name,
                func.count(InspectionModel.id),
                func.sum(defective_case),
            )
            .join(TVModel, TVModel.line_id == ProductionLineModel.id)
            .join(InspectionModel, InspectionModel.tv_id == TVModel.id)
            .filter(in_month)
        )
        if production_line_id is not None:
            query = query.filter(ProductionLineModel.id == production_line_id)
        rows = (
            query.group_by(ProductionLineModel.id, ProductionLineModel.code, ProductionLineModel.name)
            .order_by(func.sum(defective_case).desc())
            .all()
        )
        return [
            MonthlyReportLineStat(line_code=code, line_name=name, inspected=insp, defective=int(defv or 0))
            for code, name, insp, defv in rows
        ]

    def _top_reasons(self, in_month, production_line_id: int | None) -> list[MonthlyReportReasonStat]:
        query = (
            self._session.query(DefectCategoryModel.name, func.count(InspectionModel.id))
            .join(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(in_month, InspectionModel.result == "FAIL")
        )
        query = self._with_line_filter(query, production_line_id)
        rows = query.group_by(DefectCategoryModel.name).order_by(func.count(InspectionModel.id).desc()).limit(8).all()
        return [MonthlyReportReasonStat(reason=r, count=c) for r, c in rows]

    def _by_station(self, in_month, production_line_id: int | None) -> list[MonthlyReportStationStat]:
        query = (
            self._session.query(DefectCategoryModel.code, func.count(InspectionModel.id))
            .join(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(in_month, InspectionModel.result == "FAIL")
        )
        query = self._with_line_filter(query, production_line_id)
        rows = query.group_by(DefectCategoryModel.code).all()
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

    def _trend_last_months(self, month: str, months: int, production_line_id: int | None = None) -> list[MonthlyReportTrendPoint]:
        """Rapor ayı dahil, geriye dönük son `months` ayın tüm zamanlar trendinden bir kesit."""
        defective_case = case((InspectionModel.result == "FAIL", 1), else_=0)
        period_expr = func.to_char(InspectionModel.inspected_at, "YYYY-MM")
        query = (
            self._session.query(period_expr.label("period"), func.count(InspectionModel.id), func.sum(defective_case))
            .filter(period_expr <= month)
        )
        query = self._with_line_filter(query, production_line_id)
        rows = query.group_by("period").order_by("period").all()
        points = [MonthlyReportTrendPoint(period=p, inspected=i, defective=int(d or 0)) for p, i, d in rows]
        return points[-months:]

    def _audit_summary(self, month: str, production_line_id: int | None = None) -> tuple[int, int, MonthlyReportSeverityBreakdown]:
        audits_q = self._session.query(func.count(AuditModel.id)).filter(AuditModel.audit_month == month)
        findings_q = (
            self._session.query(func.count(AuditFindingModel.id))
            .join(AuditModel, AuditModel.id == AuditFindingModel.audit_id)
            .filter(AuditModel.audit_month == month)
        )
        severity_q = (
            self._session.query(AuditFindingModel.severity, func.count(AuditFindingModel.id))
            .join(AuditModel, AuditModel.id == AuditFindingModel.audit_id)
            .filter(AuditModel.audit_month == month)
        )
        if production_line_id is not None:
            audits_q = audits_q.filter(AuditModel.production_line_id == production_line_id)
            findings_q = findings_q.filter(AuditModel.production_line_id == production_line_id)
            severity_q = severity_q.filter(AuditModel.production_line_id == production_line_id)

        total_audits = audits_q.scalar() or 0
        total_findings = findings_q.scalar() or 0
        severity_rows = severity_q.group_by(AuditFindingModel.severity).all()

        severity_map = {sev: count for sev, count in severity_rows}
        breakdown = MonthlyReportSeverityBreakdown(
            low=severity_map.get("LOW", 0),
            medium=severity_map.get("MEDIUM", 0),
            high=severity_map.get("HIGH", 0),
            critical=severity_map.get("CRITICAL", 0),
        )
        return total_audits, total_findings, breakdown
