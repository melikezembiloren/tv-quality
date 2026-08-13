from app.domain.entities.tv import TV
from app.domain.entities.inspection import Inspection
from app.application.interfaces.tv_repository import TVRepository
from app.application.interfaces.operator_repository import OperatorRepository
from app.application.interfaces.inspection_repository import InspectionRepository
from app.application.dto.record_inspection_dto import RecordInspectionInput, RecordInspectionOutput


class InvalidOperatorPinError(Exception):
    pass


class RecordInspectionUseCase:
    """
    Kalite kontrol ekranından gelen 'bu TV OK mi, hatalı mı' kaydını işler.
    Üretim hattı ekranından (RegisterTV/rework akışı) bağımsız çalışır —
    TV daha önce sistemde yoksa burada ilk kez (sadece hat bilgisiyle) oluşturulur.
    """

    def __init__(
        self,
        tv_repository: TVRepository,
        operator_repository: OperatorRepository,
        inspection_repository: InspectionRepository,
    ):
        self._tv_repository = tv_repository
        self._operator_repository = operator_repository
        self._inspection_repository = inspection_repository

    def execute(self, input_data: RecordInspectionInput) -> RecordInspectionOutput:
        operator = self._operator_repository.get_by_pin(input_data.operator_pin)
        if operator is None:
            raise InvalidOperatorPinError("PIN tanınmadı")

        tv = self._tv_repository.get_by_serial_number(input_data.serial_number)
        if tv is None:
            tv = TV(id=None, serial_number=input_data.serial_number, line_id=input_data.production_line_id)
            tv = self._tv_repository.save(tv)

        if input_data.result == "FAIL":
            tv.mark_fail()  # domain kuralı: SCRAP olmuş bir TV FAIL olamaz
            tv = self._tv_repository.save(tv)

        inspection = Inspection(
            id=None,
            tv_id=tv.id,
            inspector_operator_id=operator.id,
            result=input_data.result,
            defect_reason=input_data.defect_reason,
        )
        saved_inspection = self._inspection_repository.save(inspection)

        return RecordInspectionOutput(
            inspection_id=saved_inspection.id,
            tv_id=tv.id,
            tv_status=tv.status,
            result=saved_inspection.result,
            defect_reason=saved_inspection.defect_reason,
        )
