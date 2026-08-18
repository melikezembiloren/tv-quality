from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.presentation.api.v1.dependencies import (
    get_db,
    get_list_defect_categories_use_case,
    get_create_defect_category_use_case,
)
from app.presentation.api.v1.schemas.defect_category_schemas import (
    DefectCategoryCreateRequest,
    DefectCategoryResponse,
)
from app.application.dto.defect_category_dto import CreateDefectCategoryInput

router = APIRouter(prefix="/defect-categories", tags=["Quality Check"])


@router.get("", response_model=list[DefectCategoryResponse])
def list_defect_categories(db: Session = Depends(get_db)):
    use_case = get_list_defect_categories_use_case(db)
    results = use_case.execute()
    return [
        DefectCategoryResponse(id=c.id, code=c.code, name=c.name, description=c.description) for c in results
    ]


@router.post("", response_model=DefectCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_defect_category(payload: DefectCategoryCreateRequest, db: Session = Depends(get_db)):
    use_case = get_create_defect_category_use_case(db)
    result = use_case.execute(CreateDefectCategoryInput(name=payload.name, description=payload.description))
    return DefectCategoryResponse(id=result.id, code=result.code, name=result.name, description=result.description)
