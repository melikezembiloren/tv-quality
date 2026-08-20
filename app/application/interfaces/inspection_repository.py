from typing import Protocol
from app.domain.entities.inspection import Inspection
from app.application.dto.inspection_list_dto import InspectionListItem


class InspectionRepository(Protocol):
    def save(self, inspection: Inspection) -> Inspection: ...

    def list_by_date(
        self,
        date: str | None,
        end_date: str | None = None,
        production_line_id: int | None = None,
    ) -> list[InspectionListItem]:
        """date, 'YYYY-MM-DD' formatında — None ise bugünün kayıtları döner.
        end_date verilirse date..end_date arası (dahil) tüm kayıtlar döner;
        end_date verilmezse sadece date gününün kayıtları döner.
        production_line_id verilirse, sadece o hatta ait TV'lerin kayıtları döner."""
        ...
