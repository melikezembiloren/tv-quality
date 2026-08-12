from pydantic import BaseModel


class ProductionLineOptionResponse(BaseModel):
    id: int
    code: str
    name: str


class UserOptionResponse(BaseModel):
    id: int
    username: str
    full_name: str


class AuditFormReferenceDataResponse(BaseModel):
    production_lines: list[ProductionLineOptionResponse]
    users: list[UserOptionResponse]
