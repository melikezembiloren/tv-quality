from dataclasses import dataclass
from datetime import datetime


@dataclass
class InspectionListItem:
    id: int
    tv_serial_number: str
    result: str
    defect_category_name: str | None
    defect_reason: str | None
    inspected_at: datetime
