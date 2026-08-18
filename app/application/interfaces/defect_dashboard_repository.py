from typing import Protocol
from app.application.dto.defect_dashboard_dto import DefectDashboardSummary


class DefectDashboardRepository(Protocol):
    """
    Salt-okunur read-model — sadece inspections (ve hat filtresi verildiğinde
    tvs üzerinden hangi hatta ait olduğunu bulmak için) tabloları okur.
    """

    def get_summary(self, production_line_id: int | None = None) -> DefectDashboardSummary: ...
