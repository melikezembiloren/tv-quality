from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_defect_dashboard_summary_use_case
from app.presentation.api.v1.schemas.defect_dashboard_schemas import (
    DefectDashboardSummaryResponse,
    PeriodStatResponse,
    ReasonFrequencyResponse,
    CategorySliceResponse,
)

router = APIRouter(prefix="/defect-dashboard", tags=["Quality Check"])


@router.get("/summary", response_model=DefectDashboardSummaryResponse)
def get_summary(
    production_line_id: int | None = Query(default=None, description="Verilirse sadece o hattın verisi, boşsa tüm hatlar"),
    start_date: date | None = Query(default=None, description="Verilirse tüm grafikler bu tarihten (dahil) itibaren"),
    end_date: date | None = Query(default=None, description="Verilirse tüm grafikler bu tarihe (dahil) kadar — boşsa start_date tek gün sayılır"),
    db: Session = Depends(get_db),
):
    use_case = get_defect_dashboard_summary_use_case(db)
    r = use_case.execute(production_line_id, start_date, end_date)

    to_stat = lambda items: [PeriodStatResponse(period=i.period, inspected=i.inspected, defective=i.defective) for i in items]
    to_slices = lambda items: [CategorySliceResponse(category_name=i.category_name, count=i.count) for i in items]

    return DefectDashboardSummaryResponse(
        total_inspected=r.total_inspected,
        total_defective=r.total_defective,
        overall_defect_rate=r.overall_defect_rate,
        daily=to_stat(r.daily),
        weekly=to_stat(r.weekly),
        monthly=to_stat(r.monthly),
        top_reasons=[ReasonFrequencyResponse(reason=t.reason, count=t.count) for t in r.top_reasons],
        category_breakdown_daily=to_slices(r.category_breakdown_daily),
        category_breakdown_weekly=to_slices(r.category_breakdown_weekly),
        category_breakdown_monthly=to_slices(r.category_breakdown_monthly),
        category_breakdown_range=to_slices(r.category_breakdown_range),
    )
