from pydantic import BaseModel


class DefectCategoryCreateRequest(BaseModel):
    name: str
    description: str | None = None


class DefectCategoryResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
