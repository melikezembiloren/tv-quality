from typing import Generator

from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.sqlalchemy_tv_repository import SqlAlchemyTVRepository
from app.application.use_cases.register_tv import RegisterTVUseCase


def get_db() -> Generator[Session, None, None]:
    """Her istek için ayrı bir veritabanı session'ı açar, istek bitince kapatır."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_register_tv_use_case(db: Session) -> RegisterTVUseCase:
    """Use case'i, gerçek repository ile 'birleştirir' (dependency injection)."""
    repository = SqlAlchemyTVRepository(db)
    return RegisterTVUseCase(repository)
