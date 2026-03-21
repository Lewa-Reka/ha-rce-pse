from __future__ import annotations

import re
from datetime import datetime, time, timedelta


HHMM_PATTERN = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")
MINUTES_STEP = 15


def duration_minutes_from_hhmm(hhmm: str) -> int:
    s = normalize_hhmm(hhmm)
    if s == "24:00":
        return 24 * 60
    h, m = map(int, s.split(":"))
    return h * 60 + m


def is_valid_duration_hhmm(hhmm: str) -> bool:
    s = normalize_hhmm(hhmm)
    if s == "24:00":
        return True
    if not HHMM_PATTERN.match(s):
        return False
    m = minutes_from_midnight(s)
    return m >= MINUTES_STEP and m % MINUTES_STEP == 0


def normalize_hhmm(value: str | dict[str, int] | None) -> str:
    if value is None:
        return "00:00"
    if isinstance(value, dict):
        h = int(value.get("hours", 0))
        m = int(value.get("minutes", 0))
        s = int(value.get("seconds", 0))
        if s >= 30:
            m += 1
        return f"{h:02d}:{m:02d}"
    s = str(value).strip()
    if not s:
        return "00:00"
    if s in ("24:00", "24:00:00"):
        return "24:00"
    if HHMM_PATTERN.match(s):
        h, m = map(int, s.split(":"))
        return f"{h:02d}:{m:02d}"
    parts = s.replace(".", ":").split(":")
    if len(parts) >= 2:
        h = int(parts[0])
        m = int(parts[1])
        return f"{h:02d}:{m:02d}"
    return f"{int(s):02d}:00"


def minutes_from_midnight(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m


def is_valid_quarter_step(hhmm: str) -> bool:
    if not HHMM_PATTERN.match(hhmm):
        return False
    m = minutes_from_midnight(hhmm)
    return m % MINUTES_STEP == 0


def is_search_end_end_of_day(hhmm: str) -> bool:
    return normalize_hhmm(hhmm) == "00:00"


def parse_hhmm_to_time(hhmm: str) -> time:
    h, m = map(int, normalize_hhmm(hhmm).split(":"))
    return time(hour=h, minute=m)


def parse_pse_dtime(dtime_str: str) -> datetime:
    if not dtime_str or " " not in dtime_str:
        raise ValueError(dtime_str)
    date_part, time_part = dtime_str.split(" ", 1)
    h_str, m_str, s_str = time_part.split(":")
    h = int(h_str)
    if h >= 24:
        base = datetime.strptime(f"{date_part} 00:00:00", "%Y-%m-%d %H:%M:%S")
        return base + timedelta(days=1)
    return datetime.strptime(dtime_str, "%Y-%m-%d %H:%M:%S")


def business_date_from_day_data(data: list[dict]) -> str | None:
    if not data:
        return None
    bd = data[0].get("business_date")
    if isinstance(bd, str) and bd:
        return bd
    try:
        period_start = parse_pse_dtime(data[0]["dtime"]) - timedelta(minutes=15)
        return period_start.strftime("%Y-%m-%d")
    except (ValueError, KeyError, TypeError):
        return None


def period_bounds_for_record(record: dict) -> tuple[datetime, datetime]:
    end = parse_pse_dtime(record["dtime"])
    start = end - timedelta(minutes=15)
    return start, end


def search_window_exclusive_end(
    business_date: str,
    search_end_hhmm: str,
) -> datetime:
    day = datetime.strptime(business_date, "%Y-%m-%d").date()
    if is_search_end_end_of_day(search_end_hhmm):
        return datetime.combine(day + timedelta(days=1), time(0, 0, 0))
    t_end = parse_hhmm_to_time(search_end_hhmm)
    return datetime.combine(day, t_end)


def search_window_inclusive_start(
    business_date: str,
    search_start_hhmm: str,
) -> datetime:
    day = datetime.strptime(business_date, "%Y-%m-%d").date()
    t_start = parse_hhmm_to_time(search_start_hhmm)
    return datetime.combine(day, t_start)


def period_overlaps_search(
    period_start: datetime,
    period_end: datetime,
    search_start: datetime,
    search_end_exclusive: datetime,
) -> bool:
    return period_start < search_end_exclusive and period_end > search_start


def window_timestamp_bounds_from_records(
    records: list[dict],
) -> tuple[datetime, datetime] | None:
    if not records:
        return None
    first_end = parse_pse_dtime(records[0]["dtime"])
    last_end = parse_pse_dtime(records[-1]["dtime"])
    window_start = first_end - timedelta(minutes=15)
    window_end_exclusive = last_end
    return window_start, window_end_exclusive


def is_now_in_window(
    now: datetime,
    window_start: datetime,
    window_end_exclusive: datetime,
) -> bool:
    return window_start <= now < window_end_exclusive
