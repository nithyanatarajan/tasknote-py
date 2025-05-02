# tests/common/test_timeutils.py

import re

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from src.common.timeutils import now_ist, now_utc, to_isoz


def test_now_ist():
    ist_time = now_ist()
    assert ist_time.tzname() == 'IST'
    assert isinstance(ist_time, datetime)


def test_now_utc():
    utc_time = now_utc()
    assert utc_time.tzname() == 'UTC'
    assert isinstance(utc_time, datetime)


ISO_Z_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$')


def test_to_isoz_test_utc_roundtrip():
    dt = datetime(2025, 5, 2, 12, 34, 56, 123456, tzinfo=UTC)

    result = to_isoz(dt)

    assert result == '2025-05-02T12:34:56.123456Z'
    assert ISO_Z_RE.match(result)


def test_to_isoz_non_utc_conversion():
    ist = ZoneInfo('Asia/Kolkata')  # +05:30
    # Same instant as the UTC dt above, expressed in IST
    dt = datetime(2025, 5, 2, 18, 4, 56, 123456, tzinfo=ist)

    result = to_isoz(dt)

    assert result == '2025-05-02T12:34:56.123456Z'
    assert ISO_Z_RE.match(result)
