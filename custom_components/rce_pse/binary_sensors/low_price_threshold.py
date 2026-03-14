from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as dt_util

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..const import CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD
from .base import RCEBaseBinarySensor


class RCETodayLowPriceThresholdWindowActiveBinarySensor(RCEBaseBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, "today_low_price_threshold_window_active")
        self.config_entry = config_entry
        self._attr_icon = "mdi:clock-check"

    def get_config_value(self, key: str, default: Any) -> Any:
        value = None
        if self.config_entry.options and key in self.config_entry.options:
            value = self.config_entry.options[key]
        else:
            value = self.config_entry.data.get(key, default)
        if key == CONF_LOW_PRICE_THRESHOLD:
            return float(value)
        return value

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False
        threshold = self.get_config_value(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
        window = self.calculator.find_first_window_below_threshold(today_data, threshold)
        if not window:
            return False
        try:
            start_time_str = window[0]["period"].split(" - ")[0]
            end_time_str = window[-1]["period"].split(" - ")[1]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            start_datetime = datetime.strptime(f"{today_str} {start_time_str}:00", "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(f"{today_str} {end_time_str}:00", "%Y-%m-%d %H:%M:%S")
            now = dt_util.now().replace(tzinfo=None)
            return start_datetime <= now < end_datetime
        except (ValueError, KeyError, IndexError):
            return False
