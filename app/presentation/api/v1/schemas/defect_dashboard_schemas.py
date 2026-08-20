from pydantic import BaseModel


class PeriodStatResponse(BaseModel):
    period: str
    inspected: int
    defective: int


class ReasonFrequencyResponse(BaseModel):
    reason: str
    count: int


class CategorySliceResponse(BaseModel):
    category_name: str
    count: int


class DefectDashboardSummaryResponse(BaseModel):
    total_inspected: int
    total_defective: int
    overall_defect_rate: float
    daily: list[PeriodStatResponse]
    weekly: list[PeriodStatResponse]
    monthly: list[PeriodStatResponse]
    top_reasons: list[ReasonFrequencyResponse]
    category_breakdown_daily: list[CategorySliceResponse]
    category_breakdown_weekly: list[CategorySliceResponse]
    category_breakdown_monthly: list[CategorySliceResponse]
    category_breakdown_range: list[CategorySliceResponse]
