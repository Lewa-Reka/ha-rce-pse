from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from homeassistant.util import dt as dt_util

from ..const import PDGSZ_USAGE_FCST_TO_ATTR
from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator

_TRANSLATIONS_DIR = Path(__file__).resolve().parent.parent / "translations"
_STATE_DISPLAY_CACHE: dict[tuple[str, str], dict[str, str]] = {}


def _load_state_display_names(lang: str, translation_key: str) -> dict[str, str]:
    cache_key = (lang, translation_key)
    if cache_key in _STATE_DISPLAY_CACHE:
        return _STATE_DISPLAY_CACHE[cache_key]
    result: dict[str, str] = {}
    try:
        path = _TRANSLATIONS_DIR / f"{lang}.json"
        if not path.exists():
            path = _TRANSLATIONS_DIR / "en.json"
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            attrs = data.get("entity", {}).get("sensor", {}).get(translation_key, {}).get("state_attributes", {})
            for key, obj in attrs.items():
                if isinstance(obj, dict) and "name" in obj:
                    result[key] = obj["name"]
    except (OSError, ValueError, KeyError):
        pass
    _STATE_DISPLAY_CACHE[cache_key] = result
    return result

def _pdgsz_records_to_hourly_state(records: list[dict]) -> dict[int, str]:
    result: dict[int, str] = {}
    for rec in records:
        dtime_str = rec.get("dtime", "")
        if " " not in dtime_str:
            continue
        try:
            hour = int(dtime_str.split(" ", 1)[1].split(":")[0])
        except (ValueError, IndexError):
            continue
        if 0 <= hour <= 23:
            fcst = rec.get("usage_fcst", 1)
            result[hour] = PDGSZ_USAGE_FCST_TO_ATTR.get(fcst, "normal_usage")
    return result


def _hourly_states_attributes(
    hourly: dict[int, str],
    display_names: dict[str, str],
) -> list[dict[str, Any]]:
    return [
        {
            "hour": f"{h:02d}:00",
            "state": hourly.get(h),
            "state_display": display_names.get(hourly.get(h, ""), ""),
        }
        for h in range(24)
    ]


class RCEPeakHoursSensorBase(RCEBaseSensor):
    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator, unique_id)
        self._attr_icon = "mdi:flash"

    def _get_pdgsz_records(self) -> list[dict]:
        raise NotImplementedError

    def _get_current_hour_for_state(self) -> int:
        return dt_util.now().hour

    def _get_state_display(self, state_key: str | None) -> str:
        if not state_key:
            return ""
        try:
            lang = self.hass.config.language
            if lang not in ("pl", "en"):
                lang = "en"
            names = _load_state_display_names(lang, self._attr_translation_key)
            return names.get(state_key, state_key)
        except (AttributeError, KeyError):
            return state_key

    @property
    def native_value(self) -> str | None:
        records = self._get_pdgsz_records()
        hourly = _pdgsz_records_to_hourly_state(records)
        current_hour = self._get_current_hour_for_state()
        state_key = hourly.get(current_hour)
        if state_key is None:
            return None
        return self._get_state_display(state_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        records = self._get_pdgsz_records()
        hourly = _pdgsz_records_to_hourly_state(records)
        try:
            lang = self.hass.config.language
            if lang not in ("pl", "en"):
                lang = "en"
            display_names = _load_state_display_names(lang, self._attr_translation_key)
        except (AttributeError, KeyError):
            display_names = {}
        return {
            "records": records,
            "hourly_states": _hourly_states_attributes(hourly, display_names),
        }

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success or not self.coordinator.data:
            return False
        return True


class RCETodayPeakHoursSensor(RCEPeakHoursSensorBase):
    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_peak_hours")

    def _get_pdgsz_records(self) -> list[dict]:
        return self.get_today_pdgsz_data()


class RCETomorrowPeakHoursSensor(RCEPeakHoursSensorBase):
    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_peak_hours")

    def _get_pdgsz_records(self) -> list[dict]:
        return self.get_tomorrow_pdgsz_data()
