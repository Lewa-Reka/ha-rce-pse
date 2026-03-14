from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..const import PDGSZ_USAGE_FCST_TO_ATTR
from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


def _pdgsz_records_to_ranges(records: list[dict]) -> dict[str, list[str]]:
    attr_keys = set(PDGSZ_USAGE_FCST_TO_ATTR.values())
    result: dict[str, list[str]] = {k: [] for k in attr_keys}
    if not records:
        return result
    records_sorted = sorted(records, key=lambda r: r.get("dtime", ""))
    i = 0
    while i < len(records_sorted):
        rec = records_sorted[i]
        fcst = rec.get("usage_fcst", 1)
        attr_key = PDGSZ_USAGE_FCST_TO_ATTR.get(fcst, "normal_usage")
        dtime_str = rec.get("dtime", "")
        if " " not in dtime_str:
            i += 1
            continue
        start_part = dtime_str.split(" ", 1)[1]
        try:
            start_hour = int(start_part.split(":")[0])
        except (ValueError, IndexError):
            i += 1
            continue
        j = i + 1
        while j < len(records_sorted) and records_sorted[j].get("usage_fcst") == fcst:
            j += 1
        end_hour = start_hour + (j - i)
        if end_hour > 24:
            end_hour = 24
        end_part = f"{end_hour:02d}:00" if end_hour < 24 else "24:00"
        result[attr_key].append(f"{start_part}–{end_part}")
        i = j
    return result


class RCEPeakHoursSensorBase(RCEBaseSensor):
    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator, unique_id)
        self._attr_icon = "mdi:flash"

    def _get_pdgsz_records(self) -> list[dict]:
        raise NotImplementedError

    @property
    def native_value(self) -> int | None:
        records = self._get_pdgsz_records()
        if not records:
            return None
        ranges = _pdgsz_records_to_ranges(records)
        return sum(len(v) for v in ranges.values())

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        records = self._get_pdgsz_records()
        return _pdgsz_records_to_ranges(records)

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success or not self.coordinator.data:
            return False
        if "pdgsz_data" not in self.coordinator.data:
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

    @property
    def available(self) -> bool:
        if not self.is_tomorrow_data_available():
            return False
        return super().available
