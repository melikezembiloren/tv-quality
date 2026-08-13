from typing import Protocol
from app.domain.entities.operator import Operator


class OperatorRepository(Protocol):
    def get_by_pin(self, pin_code: str) -> Operator | None: ...
