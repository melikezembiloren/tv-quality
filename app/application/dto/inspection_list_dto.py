from dataclasses import dataclass
from datetime import datetime


@dataclass
class InspectionListItem:
    id: int
    tv_serial_number: str
    result: str
    defect_reason: str | None
    inspector_name: str
    inspected_at: datetime
