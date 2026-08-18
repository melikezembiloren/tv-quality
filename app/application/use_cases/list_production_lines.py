from app.application.interfaces.reference_data_repository import ReferenceDataRepository
from app.application.dto.reference_data_dto import ProductionLineOption


class ListProductionLinesUseCase:
    def __init__(self, repository: ReferenceDataRepository):
        self._repository = repository

    def execute(self) -> list[ProductionLineOption]:
        return self._repository.list_production_lines()
