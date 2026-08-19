from datetime import date as date_cls

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_monthly_report_use_case
from app.presentation.pdf.monthly_report_pdf import generate_monthly_report_pdf
from app.application.use_cases.get_monthly_report import InvalidReportMonthError

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly-summary")
def export_monthly_summary(
    month: str | None = Query(default=None, description="YYYY-MM, boşsa bu ay"),
    db: Session = Depends(get_db),
):
    """Üst yönetime sunulacak, tek sayfalık aylık kalite özet raporunu PDF olarak indirir."""
    report_month = month or date_cls.today().strftime("%Y-%m")

    use_case = get_monthly_report_use_case(db)
    try:
        data = use_case.execute(report_month)
    except InvalidReportMonthError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    pdf_bytes = generate_monthly_report_pdf(data)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="aylik-ozet-raporu-{report_month}.pdf"'},
    )
