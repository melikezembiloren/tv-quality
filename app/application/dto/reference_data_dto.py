from dataclasses import dataclass


@dataclass
class ProductionLineOption:
    id: int
    code: str
    name: str


@dataclass
class UserOption:
    id: int
    username: str
    full_name: str
