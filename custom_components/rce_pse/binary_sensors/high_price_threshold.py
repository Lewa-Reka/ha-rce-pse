from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as dt_util

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..const import CONF_HIGH_PRICE_THRESHOLD, DEFAULT_HIGH_PRICE_THRESHOLD
from .base import RCEBaseBinarySensor


class RCEHighPriceThresholdWindowActiveBinarySensor(RCEBaseBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, "high_price_threshold_window_active")
        self.config_entry = config_entry
        self._attr_icon = "mdi:clock-check"

    def get_config_value(self, key: str, default: Any) -> Any:
        value = None
        if self.config_entry.options and key in self.config_entry.options:
            value = self.config_entry.options[key]
        else:
            value = self.config_entry.data.get(key, default)
        if key == CONF_HIGH_PRICE_THRESHOLD:
            return float(value)
        return value

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        tomorrow_data = self.get_tomorrow_data()
        threshold = self.get_config_value(CONF_HIGH_PRICE_THRESHOLD, DEFAULT_HIGH_PRICE_THRESHOLD)
        window = self.calculator.pick_nearest_threshold_window(
            today_data, tomorrow_data, threshold, False, dt_util.now()
        )
        if not window:
            return False
        bounds = self.calculator.threshold_window_bounds_naive(window)
        if not bounds:
            return False
        start_naive, end_naive = bounds
        now = dt_util.now().replace(tzinfo=None)
        return start_naive <= now < end_naive
