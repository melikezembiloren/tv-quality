from typing import Protocol
from app.application.dto.monthly_report_dto import MonthlyReportData


class MonthlyReportRepository(Protocol):
    """
    Salt-okunur read-model — üst yönetime sunulacak aylık özet PDF raporunun
    verisini tek bir sorgu setinde toplar (inspections/tvs/production_lines/
    defect_categories/audits/audit_findings).
    """

    def get_report(self, month: str) -> MonthlyReportData: ...
