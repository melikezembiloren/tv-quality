from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TvHistoryInspectionItem:
    id: int
    result: str
    defect_category_name: str | None
    defect_reason: str | None
    inspected_at: datetime


@dataclass
class TvHistoryOutput:
    tv_id: int
    serial_number: str
    line_code: str
    line_name: str
    status: str
    created_at: datetime
    inspections: list[TvHistoryInspectionItem] = field(default_factory=list)
