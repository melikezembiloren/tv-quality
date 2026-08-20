from datetime import date

from app.application.interfaces.defect_dashboard_repository import DefectDashboardRepository
from app.application.dto.defect_dashboard_dto import DefectDashboardSummary


class GetDefectDashboardSummaryUseCase:
    def __init__(self, repository: DefectDashboardRepository):
        self._repository = repository

    def execute(
        self,
        production_line_id: int | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> DefectDashboardSummary:
        return self._repository.get_summary(production_line_id, start_date, end_date)
