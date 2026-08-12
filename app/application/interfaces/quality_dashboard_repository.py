from typing import Protocol
from app.application.dto.quality_dashboard_dto import QualityDashboardSummary


class QualityDashboardRepository(Protocol):
    """
    Bu bir yazma (write) repository'si değil, salt-okunur bir 'read model' —
    dashboard'un ihtiyaç duyduğu agregasyonları doğrudan üretir. Bu yüzden
    domain entity değil, doğrudan raporlama DTO'su döndürür (kalite verisi
    üretim/TV tablolarına hiç dokunmadan, tamamen bağımsız hesaplanır).
    """

    def get_summary(self) -> QualityDashboardSummary: ...
