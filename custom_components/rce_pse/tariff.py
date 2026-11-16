from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Any

from .const import (
    CONF_TARIFF_ENABLED, CONF_TARIFF_SUMMER_RATE_I, CONF_TARIFF_SUMMER_RATE_II,
    CONF_TARIFF_SUMMER_RATE_III, CONF_TARIFF_WINTER_RATE_I, CONF_TARIFF_WINTER_RATE_II,
    CONF_TARIFF_WINTER_RATE_III, CONF_TARIFF_SUMMER_I_START, CONF_TARIFF_SUMMER_I_END,
    CONF_TARIFF_SUMMER_II_START, CONF_TARIFF_SUMMER_II_END, CONF_TARIFF_WINTER_I_START,
    CONF_TARIFF_WINTER_I_END, CONF_TARIFF_WINTER_II_START, CONF_TARIFF_WINTER_II_END,
    CONF_TARIFF_SUMMER_START, CONF_TARIFF_SUMMER_END, DEFAULT_TARIFF_ENABLED,
    DEFAULT_TARIFF_RATE, DEFAULT_TARIFF_SUMMER_I_START, DEFAULT_TARIFF_SUMMER_I_END,
    DEFAULT_TARIFF_SUMMER_II_START, DEFAULT_TARIFF_SUMMER_II_END,
    DEFAULT_TARIFF_WINTER_I_START, DEFAULT_TARIFF_WINTER_I_END,
    DEFAULT_TARIFF_WINTER_II_START, DEFAULT_TARIFF_WINTER_II_END,
    DEFAULT_TARIFF_SUMMER_START, DEFAULT_TARIFF_SUMMER_END,
)

RATE_KEYS = (
    CONF_TARIFF_SUMMER_RATE_I, CONF_TARIFF_SUMMER_RATE_II, CONF_TARIFF_SUMMER_RATE_III,
    CONF_TARIFF_WINTER_RATE_I, CONF_TARIFF_WINTER_RATE_II, CONF_TARIFF_WINTER_RATE_III,
)
TIME_DEFAULTS = {
    CONF_TARIFF_SUMMER_I_START: DEFAULT_TARIFF_SUMMER_I_START,
    CONF_TARIFF_SUMMER_I_END: DEFAULT_TARIFF_SUMMER_I_END,
    CONF_TARIFF_SUMMER_II_START: DEFAULT_TARIFF_SUMMER_II_START,
    CONF_TARIFF_SUMMER_II_END: DEFAULT_TARIFF_SUMMER_II_END,
    CONF_TARIFF_WINTER_I_START: DEFAULT_TARIFF_WINTER_I_START,
    CONF_TARIFF_WINTER_I_END: DEFAULT_TARIFF_WINTER_I_END,
    CONF_TARIFF_WINTER_II_START: DEFAULT_TARIFF_WINTER_II_START,
    CONF_TARIFF_WINTER_II_END: DEFAULT_TARIFF_WINTER_II_END,
}

def _easter_sunday(year: int) -> date:
    """Return Gregorian Easter Sunday (Meeus/Jones/Butcher algorithm)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def polish_public_holidays(year: int) -> set[date]:
    easter = _easter_sunday(year)
    fixed = {
        (1, 1), (1, 6), (5, 1), (5, 3), (8, 15), (11, 1),
        (11, 11), (12, 24), (12, 25), (12, 26),
    }
    days = {date(year, month, day) for month, day in fixed}
    days.update({easter, easter + timedelta(days=1), easter + timedelta(days=49), easter + timedelta(days=60)})
    return days

def _parse_hhmm(value: Any, default: str) -> time:
    try:
        hour, minute = str(value if value is not None else default).split(":")
        h, m = int(hour), int(minute)
        if 0 <= h <= 23 and 0 <= m <= 59:
            return time(h, m)
    except (ValueError, TypeError):
        pass
    return time.fromisoformat(default)

def _parse_month_day(value: Any, default: str) -> tuple[int, int]:
    try:
        month, day = str(value if value is not None else default).split("-")
        candidate = date(2024, int(month), int(day))
        return candidate.month, candidate.day
    except (ValueError, TypeError):
        month, day = default.split("-")
        return int(month), int(day)

def _in_window(value: time, start: time, end: time) -> bool:
    if start == end:
        return False
    if start < end:
        return start <= value < end
    return value >= start or value < end

def _is_summer(day: date, start_value: Any, end_value: Any) -> bool:
    start = _parse_month_day(start_value, DEFAULT_TARIFF_SUMMER_START)
    end = _parse_month_day(end_value, DEFAULT_TARIFF_SUMMER_END)
    current = (day.month, day.day)
    if start <= end:
        return start <= current <= end
    return current >= start or current <= end

def surcharge_for_record(record: dict[str, Any], config: dict[str, Any]) -> float:
    """Return TARIFF PLN/MWh surcharge for a PSE 15-minute record."""
    if not config.get(CONF_TARIFF_ENABLED, DEFAULT_TARIFF_ENABLED):
        return 0.0
    raw_start = record.get("start_dtime")
    if isinstance(raw_start, datetime):
        period_start = raw_start
    else:
        raw_end = record.get("dtime")
        if not isinstance(raw_end, str):
            return 0.0
        try:
            # PSE dtime is a naive wall-clock timestamp. Use it directly:
            # tariff assignment must not convert it to Home Assistant local time.
            period_start = datetime.fromisoformat(raw_end) - timedelta(minutes=15)
        except ValueError:
            return 0.0
    day = period_start.date()
    if day.weekday() >= 5 or day in polish_public_holidays(day.year):
        zone = "III"
        season = "summer" if _is_summer(day, config.get(CONF_TARIFF_SUMMER_START), config.get(CONF_TARIFF_SUMMER_END)) else "winter"
    else:
        season = "summer" if _is_summer(day, config.get(CONF_TARIFF_SUMMER_START), config.get(CONF_TARIFF_SUMMER_END)) else "winter"
        clock = period_start.time()
        prefix = "tariff_summer" if season == "summer" else "tariff_winter"
        i_start_key = f"{prefix}_i_start"
        i_end_key = f"{prefix}_i_end"
        ii_start_key = f"{prefix}_ii_start"
        ii_end_key = f"{prefix}_ii_end"
        i_start = _parse_hhmm(config.get(i_start_key), TIME_DEFAULTS[i_start_key])
        i_end = _parse_hhmm(config.get(i_end_key), TIME_DEFAULTS[i_end_key])
        ii_start = _parse_hhmm(config.get(ii_start_key), TIME_DEFAULTS[ii_start_key])
        ii_end = _parse_hhmm(config.get(ii_end_key), TIME_DEFAULTS[ii_end_key])
        if _in_window(clock, i_start, i_end):
            zone = "I"
        elif _in_window(clock, ii_start, ii_end):
            zone = "II"
        else:
            zone = "III"
    rate_key = f"tariff_{season}_rate_{zone.lower()}"
    try:
        return float(config.get(rate_key, DEFAULT_TARIFF_RATE) or 0.0)
    except (TypeError, ValueError):
        return 0.0

def apply_tariff_surcharge(records: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    if not records or not config.get(CONF_TARIFF_ENABLED, DEFAULT_TARIFF_ENABLED):
        return records
    result: list[dict[str, Any]] = []
    for record in records:
        new_record = record.copy()
        try:
            raw_price = float(new_record["rce_pln"])
            surcharge = surcharge_for_record(new_record, config)
            # Preserve the established neg-to-zero meaning: clamp the RCE component
            # first, then add the same TARIFF surcharge to the resulting channel.
            new_record["rce_pln_neg_to_zero"] = f"{max(0.0, raw_price) + surcharge:.6f}"
            new_record["rce_pln"] = f"{raw_price + surcharge:.6f}"
        except (KeyError, TypeError, ValueError):
            pass
        result.append(new_record)
    return result
