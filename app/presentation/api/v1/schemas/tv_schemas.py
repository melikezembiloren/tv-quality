from pydantic import BaseModel


class TVCreateRequest(BaseModel):
    serial_number: str
    line_id: int
    product_model_id: int


class TVResponse(BaseModel):
    id: int
    serial_number: str
    status: str
