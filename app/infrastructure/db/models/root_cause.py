from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class RootCauseModel(Base):
    __tablename__ = "root_causes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
