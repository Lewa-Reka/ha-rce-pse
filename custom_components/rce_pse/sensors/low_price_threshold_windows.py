from __future__ import annotations

from datetime import datetime, timedelta
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


class RCETodayLowPriceThresholdWindowStartSensor(RCELowPriceThresholdWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_low_price_threshold_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        threshold = self.get_config_value(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
        window = self.calculator.find_first_window_below_threshold(today_data, threshold)
        if not window:
            return None
        try:
            start_time_str = window[0]["period"].split(" - ")[0]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            datetime_str = f"{today_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETodayLowPriceThresholdWindowEndSensor(RCELowPriceThresholdWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_low_price_threshold_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        threshold = self.get_config_value(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
        window = self.calculator.find_first_window_below_threshold(today_data, threshold)
        if not window:
            return None
        try:
            end_time_str = window[-1]["period"].split(" - ")[1]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            datetime_str = f"{today_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowLowPriceThresholdWindowStartSensor(RCELowPriceThresholdWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_low_price_threshold_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        threshold = self.get_config_value(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
        window = self.calculator.find_first_window_below_threshold(tomorrow_data, threshold)
        if not window:
            return None
        try:
            start_time_str = window[0]["period"].split(" - ")[0]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowLowPriceThresholdWindowEndSensor(RCELowPriceThresholdWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_low_price_threshold_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        threshold = self.get_config_value(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
        window = self.calculator.find_first_window_below_threshold(tomorrow_data, threshold)
        if not window:
            return None
        try:
            end_time_str = window[-1]["period"].split(" - ")[1]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None
