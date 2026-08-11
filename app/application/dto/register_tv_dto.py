from dataclasses import dataclass


@dataclass
class RegisterTVInput:
    serial_number: str
    line_id: int
    product_model_id: int


@dataclass
class RegisterTVOutput:
    id: int
    serial_number: str
    status: str
