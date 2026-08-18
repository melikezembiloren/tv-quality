import re
import uuid

from app.domain.entities.defect_category import DefectCategory
from app.application.interfaces.defect_category_repository import DefectCategoryRepository
from app.application.dto.defect_category_dto import CreateDefectCategoryInput, DefectCategoryOutput


def _generate_code(name: str) -> str:
    """İsimden otomatik bir kod üretir — kullanıcı 'kod' diye bir şeyle uğraşmasın diye.
    Örn. 'Arka kapak oturmamış' -> 'ARKA_KAPAK_OTURMAMIS'. Çakışma ihtimaline karşı kısa bir ek eklenir."""
    ascii_map = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    slug = name.translate(ascii_map).upper()
    slug = re.sub(r"[^A-Z0-9]+", "_", slug).strip("_")[:40]
    suffix = uuid.uuid4().hex[:4].upper()
    return f"{slug}_{suffix}" if slug else f"HATA_{suffix}"


class CreateDefectCategoryUseCase:
    def __init__(self, repository: DefectCategoryRepository):
        self._repository = repository

    def execute(self, input_data: CreateDefectCategoryInput) -> DefectCategoryOutput:
        category = DefectCategory(
            id=None,
            code=_generate_code(input_data.name),
            name=input_data.name,
            description=input_data.description,
        )
        saved = self._repository.save(category)
        return DefectCategoryOutput(id=saved.id, code=saved.code, name=saved.name, description=saved.description)
