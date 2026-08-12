from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import (
    get_db,
    get_create_audit_use_case,
    get_audit_detail_use_case,
    get_list_audits_use_case,
)
from app.presentation.api.v1.schemas.audit_schemas import (
    AuditCreateRequest,
    AuditResponse,
    FindingResponse,
    AuditSummaryResponse,
)
from app.application.dto.audit_dto import CreateAuditInput, FindingInput, ListAuditsInput
from app.application.use_cases.get_audit_detail import AuditNotFoundError
from app.domain.exceptions import DomainError

router = APIRouter(prefix="/audits", tags=["Audit"])


@router.post("", response_model=AuditResponse, status_code=status.HTTP_201_CREATED)
def create_audit(payload: AuditCreateRequest, db: Session = Depends(get_db)):
    use_case = get_create_audit_use_case(db)

    input_data = CreateAuditInput(
        production_line_id=payload.production_line_id,
        audited_by_user_id=payload.audited_by_user_id,
        audit_month=payload.audit_month,
        findings=[FindingInput(description=f.description, severity=f.severity) for f in payload.findings],
    )

    try:
        result = use_case.execute(input_data)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return AuditResponse(
        id=result.id,
        production_line_id=result.production_line_id,
        audited_by_user_id=result.audited_by_user_id,
        audit_month=result.audit_month,
        findings=[FindingResponse(id=f.id, description=f.description, severity=f.severity) for f in result.findings],
    )


@router.get("", response_model=list[AuditSummaryResponse])
def list_audits(
    production_line_id: int | None = Query(default=None),
    audit_month: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    use_case = get_list_audits_use_case(db)
    results = use_case.execute(ListAuditsInput(production_line_id=production_line_id, audit_month=audit_month))
    return [
        AuditSummaryResponse(
            id=r.id, production_line_id=r.production_line_id, audit_month=r.audit_month, finding_count=r.finding_count
        )
        for r in results
    ]


@router.get("/{audit_id}", response_model=AuditResponse)
def get_audit_detail(audit_id: int, db: Session = Depends(get_db)):
    use_case = get_audit_detail_use_case(db)
    try:
        result = use_case.execute(audit_id)
    except AuditNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return AuditResponse(
        id=result.id,
        production_line_id=result.production_line_id,
        audited_by_user_id=result.audited_by_user_id,
        audit_month=result.audit_month,
        findings=[FindingResponse(id=f.id, description=f.description, severity=f.severity) for f in result.findings],
    )
