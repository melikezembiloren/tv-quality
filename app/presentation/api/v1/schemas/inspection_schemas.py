from datetime import datetime

from pydantic import BaseModel


class InspectionCreateRequest(BaseModel):
    serial_number: str
    production_line_id: int
    result: str  # "PASS" ya da "FAIL"
    defect_category_id: int | None = None
    defect_reason: str | None = None  # ek açıklama, opsiyonel


class InspectionResponse(BaseModel):
    inspection_id: int
    tv_id: int
    tv_status: str
    result: str
    defect_category_id: int | None
    defect_reason: str | None


class InspectionListItemResponse(BaseModel):
    id: int
    tv_serial_number: str
    result: str
    defect_category_name: str | None
    defect_reason: str | None
    inspected_at: datetime
