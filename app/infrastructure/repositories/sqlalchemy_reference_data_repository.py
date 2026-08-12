from sqlalchemy.orm import Session

from app.infrastructure.db.models.production_line import ProductionLineModel
from app.infrastructure.db.models.user import UserModel
from app.application.dto.reference_data_dto import ProductionLineOption, UserOption


class SqlAlchemyReferenceDataRepository:
    def __init__(self, session: Session):
        self._session = session

    def list_production_lines(self) -> list[ProductionLineOption]:
        rows = self._session.query(ProductionLineModel).order_by(ProductionLineModel.code).all()
        return [ProductionLineOption(id=r.id, code=r.code, name=r.name) for r in rows]

    def list_users(self) -> list[UserOption]:
        rows = self._session.query(UserModel).order_by(UserModel.first_name).all()
        return [
            UserOption(id=r.id, username=r.username, full_name=f"{r.first_name} {r.last_name}")
            for r in rows
        ]
