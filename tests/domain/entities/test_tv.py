import pytest
from app.domain.entities.tv import TV
from app.domain.exceptions import InvalidTvStateError


def make_tv(status: str = "IN_PRODUCTION") -> TV:
    return TV(id=1, serial_number="TV12345678", line_id=1, status=status)


def test_scrap_succeeds_when_tv_is_fail():
    tv = make_tv(status="FAIL")
    tv.mark_scrap()
    assert tv.status == "SCRAP"

def test_fail_succeeds_when_tv_is_not_scrap():
    tv = make_tv(status="IN_PRODUCTION")
    tv.mark_fail()
    assert tv.status == "FAIL"


def test_fail_fails_when_tv_is_scrap():
    tv = make_tv(status="SCRAP")
    with pytest.raises(InvalidTvStateError):
        tv.mark_fail()