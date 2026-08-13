from sqlalchemy.orm import Session

from app.domain.entities.inspection import Inspection
from app.infrastructure.db.models.inspection import InspectionModel


class SqlAlchemyInspectionRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, inspection: Inspection) -> Inspection:
        row = InspectionModel(
            tv_id=inspection.tv_id,
            inspector_operator_id=inspection.inspector_operator_id,
            result=inspection.result,
            defect_reason=inspection.defect_reason,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)

        return Inspection(
            id=row.id,
            tv_id=row.tv_id,
            inspector_operator_id=row.inspector_operator_id,
            result=row.result,
            defect_reason=row.defect_reason,
            inspected_at=row.inspected_at,
        )
