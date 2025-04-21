from datetime import datetime

from src.common.timeutils import now_ist, now_utc


def test_now_ist():
    ist_time = now_ist()
    assert ist_time.tzname() == 'IST'
    assert isinstance(ist_time, datetime)


def test_now_utc():
    utc_time = now_utc()
    assert utc_time.tzname() == 'UTC'
    assert isinstance(utc_time, datetime)
