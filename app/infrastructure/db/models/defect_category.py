from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class DefectCategoryModel(Base):
    __tablename__ = "defect_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
