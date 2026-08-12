from typing import Generator

from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.sqlalchemy_tv_repository import SqlAlchemyTVRepository
from app.infrastructure.repositories.sqlalchemy_audit_repository import SqlAlchemyAuditRepository
from app.infrastructure.repositories.sqlalchemy_quality_dashboard_repository import (
    SqlAlchemyQualityDashboardRepository,
)
from app.application.use_cases.register_tv import RegisterTVUseCase
from app.application.use_cases.create_audit import CreateAuditUseCase
from app.application.use_cases.get_audit_detail import GetAuditDetailUseCase
from app.application.use_cases.list_audits import ListAuditsUseCase
from app.application.use_cases.get_quality_dashboard_summary import GetQualityDashboardSummaryUseCase


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


def get_create_audit_use_case(db: Session) -> CreateAuditUseCase:
    repository = SqlAlchemyAuditRepository(db)
    return CreateAuditUseCase(repository)


def get_audit_detail_use_case(db: Session) -> GetAuditDetailUseCase:
    repository = SqlAlchemyAuditRepository(db)
    return GetAuditDetailUseCase(repository)


def get_list_audits_use_case(db: Session) -> ListAuditsUseCase:
    repository = SqlAlchemyAuditRepository(db)
    return ListAuditsUseCase(repository)


def get_quality_dashboard_summary_use_case(db: Session) -> GetQualityDashboardSummaryUseCase:
    repository = SqlAlchemyQualityDashboardRepository(db)
    return GetQualityDashboardSummaryUseCase(repository)
