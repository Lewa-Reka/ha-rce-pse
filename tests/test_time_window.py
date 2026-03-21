from datetime import datetime

from custom_components.rce_pse.time_window import (
    is_now_in_window,
    is_search_end_end_of_day,
    is_valid_quarter_step,
    normalize_hhmm,
    parse_pse_dtime,
    period_bounds_for_record,
    period_overlaps_search,
    search_window_exclusive_end,
)


def test_normalize_hhmm_from_dict():
    assert normalize_hhmm({"hours": 9, "minutes": 15, "seconds": 0}) == "09:15"


def test_is_valid_quarter_step():
    assert is_valid_quarter_step("10:15") is True
    assert is_valid_quarter_step("10:03") is False


def test_parse_pse_dtime_midnight_next_day():
    dt = parse_pse_dtime("2024-01-01 24:00:00")
    assert dt == datetime(2024, 1, 2, 0, 0, 0)


def test_parse_pse_dtime_normal():
    assert parse_pse_dtime("2024-01-01 10:15:00") == datetime(2024, 1, 1, 10, 15, 0)


def test_period_bounds_for_record():
    rec = {"dtime": "2024-01-01 10:15:00"}
    start, end = period_bounds_for_record(rec)
    assert start == datetime(2024, 1, 1, 10, 0, 0)
    assert end == datetime(2024, 1, 1, 10, 15, 0)


def test_search_end_eod():
    ex = search_window_exclusive_end("2024-01-01", "00:00")
    assert ex == datetime(2024, 1, 2, 0, 0, 0)


def test_search_end_fixed():
    ex = search_window_exclusive_end("2024-01-01", "10:00")
    assert ex == datetime(2024, 1, 1, 10, 0, 0)


def test_period_overlap():
    ps = datetime(2024, 1, 1, 9, 45)
    pe = datetime(2024, 1, 1, 10, 0)
    ss = datetime(2024, 1, 1, 0, 0)
    se = datetime(2024, 1, 1, 10, 0)
    assert period_overlaps_search(ps, pe, ss, se) is True


def test_is_now_in_window_end_exclusive():
    ws = datetime(2024, 1, 1, 9, 45)
    we = datetime(2024, 1, 1, 10, 0)
    assert is_now_in_window(datetime(2024, 1, 1, 9, 59), ws, we) is True
    assert is_now_in_window(datetime(2024, 1, 1, 10, 0), ws, we) is False


def test_is_search_end_end_of_day():
    assert is_search_end_end_of_day("00:00") is True
    assert is_search_end_end_of_day("0:00") is True
