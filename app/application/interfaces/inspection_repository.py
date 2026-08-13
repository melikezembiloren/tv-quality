from typing import Protocol
from app.domain.entities.inspection import Inspection


class InspectionRepository(Protocol):
    def save(self, inspection: Inspection) -> Inspection: ...
