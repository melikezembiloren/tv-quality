from app.domain.entities.tv import TV
from app.application.interfaces.tv_repository import TVRepository
from app.application.dto.register_tv_dto import RegisterTVInput, RegisterTVOutput


class DuplicateSerialNumberError(Exception):
    pass


class RegisterTVUseCase:
    def __init__(self, tv_repository: TVRepository):
        self._tv_repository = tv_repository

    def execute(self, input_data: RegisterTVInput) -> RegisterTVOutput:
        existing = self._tv_repository.get_by_serial_number(input_data.serial_number)
        if existing is not None:
            raise DuplicateSerialNumberError(
                f"{input_data.serial_number} zaten kayıtlı"
            )

        tv = TV(
            id=None,
            serial_number=input_data.serial_number,
            line_id=input_data.line_id,
            product_model_id=input_data.product_model_id,
        )

        saved_tv = self._tv_repository.save(tv)

        return RegisterTVOutput(
            id=saved_tv.id,
            serial_number=saved_tv.serial_number,
            status=saved_tv.status,
        )
