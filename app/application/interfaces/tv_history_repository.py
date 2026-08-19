from typing import Protocol
from app.application.dto.tv_history_dto import TvHistoryOutput


class TvHistoryRepository(Protocol):
    """
    Salt-okunur read-model — bir TV'nin (hattı + tüm kontrol geçmişi) tek seferde
    okunması için var. tvs/inspections/production_lines/defect_categories tablolarını
    okur, hiçbirini değiştirmez.
    """

    def get_by_serial_number(self, serial_number: str) -> TvHistoryOutput | None: ...
