from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class ProductModelModel(Base):
    __tablename__ = "product_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    barcode_prefix: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
