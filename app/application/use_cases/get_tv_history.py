from app.application.interfaces.tv_history_repository import TvHistoryRepository
from app.application.dto.tv_history_dto import TvHistoryOutput
from app.domain.exceptions import DomainError


class TvNotFoundError(DomainError):
    """Verilen seri numarasıyla eşleşen bir TV bulunamadığında fırlatılır."""
    pass


class GetTvHistoryUseCase:
    def __init__(self, repository: TvHistoryRepository):
        self._repository = repository

    def execute(self, serial_number: str) -> TvHistoryOutput:
        result = self._repository.get_by_serial_number(serial_number.strip())
        if result is None:
            raise TvNotFoundError(f"'{serial_number}' seri numaralı TV bulunamadı")
        return result
