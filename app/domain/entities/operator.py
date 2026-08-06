from dataclasses import dataclass


@dataclass
class Operator:
    id: int | None
    first_name: str
    last_name: str
    pin_code: str