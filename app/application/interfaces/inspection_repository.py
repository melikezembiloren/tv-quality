from typing import Protocol
from app.domain.entities.inspection import Inspection
from app.application.dto.inspection_list_dto import InspectionListItem


class InspectionRepository(Protocol):
    def save(self, inspection: Inspection) -> Inspection: ...

    def list_by_date(self, date: str | None) -> list[InspectionListItem]:
        """date, 'YYYY-MM-DD' formatında — None ise bugünün kayıtları döner."""
        ...
