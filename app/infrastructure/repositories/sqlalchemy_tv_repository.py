from sqlalchemy.orm import Session

from app.domain.entities.tv import TV
from app.infrastructure.db.models.tv import TVModel


class SqlAlchemyTVRepository:
    """TVRepository Protocol'ünün gerçek (PostgreSQL) implementasyonu."""

    def __init__(self, session: Session):
        self._session = session

    def get_by_serial_number(self, serial_number: str) -> TV | None:
        row = (
            self._session.query(TVModel)
            .filter(TVModel.serial_number == serial_number)
            .first()
        )
        if row is None:
            return None
        return self._to_entity(row)

    def save(self, tv: TV) -> TV:
        if tv.id is None:
            row = TVModel(
                serial_number=tv.serial_number,
                line_id=tv.line_id,
                product_model_id=tv.product_model_id,
                status=tv.status,
            )
            self._session.add(row)
        else:
            row = self._session.get(TVModel, tv.id)
            row.status = tv.status

        self._session.commit()
        self._session.refresh(row)
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row: TVModel) -> TV:
        """Infrastructure satırını (ORM) domain nesnesine çevirir."""
        return TV(
            id=row.id,
            serial_number=row.serial_number,
            line_id=row.line_id,
            product_model_id=row.product_model_id,
            status=row.status,
            created_at=row.created_at,
        )
