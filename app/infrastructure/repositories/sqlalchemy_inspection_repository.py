from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.inspection import Inspection
from app.infrastructure.db.models.inspection import InspectionModel
from app.infrastructure.db.models.tv import TVModel
from app.infrastructure.db.models.defect_category import DefectCategoryModel
from app.application.dto.inspection_list_dto import InspectionListItem


class SqlAlchemyInspectionRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, inspection: Inspection) -> Inspection:
        row = InspectionModel(
            tv_id=inspection.tv_id,
            result=inspection.result,
            defect_category_id=inspection.defect_category_id,
            defect_reason=inspection.defect_reason,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)

        return Inspection(
            id=row.id,
            tv_id=row.tv_id,
            result=row.result,
            defect_category_id=row.defect_category_id,
            defect_reason=row.defect_reason,
            inspected_at=row.inspected_at,
        )

    def list_by_date(self, date: str | None) -> list[InspectionListItem]:
        target_date = date or func.current_date()

        rows = (
            self._session.query(
                InspectionModel.id,
                TVModel.serial_number,
                InspectionModel.result,
                DefectCategoryModel.name,
                InspectionModel.defect_reason,
                InspectionModel.inspected_at,
            )
            .join(TVModel, TVModel.id == InspectionModel.tv_id)
            .outerjoin(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(func.date(InspectionModel.inspected_at) == target_date)
            .order_by(InspectionModel.inspected_at.desc())
            .all()
        )

        return [
            InspectionListItem(
                id=r[0],
                tv_serial_number=r[1],
                result=r[2],
                defect_category_name=r[3],
                defect_reason=r[4],
                inspected_at=r[5],
            )
            for r in rows
        ]
