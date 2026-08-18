from datetime import date as date_cls

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import (
    get_db,
    get_record_inspection_use_case,
    get_list_inspections_use_case,
)
from app.presentation.api.v1.schemas.inspection_schemas import (
    InspectionCreateRequest,
    InspectionResponse,
    InspectionListItemResponse,
)
from app.application.dto.record_inspection_dto import RecordInspectionInput
from app.domain.exceptions import DomainError
from app.presentation.pdf.daily_report import generate_daily_report_pdf

# Bilinçli olarak /tvs, /audits gibi diğer köklerle hiç kesişmiyor —
# üretim hattı ekranlarından bağımsız kalite kontrol akışı.
router = APIRouter(prefix="/inspections", tags=["Quality Check"])


@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def record_inspection(payload: InspectionCreateRequest, db: Session = Depends(get_db)):
    use_case = get_record_inspection_use_case(db)

    input_data = RecordInspectionInput(
        serial_number=payload.serial_number,
        production_line_id=payload.production_line_id,
        result=payload.result,
        defect_category_id=payload.defect_category_id,
        defect_reason=payload.defect_reason,
    )

    try:
        result = use_case.execute(input_data)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return InspectionResponse(
        inspection_id=result.inspection_id,
        tv_id=result.tv_id,
        tv_status=result.tv_status,
        result=result.result,
        defect_category_id=result.defect_category_id,
        defect_reason=result.defect_reason,
    )


@router.get("", response_model=list[InspectionListItemResponse])
def list_inspections(date: str | None = Query(default=None, description="YYYY-MM-DD, boşsa bugün"), db: Session = Depends(get_db)):
    use_case = get_list_inspections_use_case(db)
    results = use_case.execute(date)
    return [
        InspectionListItemResponse(
            id=r.id,
            tv_serial_number=r.tv_serial_number,
            result=r.result,
            defect_category_name=r.defect_category_name,
            defect_reason=r.defect_reason,
            inspected_at=r.inspected_at,
        )
        for r in results
    ]


@router.get("/export")
def export_daily_report(date: str | None = Query(default=None, description="YYYY-MM-DD, boşsa bugün"), db: Session = Depends(get_db)):
    """Günlük kayıt listesini, Tectone logolu resmi bir PDF rapor olarak indirir."""
    report_date = date or date_cls.today().isoformat()

    use_case = get_list_inspections_use_case(db)
    results = use_case.execute(report_date)

    pdf_bytes = generate_daily_report_pdf(report_date, results)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="gunluk-kalite-raporu-{report_date}.pdf"'},
    )
