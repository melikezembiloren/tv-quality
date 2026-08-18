from app.application.interfaces.defect_category_repository import DefectCategoryRepository
from app.application.dto.defect_category_dto import DefectCategoryOutput


class ListDefectCategoriesUseCase:
    def __init__(self, repository: DefectCategoryRepository):
        self._repository = repository

    def execute(self) -> list[DefectCategoryOutput]:
        categories = self._repository.list_all()
        return [
            DefectCategoryOutput(id=c.id, code=c.code, name=c.name, description=c.description)
            for c in categories
        ]
