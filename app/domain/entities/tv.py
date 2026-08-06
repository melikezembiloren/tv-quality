from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.exceptions import InvalidTvStateError


@dataclass
class TV:
    id: int | None
    serial_number: str          
    line_id: int
    status: str = "IN_PRODUCTION"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_fail(self) -> None:
        if self.status == "SCRAP":
            raise InvalidTvStateError("SCRAP TV FAIL olamaz")
        self.status = "FAIL"

    def mark_scrap(self) -> None:
        if self.status != "FAIL":
            raise InvalidTvStateError("FAIL olmadan SCRAP edilemez")
        self.status = "SCRAP"

    def mark_rework(self) -> None:
        if self.status != "FAIL":
            raise InvalidTvStateError("FAIL olmadan REWORK yapılamaz")
        self.status = "REWORK"

     
        
