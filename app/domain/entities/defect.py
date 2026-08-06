from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.exceptions import InvalidDefectStateError


@dataclass
class Defect:
    id: int | None
    tv_id: int
    defect_category_id: int
    found_by_operator_id: int
    root_cause_id: int | None = None
    status: str = "OPEN"
    found_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

def start_repair(self) -> None:
        if self.status != "OPEN":
            raise InvalidDefectStateError("Sadece OPEN durumundaki bir defect tamire alınabilir")
        self.status = "IN_REPAIR"

def mark_scrap(self) -> None:
        if self.status not in ("OPEN", "IN_REPAIR"):
            raise InvalidDefectStateError("Sadece OPEN ya da IN_REPAIR durumundaki bir defect SCRAP olabilir")
        self.status = "SCRAP"

def close(self) -> None:
        if self.status != "IN_REPAIR":
              raise InvalidDefectStateError("Sadece IN_REPAIR durumundaki bir defect CLOSED olabilir")
        self.status = "CLOSED"


     
        
