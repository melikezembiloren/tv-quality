from datetime import date as date_cls

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import (
    get_db,
    get_monthly_report_use_case,
    get_list_production_lines_use_case,
)
from app.presentation.pdf.monthly_report_pdf import (
    generate_monthly_report_pdf,
    generate_monthly_report_pdf_by_line,
)
from app.application.use_cases.get_monthly_report import InvalidReportMonthError

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly-summary")
def export_monthly_summary(
    month: str | None = Query(default=None, description="YYYY-MM, boşsa bu ay"),
    production_line_id: int | None = Query(default=None, description="Verilirse sadece o hattın raporu, boşsa tüm hatlar"),
    db: Session = Depends(get_db),
):
    """Üst yönetime sunulacak aylık kalite özet raporunu (Tüm Hatlar ya da tek bir hat) PDF olarak indirir."""
    report_month = month or date_cls.today().strftime("%Y-%m")

    use_case = get_monthly_report_use_case(db)
    try:
        data = use_case.execute(report_month, production_line_id)
    except InvalidReportMonthError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    line_label = None
    filename_suffix = report_month
    if production_line_id is not None:
        lines = get_list_production_lines_use_case(db).execute()
        match = next((l for l in lines if l.id == production_line_id), None)
        if match:
            line_label = f"{match.code} — {match.name}"
            filename_suffix = f"{report_month}-{match.code}"

    pdf_bytes = generate_monthly_report_pdf(data, line_label=line_label)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="aylik-ozet-raporu-{filename_suffix}.pdf"'},
    )


@router.get("/monthly-summary-by-line")
def export_monthly_summary_by_line(
    month: str | None = Query(default=None, description="YYYY-MM, boşsa bu ay"),
    db: Session = Depends(get_db),
):
    """
    Üst yönetime tek belge olarak sunulacak, hat bazlı kırılımlı aylık rapor:
    ilk sayfa Tüm Hatlar özeti, ardından her üretim hattı için ayrı bir sayfa.
    """
    report_month = month or date_cls.today().strftime("%Y-%m")

    use_case = get_monthly_report_use_case(db)
    try:
        overall_data = use_case.execute(report_month, None)
    except InvalidReportMonthError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    lines = get_list_production_lines_use_case(db).execute()
    per_line = []
    for line in lines:
        line_data = use_case.execute(report_month, line.id)
        if line_data.total_inspected == 0:
            continue  # bu ay hiç kaydı olmayan hat için boş sayfa eklemeye gerek yok
        per_line.append((f"{line.code} — {line.name}", line_data))

    pdf_bytes = generate_monthly_report_pdf_by_line(overall_data, per_line)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="aylik-ozet-raporu-hat-bazli-{report_month}.pdf"'},
    )
