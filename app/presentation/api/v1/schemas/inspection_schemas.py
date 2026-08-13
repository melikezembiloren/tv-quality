from datetime import datetime

from pydantic import BaseModel


class InspectionCreateRequest(BaseModel):
    serial_number: str
    production_line_id: int
    operator_pin: str
    result: str  # "PASS" ya da "FAIL"
    defect_reason: str | None = None


class InspectionResponse(BaseModel):
    inspection_id: int
    tv_id: int
    tv_status: str
    result: str
    defect_reason: str | None


class InspectionListItemResponse(BaseModel):
    id: int
    tv_serial_number: str
    result: str
    defect_reason: str | None
    inspector_name: str
    inspected_at: datetime
