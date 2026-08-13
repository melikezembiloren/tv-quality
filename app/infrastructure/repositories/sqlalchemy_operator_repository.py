from sqlalchemy.orm import Session

from app.domain.entities.operator import Operator
from app.infrastructure.db.models.operator import OperatorModel


class SqlAlchemyOperatorRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_pin(self, pin_code: str) -> Operator | None:
        row = self._session.query(OperatorModel).filter(OperatorModel.pin_code == pin_code).first()
        if row is None:
            return None
        return Operator(id=row.id, pin_code=row.pin_code, first_name=row.first_name, last_name=row.last_name)
