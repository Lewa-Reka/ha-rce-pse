from __future__ import annotations

from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as dt_util

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..const import (
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
)
from .base import RCEBaseBinarySensor


class RCECustomWindowBinarySensor(RCEBaseBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry, 
                 unique_id: str) -> None:
        super().__init__(coordinator, unique_id)
        self.config_entry = config_entry

    def get_config_value(self, key: str, default: any) -> any:
        value = None
        if self.config_entry.options and key in self.config_entry.options:
            value = self.config_entry.options[key]
        else:
            value = self.config_entry.data.get(key, default)
        
        if key in [
            CONF_CHEAPEST_TIME_WINDOW_START, CONF_CHEAPEST_TIME_WINDOW_END,
            CONF_CHEAPEST_WINDOW_DURATION_HOURS, CONF_EXPENSIVE_TIME_WINDOW_START,
            CONF_EXPENSIVE_TIME_WINDOW_END, CONF_EXPENSIVE_WINDOW_DURATION_HOURS
        ]:
            return int(value)
        
        return value


class RCETodayCheapestWindowBinarySensor(RCECustomWindowBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_active")
        self._attr_icon = "mdi:clock-check"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return False
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            window_start_str = window_start.strftime("%H:%M")
            
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_end_str = last_period_end.strftime("%H:%M")
            
            return self.is_current_time_in_window(window_start_str, window_end_str)
        except (ValueError, KeyError):
            return False


class RCETodayExpensiveWindowBinarySensor(RCECustomWindowBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_active")
        self._attr_icon = "mdi:clock-alert"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return False
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            window_start_str = window_start.strftime("%H:%M")
            
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_end_str = last_period_end.strftime("%H:%M")
            
            return self.is_current_time_in_window(window_start_str, window_end_str)
        except (ValueError, KeyError):
            return False