from dataclasses import dataclass


@dataclass
class RecordInspectionInput:
    serial_number: str
    production_line_id: int
    result: str  # "PASS" ya da "FAIL"
    defect_category_id: int | None = None
    defect_reason: str | None = None  # ek açıklama, opsiyonel


@dataclass
class RecordInspectionOutput:
    inspection_id: int
    tv_id: int
    tv_status: str
    result: str
    defect_category_id: int | None
    defect_reason: str | None
