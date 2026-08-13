from typing import Protocol
from app.application.dto.defect_dashboard_dto import DefectDashboardSummary


class DefectDashboardRepository(Protocol):
    """
    Salt-okunur read-model — sadece inspections tablosunu okur.
    tvs.line/model bilgisine bile dokunmaz; TV OK/Hatalı akışından tamamen bağımsız hesaplanır.
    """

    def get_summary(self) -> DefectDashboardSummary: ...
