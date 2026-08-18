from dataclasses import dataclass


@dataclass
class CreateDefectCategoryInput:
    name: str
    description: str | None = None


@dataclass
class DefectCategoryOutput:
    id: int
    code: str
    name: str
    description: str | None
