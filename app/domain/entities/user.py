from dataclasses import dataclass

@dataclass
class User:
    id: int | None
    first_name: str
    last_name: str
    password_hash: str