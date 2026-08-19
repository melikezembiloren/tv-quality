from typing import Generator

from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.sqlalchemy_tv_repository import SqlAlchemyTVRepository
from app.infrastructure.repositories.sqlalchemy_audit_repository import SqlAlchemyAuditRepository
from app.infrastructure.repositories.sqlalchemy_quality_dashboard_repository import (
    SqlAlchemyQualityDashboardRepository,
)
from app.infrastructure.repositories.sqlalchemy_reference_data_repository import (
    SqlAlchemyReferenceDataRepository,
)
from app.infrastructure.repositories.sqlalchemy_inspection_repository import SqlAlchemyInspectionRepository
from app.infrastructure.repositories.sqlalchemy_defect_dashboard_repository import (
    SqlAlchemyDefectDashboardRepository,
)
from app.infrastructure.repositories.sqlalchemy_defect_category_repository import (
    SqlAlchemyDefectCategoryRepository,
)
from app.infrastructure.repositories.sqlalchemy_tv_history_repository import SqlAlchemyTvHistoryRepository
from app.infrastructure.repositories.sqlalchemy_monthly_report_repository import (
    SqlAlchemyMonthlyReportRepository,
)
from app.application.use_cases.register_tv import RegisterTVUseCase
from app.application.use_cases.create_audit import CreateAuditUseCase
from app.application.use_cases.get_audit_detail import GetAuditDetailUseCase
from app.application.use_cases.list_audits import ListAuditsUseCase
from app.application.use_cases.get_quality_dashboard_summary import GetQualityDashboardSummaryUseCase
from app.application.use_cases.get_audit_form_reference_data import GetAuditFormReferenceDataUseCase
from app.application.use_cases.record_inspection import RecordInspectionUseCase
from app.application.use_cases.get_defect_dashboard_summary import GetDefectDashboardSummaryUseCase
from app.application.use_cases.list_inspections import ListInspectionsUseCase
from app.application.use_cases.list_defect_categories import ListDefectCategoriesUseCase
from app.application.use_cases.create_defect_category import CreateDefectCategoryUseCase
from app.application.use_cases.list_production_lines import ListProductionLinesUseCase
from app.application.use_cases.get_tv_history import GetTvHistoryUseCase
from app.application.use_cases.get_monthly_report import GetMonthlyReportUseCase


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


def get_audit_form_reference_data_use_case(db: Session) -> GetAuditFormReferenceDataUseCase:
    repository = SqlAlchemyReferenceDataRepository(db)
    return GetAuditFormReferenceDataUseCase(repository)


def get_record_inspection_use_case(db: Session) -> RecordInspectionUseCase:
    return RecordInspectionUseCase(
        tv_repository=SqlAlchemyTVRepository(db),
        inspection_repository=SqlAlchemyInspectionRepository(db),
    )


def get_defect_dashboard_summary_use_case(db: Session) -> GetDefectDashboardSummaryUseCase:
    repository = SqlAlchemyDefectDashboardRepository(db)
    return GetDefectDashboardSummaryUseCase(repository)


def get_list_inspections_use_case(db: Session) -> ListInspectionsUseCase:
    repository = SqlAlchemyInspectionRepository(db)
    return ListInspectionsUseCase(repository)


def get_list_defect_categories_use_case(db: Session) -> ListDefectCategoriesUseCase:
    repository = SqlAlchemyDefectCategoryRepository(db)
    return ListDefectCategoriesUseCase(repository)


def get_create_defect_category_use_case(db: Session) -> CreateDefectCategoryUseCase:
    repository = SqlAlchemyDefectCategoryRepository(db)
    return CreateDefectCategoryUseCase(repository)


def get_list_production_lines_use_case(db: Session) -> ListProductionLinesUseCase:
    repository = SqlAlchemyReferenceDataRepository(db)
    return ListProductionLinesUseCase(repository)


def get_tv_history_use_case(db: Session) -> GetTvHistoryUseCase:
    repository = SqlAlchemyTvHistoryRepository(db)
    return GetTvHistoryUseCase(repository)


def get_monthly_report_use_case(db: Session) -> GetMonthlyReportUseCase:
    repository = SqlAlchemyMonthlyReportRepository(db)
    return GetMonthlyReportUseCase(repository)
