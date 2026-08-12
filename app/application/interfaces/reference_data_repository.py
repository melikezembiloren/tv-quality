from typing import Protocol
from app.application.dto.reference_data_dto import ProductionLineOption, UserOption


class ReferenceDataRepository(Protocol):
    """Form dropdown'ları gibi salt-okunur, basit referans listeleri için."""

    def list_production_lines(self) -> list[ProductionLineOption]: ...
    def list_users(self) -> list[UserOption]: ...
