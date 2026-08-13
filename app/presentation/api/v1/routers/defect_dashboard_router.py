from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_defect_dashboard_summary_use_case
from app.presentation.api.v1.schemas.defect_dashboard_schemas import (
    DefectDashboardSummaryResponse,
    PeriodStatResponse,
    ReasonFrequencyResponse,
)

router = APIRouter(prefix="/defect-dashboard", tags=["Quality Check"])


@router.get("/summary", response_model=DefectDashboardSummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    use_case = get_defect_dashboard_summary_use_case(db)
    r = use_case.execute()

    to_stat = lambda items: [PeriodStatResponse(period=i.period, inspected=i.inspected, defective=i.defective) for i in items]

    return DefectDashboardSummaryResponse(
        total_inspected=r.total_inspected,
        total_defective=r.total_defective,
        overall_defect_rate=r.overall_defect_rate,
        daily=to_stat(r.daily),
        weekly=to_stat(r.weekly),
        monthly=to_stat(r.monthly),
        top_reasons=[ReasonFrequencyResponse(reason=t.reason, count=t.count) for t in r.top_reasons],
    )
