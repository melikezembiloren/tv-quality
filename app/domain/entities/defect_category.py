from dataclasses import dataclass


@dataclass
class DefectCategory:
    id: int | None
    code: str
    name: str
    description: str | None = None