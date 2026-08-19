from sqlalchemy.orm import Session

from app.infrastructure.db.models.tv import TVModel
from app.infrastructure.db.models.production_line import ProductionLineModel
from app.infrastructure.db.models.inspection import InspectionModel
from app.infrastructure.db.models.defect_category import DefectCategoryModel
from app.application.dto.tv_history_dto import TvHistoryOutput, TvHistoryInspectionItem


class SqlAlchemyTvHistoryRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_serial_number(self, serial_number: str) -> TvHistoryOutput | None:
        tv_row = (
            self._session.query(TVModel, ProductionLineModel)
            .join(ProductionLineModel, ProductionLineModel.id == TVModel.line_id)
            .filter(TVModel.serial_number == serial_number)
            .first()
        )
        if tv_row is None:
            return None
        tv, line = tv_row

        inspection_rows = (
            self._session.query(InspectionModel, DefectCategoryModel.name)
            .outerjoin(DefectCategoryModel, DefectCategoryModel.id == InspectionModel.defect_category_id)
            .filter(InspectionModel.tv_id == tv.id)
            .order_by(InspectionModel.inspected_at.desc())
            .all()
        )

        return TvHistoryOutput(
            tv_id=tv.id,
            serial_number=tv.serial_number,
            line_code=line.code,
            line_name=line.name,
            status=tv.status,
            created_at=tv.created_at,
            inspections=[
                TvHistoryInspectionItem(
                    id=insp.id,
                    result=insp.result,
                    defect_category_name=cat_name,
                    defect_reason=insp.defect_reason,
                    inspected_at=insp.inspected_at,
                )
                for insp, cat_name in inspection_rows
            ],
        )
