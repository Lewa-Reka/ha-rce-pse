from __future__ import annotations

from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorDeviceClass
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
from .base import RCEBaseSensor


class RCECustomWindowSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry, 
                 sensor_type: str) -> None:
        super().__init__(coordinator, sensor_type)
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


class RCETodayCheapestWindowStartSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_start")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            return window_start.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETodayCheapestWindowEndSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_end")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            return last_period_end.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETodayCheapestWindowRangeSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            
            return f"{window_start.strftime('%H:%M')} - {last_period_end.strftime('%H:%M')}"
        except (ValueError, KeyError):
            return None


class RCETodayExpensiveWindowStartSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_start")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            return window_start.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETodayExpensiveWindowEndSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_end")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            return last_period_end.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETodayExpensiveWindowRangeSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            
            return f"{window_start.strftime('%H:%M')} - {last_period_end.strftime('%H:%M')}"
        except (ValueError, KeyError):
            return None


class RCETomorrowCheapestWindowStartSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_start")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            return window_start.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETomorrowCheapestWindowEndSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_end")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            return last_period_end.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETomorrowCheapestWindowRangeSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
            
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            
            return f"{window_start.strftime('%H:%M')} - {last_period_end.strftime('%H:%M')}"
        except (ValueError, KeyError):
            return None


class RCETomorrowExpensiveWindowStartSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_start")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            return window_start.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETomorrowExpensiveWindowEndSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_end")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            return last_period_end.strftime("%H:%M")
        except (ValueError, KeyError):
            return None


class RCETomorrowExpensiveWindowRangeSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            first_period_end = datetime.strptime(optimal_window[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            window_start = first_period_end - timedelta(minutes=15)
            
            last_period_end = datetime.strptime(optimal_window[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            
            return f"{window_start.strftime('%H:%M')} - {last_period_end.strftime('%H:%M')}"
        except (ValueError, KeyError):
            return None


class RCETodayCheapestWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_start_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            start_time_str = optimal_window[0]["period"].split(" - ")[0]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            datetime_str = f"{today_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETodayCheapestWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_end_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            end_time_str = optimal_window[-1]["period"].split(" - ")[1]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            datetime_str = f"{today_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETodayExpensiveWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_start_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            start_time_str = optimal_window[0]["period"].split(" - ")[0]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            datetime_str = f"{today_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
            
        except (ValueError, KeyError, IndexError):
            return None


class RCETodayExpensiveWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_end_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            today_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            end_time_str = optimal_window[-1]["period"].split(" - ")[1]
            today_str = dt_util.now().strftime("%Y-%m-%d")
            datetime_str = f"{today_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowCheapestWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_start_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            start_time_str = optimal_window[0]["period"].split(" - ")[0]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
            
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowCheapestWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_end_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=False
        )
        
        if not optimal_window:
            return None
        
        try:
            end_time_str = optimal_window[-1]["period"].split(" - ")[1]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowExpensiveWindowStartTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_start_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            start_time_str = optimal_window[0]["period"].split(" - ")[0]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
            
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowExpensiveWindowEndTimestampSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_end_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        start_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_hour = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
        
        optimal_window = self.calculator.find_optimal_window(
            tomorrow_data, start_hour, end_hour, duration, is_max=True
        )
        
        if not optimal_window:
            return None
        
        try:
            end_time_str = optimal_window[-1]["period"].split(" - ")[1]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None 