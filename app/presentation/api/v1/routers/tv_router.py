from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_register_tv_use_case, get_tv_history_use_case
from app.presentation.api.v1.schemas.tv_schemas import (
    TVCreateRequest,
    TVResponse,
    TvHistoryResponse,
    TvHistoryInspectionResponse,
)
from app.application.dto.register_tv_dto import RegisterTVInput
from app.application.use_cases.register_tv import DuplicateSerialNumberError
from app.application.use_cases.get_tv_history import TvNotFoundError

router = APIRouter(prefix="/tvs", tags=["TV"])


@router.post("", response_model=TVResponse, status_code=status.HTTP_201_CREATED)
def register_tv(payload: TVCreateRequest, db: Session = Depends(get_db)):
    use_case = get_register_tv_use_case(db)

    input_data = RegisterTVInput(
        serial_number=payload.serial_number,
        line_id=payload.line_id,
        product_model_id=payload.product_model_id,
    )

    try:
        result = use_case.execute(input_data)
    except DuplicateSerialNumberError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return TVResponse(id=result.id, serial_number=result.serial_number, status=result.status)


@router.get("/{serial_number}/history", response_model=TvHistoryResponse)
def get_tv_history(serial_number: str, db: Session = Depends(get_db)):
    """Bir TV'nin seri numarasına göre üretim hattı + tüm kontrol geçmişini döner."""
    use_case = get_tv_history_use_case(db)
    try:
        result = use_case.execute(serial_number)
    except TvNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return TvHistoryResponse(
        tv_id=result.tv_id,
        serial_number=result.serial_number,
        line_code=result.line_code,
        line_name=result.line_name,
        status=result.status,
        created_at=result.created_at,
        inspections=[
            TvHistoryInspectionResponse(
                id=i.id,
                result=i.result,
                defect_category_name=i.defect_category_name,
                defect_reason=i.defect_reason,
                inspected_at=i.inspected_at,
            )
            for i in result.inspections
        ],
    )
