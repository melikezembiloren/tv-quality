from typing import Protocol
from app.domain.entities.tv import TV


class TVRepository(Protocol):
    def get_by_serial_number(self, serial_number: str) -> TV | None: ...
    def save(self, tv: TV) -> TV: ...
