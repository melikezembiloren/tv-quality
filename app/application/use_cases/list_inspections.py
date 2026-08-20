from app.application.interfaces.inspection_repository import InspectionRepository
from app.application.dto.inspection_list_dto import InspectionListItem


class ListInspectionsUseCase:
    def __init__(self, repository: InspectionRepository):
        self._repository = repository

    def execute(
        self,
        date: str | None,
        end_date: str | None = None,
        production_line_id: int | None = None,
    ) -> list[InspectionListItem]:
        return self._repository.list_by_date(date, end_date, production_line_id)
