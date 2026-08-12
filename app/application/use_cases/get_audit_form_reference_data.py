from dataclasses import dataclass

from app.application.interfaces.reference_data_repository import ReferenceDataRepository
from app.application.dto.reference_data_dto import ProductionLineOption, UserOption


@dataclass
class AuditFormReferenceData:
    production_lines: list[ProductionLineOption]
    users: list[UserOption]


class GetAuditFormReferenceDataUseCase:
    def __init__(self, repository: ReferenceDataRepository):
        self._repository = repository

    def execute(self) -> AuditFormReferenceData:
        return AuditFormReferenceData(
            production_lines=self._repository.list_production_lines(),
            users=self._repository.list_users(),
        )
