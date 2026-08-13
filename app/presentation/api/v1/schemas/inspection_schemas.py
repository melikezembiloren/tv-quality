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
