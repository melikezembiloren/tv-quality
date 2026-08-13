from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import get_db, get_record_inspection_use_case
from app.presentation.api.v1.schemas.inspection_schemas import InspectionCreateRequest, InspectionResponse
from app.application.dto.record_inspection_dto import RecordInspectionInput
from app.application.use_cases.record_inspection import InvalidOperatorPinError
from app.domain.exceptions import DomainError

# Bilinçli olarak /tvs, /audits gibi diğer köklerle hiç kesişmiyor —
# üretim hattı ekranlarından bağımsız kalite kontrol akışı.
router = APIRouter(prefix="/inspections", tags=["Quality Check"])


@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def record_inspection(payload: InspectionCreateRequest, db: Session = Depends(get_db)):
    use_case = get_record_inspection_use_case(db)

    input_data = RecordInspectionInput(
        serial_number=payload.serial_number,
        production_line_id=payload.production_line_id,
        operator_pin=payload.operator_pin,
        result=payload.result,
        defect_reason=payload.defect_reason,
    )

    try:
        result = use_case.execute(input_data)
    except InvalidOperatorPinError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return InspectionResponse(
        inspection_id=result.inspection_id,
        tv_id=result.tv_id,
        tv_status=result.tv_status,
        result=result.result,
        defect_reason=result.defect_reason,
    )
