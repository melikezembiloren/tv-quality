from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_register_tv_use_case
from app.presentation.api.v1.schemas.tv_schemas import TVCreateRequest, TVResponse
from app.application.dto.register_tv_dto import RegisterTVInput
from app.application.use_cases.register_tv import DuplicateSerialNumberError

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
