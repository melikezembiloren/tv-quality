from dataclasses import dataclass

@dataclass
class ProductionLine:
    id: int | None
    code: str
    name: str
    daily_target: int
    weekly_target: int
    monthly_target: int