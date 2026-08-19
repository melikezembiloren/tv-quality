from datetime import datetime

from pydantic import BaseModel


class TVCreateRequest(BaseModel):
    serial_number: str
    line_id: int
    product_model_id: int


class TVResponse(BaseModel):
    id: int
    serial_number: str
    status: str


class TvHistoryInspectionResponse(BaseModel):
    id: int
    result: str
    defect_category_name: str | None
    defect_reason: str | None
    inspected_at: datetime


class TvHistoryResponse(BaseModel):
    tv_id: int
    serial_number: str
    line_code: str
    line_name: str
    status: str
    created_at: datetime
    inspections: list[TvHistoryInspectionResponse]
