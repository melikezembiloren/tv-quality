from app.application.interfaces.quality_dashboard_repository import QualityDashboardRepository
from app.application.dto.quality_dashboard_dto import QualityDashboardSummary


class GetQualityDashboardSummaryUseCase:
    def __init__(self, repository: QualityDashboardRepository):
        self._repository = repository

    def execute(self) -> QualityDashboardSummary:
        return self._repository.get_summary()
