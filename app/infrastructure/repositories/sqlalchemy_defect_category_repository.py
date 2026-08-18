from sqlalchemy.orm import Session

from app.domain.entities.defect_category import DefectCategory
from app.infrastructure.db.models.defect_category import DefectCategoryModel


class SqlAlchemyDefectCategoryRepository:
    def __init__(self, session: Session):
        self._session = session

    def list_all(self) -> list[DefectCategory]:
        rows = self._session.query(DefectCategoryModel).order_by(DefectCategoryModel.name).all()
        return [self._to_entity(r) for r in rows]

    def save(self, category: DefectCategory) -> DefectCategory:
        row = DefectCategoryModel(code=category.code, name=category.name, description=category.description)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return self._to_entity(row)

    def get_by_id(self, category_id: int) -> DefectCategory | None:
        row = self._session.get(DefectCategoryModel, category_id)
        return self._to_entity(row) if row else None

    @staticmethod
    def _to_entity(row: DefectCategoryModel) -> DefectCategory:
        return DefectCategory(id=row.id, code=row.code, name=row.name, description=row.description)
