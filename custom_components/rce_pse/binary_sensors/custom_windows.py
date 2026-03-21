from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..const import (
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
)
from ..time_window import business_date_from_day_data, duration_minutes_from_hhmm, normalize_hhmm
from .base import RCEBaseBinarySensor

_TIME_WINDOW_KEYS = frozenset(
    {
        CONF_CHEAPEST_TIME_WINDOW_START,
        CONF_CHEAPEST_TIME_WINDOW_END,
        CONF_CHEAPEST_WINDOW_DURATION_HOURS,
        CONF_EXPENSIVE_TIME_WINDOW_START,
        CONF_EXPENSIVE_TIME_WINDOW_END,
        CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
        CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    }
)


class RCECustomWindowBinarySensor(RCEBaseBinarySensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
        unique_id: str,
    ) -> None:
        super().__init__(coordinator, unique_id)
        self.config_entry = config_entry

    def get_config_value(self, key: str, default: Any) -> Any:
        if self.config_entry.options and key in self.config_entry.options:
            value = self.config_entry.options[key]
        else:
            value = self.config_entry.data.get(key, default)

        if key in _TIME_WINDOW_KEYS:
            return normalize_hhmm(str(value))

        return value

    def find_optimal_window_for_data(
        self,
        day_data: list[dict],
        search_start: str,
        search_end: str,
        duration_hhmm: str,
        is_max: bool,
    ) -> list[dict]:
        bd = business_date_from_day_data(day_data)
        if not bd:
            return []
        dm = duration_minutes_from_hhmm(duration_hhmm)
        return self.calculator.find_optimal_window(
            day_data, bd, search_start, search_end, dm, is_max=is_max
        )


class RCETodayCheapestWindowBinarySensor(RCECustomWindowBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_active")
        self._attr_icon = "mdi:clock-check"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False

        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return False

        return self.is_now_within_optimal_window_records(optimal_window)


class RCETodayExpensiveWindowBinarySensor(RCECustomWindowBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_active")
        self._attr_icon = "mdi:clock-alert"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False

        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return False

        return self.is_now_within_optimal_window_records(optimal_window)


class RCETodaySecondExpensiveWindowBinarySensor(RCECustomWindowBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_second_expensive_window_active")
        self._attr_icon = "mdi:clock-alert"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False

        start_s = self.get_config_value(
            CONF_SECOND_EXPENSIVE_TIME_WINDOW_START, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START
        )
        end_s = self.get_config_value(
            CONF_SECOND_EXPENSIVE_TIME_WINDOW_END, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END
        )
        duration = self.get_config_value(
            CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS
        )

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return False

        return self.is_now_within_optimal_window_records(optimal_window)
