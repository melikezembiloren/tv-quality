from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import (
    get_db,
    get_audit_form_reference_data_use_case,
    get_list_production_lines_use_case,
)
from app.presentation.api.v1.schemas.reference_data_schemas import (
    AuditFormReferenceDataResponse,
    ProductionLineOptionResponse,
    UserOptionResponse,
)

router = APIRouter(prefix="/reference-data", tags=["Reference Data"])


@router.get("/audit-form", response_model=AuditFormReferenceDataResponse)
def get_audit_form_reference_data(db: Session = Depends(get_db)):
    use_case = get_audit_form_reference_data_use_case(db)
    result = use_case.execute()
    return AuditFormReferenceDataResponse(
        production_lines=[
            ProductionLineOptionResponse(id=l.id, code=l.code, name=l.name) for l in result.production_lines
        ],
        users=[UserOptionResponse(id=u.id, username=u.username, full_name=u.full_name) for u in result.users],
    )


@router.get("/production-lines", response_model=list[ProductionLineOptionResponse])
def list_production_lines(db: Session = Depends(get_db)):
    use_case = get_list_production_lines_use_case(db)
    lines = use_case.execute()
    return [ProductionLineOptionResponse(id=l.id, code=l.code, name=l.name) for l in lines]
