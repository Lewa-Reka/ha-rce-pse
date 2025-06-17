from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.util import dt as dt_util

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayHoursSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator, unique_id)
        self._attr_icon = "mdi:clock"


class RCETodayMaxPriceHourStartSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price_hour_start")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        return max_price_records[0]["period"].split(" - ")[0] if max_price_records else None


class RCETodayMaxPriceHourEndSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price_hour_end")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        return max_price_records[-1]["period"].split(" - ")[1] if max_price_records else None


class RCETodayMinPriceHourStartSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price_hour_start")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        return min_price_records[0]["period"].split(" - ")[0] if min_price_records else None


class RCETodayMinPriceHourEndSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price_hour_end")

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        return min_price_records[-1]["period"].split(" - ")[1] if min_price_records else None


class RCETodayMaxPriceHourStartTimestampSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price_hour_start_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        if not max_price_records:
            return None
        
        try:
            first_period_end = datetime.strptime(max_price_records[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            period_start = first_period_end - timedelta(minutes=15)
            return dt_util.as_local(period_start)
        except (ValueError, KeyError):
            return None


class RCETodayMaxPriceHourEndTimestampSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price_hour_end_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        if not max_price_records:
            return None
        
        try:
            last_period_end = datetime.strptime(max_price_records[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(last_period_end)
        except (ValueError, KeyError):
            return None


class RCETodayMinPriceHourStartTimestampSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price_hour_start_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        if not min_price_records:
            return None
        
        try:
            first_period_end = datetime.strptime(min_price_records[0]["dtime"], "%Y-%m-%d %H:%M:%S")
            period_start = first_period_end - timedelta(minutes=15)
            return dt_util.as_local(period_start)
        except (ValueError, KeyError):
            return None


class RCETodayMinPriceHourEndTimestampSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price_hour_end_timestamp")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        if not min_price_records:
            return None
        
        try:
            last_period_end = datetime.strptime(min_price_records[-1]["dtime"], "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(last_period_end)
        except (ValueError, KeyError):
            return None


class RCETodayMinPriceRangeSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        if not min_price_records:
            return None
            
        start_time = min_price_records[0]["period"].split(" - ")[0]
        end_time = min_price_records[-1]["period"].split(" - ")[1]
        return f"{start_time} - {end_time}"


class RCETodayMaxPriceRangeSensor(RCETodayHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        if not max_price_records:
            return None
            
        start_time = max_price_records[0]["period"].split(" - ")[0]
        end_time = max_price_records[-1]["period"].split(" - ")[1]
        return f"{start_time} - {end_time}" 