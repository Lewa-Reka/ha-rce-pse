from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.util import dt as dt_util

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..time_window import (
    business_date_from_day_data,
    duration_minutes_from_hhmm,
    normalize_hhmm,
    parse_pse_dtime,
)
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
from .base import RCEBaseSensor

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


class RCECustomWindowSensor(RCEBaseSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
    ) -> None:
        super().__init__(coordinator, sensor_type)
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

    def window_start_as_local(self, optimal_window: list[dict]) -> datetime | None:
        if not optimal_window:
            return None
        try:
            pe = parse_pse_dtime(optimal_window[0]["dtime"])
            return dt_util.as_local(pe - timedelta(minutes=15))
        except (ValueError, KeyError, IndexError):
            return None

    def window_end_as_local(self, optimal_window: list[dict]) -> datetime | None:
        if not optimal_window:
            return None
        try:
            pe = parse_pse_dtime(optimal_window[-1]["dtime"])
            return dt_util.as_local(pe)
        except (ValueError, KeyError, IndexError):
            return None


class RCETodayCheapestWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return None

        return self.window_start_as_local(optimal_window)


class RCETodayCheapestWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return None

        return self.window_end_as_local(optimal_window)


class RCETodayExpensiveWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        return self.window_start_as_local(optimal_window)


class RCETodayExpensiveWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        return self.window_end_as_local(optimal_window)


class RCETomorrowCheapestWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return None

        return self.window_start_as_local(optimal_window)


class RCETomorrowCheapestWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return None

        return self.window_end_as_local(optimal_window)


class RCETomorrowExpensiveWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        return self.window_start_as_local(optimal_window)


class RCETomorrowExpensiveWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        return self.window_end_as_local(optimal_window)


class RCETodaySecondExpensiveWindowStartSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_second_expensive_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

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
            return None

        return self.window_start_as_local(optimal_window)


class RCETodaySecondExpensiveWindowEndSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_second_expensive_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
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
            return None

        return self.window_end_as_local(optimal_window)


class RCETomorrowSecondExpensiveWindowStartSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_second_expensive_window_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

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
            tomorrow_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        return self.window_start_as_local(optimal_window)


class RCETomorrowSecondExpensiveWindowEndSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_second_expensive_window_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
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
            tomorrow_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        return self.window_end_as_local(optimal_window)