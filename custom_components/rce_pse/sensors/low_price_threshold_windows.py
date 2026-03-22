from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.util import dt as dt_util

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..const import CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD
from .base import RCEBaseSensor


class RCELowPriceThresholdWindowSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry, sensor_type: str) -> None:
        super().__init__(coordinator, sensor_type)
        self.config_entry = config_entry

    def get_config_value(self, key: str, default: Any) -> Any:
        value = None
        if self.config_entry.options and key in self.config_entry.options:
            value = self.config_entry.options[key]
        else:
            value = self.config_entry.data.get(key, default)
        if key == CONF_LOW_PRICE_THRESHOLD:
            return float(value)
        return value

    def nearest_window(self) -> list[dict] | None:
        today_data = self.get_today_data()
        tomorrow_data = self.get_tomorrow_data()
        threshold = self.get_config_value(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
        return self.calculator.pick_nearest_threshold_window(
            today_data, tomorrow_data, threshold, True, dt_util.now()
        )


class RCELowPriceThresholdWindowStartSensor(RCELowPriceThresholdWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "low_price_threshold_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        window = self.nearest_window()
        if not window:
            return None
        bounds = self.calculator.threshold_window_bounds_naive(window)
        if not bounds:
            return None
        start_naive, _ = bounds
        return dt_util.as_local(start_naive)


class RCELowPriceThresholdWindowEndSensor(RCELowPriceThresholdWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "low_price_threshold_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        window = self.nearest_window()
        if not window:
            return None
        bounds = self.calculator.threshold_window_bounds_naive(window)
        if not bounds:
            return None
        _, end_naive = bounds
        return dt_util.as_local(end_naive)
