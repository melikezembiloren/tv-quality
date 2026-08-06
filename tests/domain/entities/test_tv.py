import pytest
from app.domain.entities.tv import TV
from app.domain.exceptions import InvalidTvStateError


def make_tv(status: str = "IN_PRODUCTION") -> TV:
    return TV(id=1, serial_number="TV12345678", line_id=1, status=status)


def test_scrap_succeeds_when_tv_is_fail():
    tv = make_tv(status="FAIL")
    tv.mark_scrap()
    assert tv.status == "SCRAP"


def test_scrap_fails_when_tv_is_not_fail():
    tv = make_tv(status="PASS")
    # TODO: tv.mark_scrap() çağrıldığında InvalidTvStateError fırladığını doğrula
    # ipucu: pytest.raises(InvalidTvStateError) kullan
    pass


def test_rework_succeeds_when_tv_is_fail():
    tv = make_tv(status="FAIL")
    # TODO
    pass


def test_rework_fails_when_tv_is_not_fail():
    tv = make_tv(status="PASS")
    # TODO
    pass
