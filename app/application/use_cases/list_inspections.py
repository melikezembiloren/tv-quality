from app.application.interfaces.inspection_repository import InspectionRepository
from app.application.dto.inspection_list_dto import InspectionListItem


class ListInspectionsUseCase:
    def __init__(self, repository: InspectionRepository):
        self._repository = repository

    def execute(self, date: str | None) -> list[InspectionListItem]:
        return self._repository.list_by_date(date)
