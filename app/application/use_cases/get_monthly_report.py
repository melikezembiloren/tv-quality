import re

from app.application.interfaces.monthly_report_repository import MonthlyReportRepository
from app.application.dto.monthly_report_dto import MonthlyReportData
from app.domain.exceptions import DomainError

_MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class InvalidReportMonthError(DomainError):
    """month, 'YYYY-MM' formatında değilse fırlatılır."""
    pass


class GetMonthlyReportUseCase:
    def __init__(self, repository: MonthlyReportRepository):
        self._repository = repository

    def execute(self, month: str) -> MonthlyReportData:
        if not _MONTH_PATTERN.match(month):
            raise InvalidReportMonthError(f"month 'YYYY-MM' formatında olmalı, alınan: {month!r}")
        return self._repository.get_report(month)
