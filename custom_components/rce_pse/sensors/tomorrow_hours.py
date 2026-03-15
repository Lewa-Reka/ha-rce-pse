from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.util import dt as dt_util

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowHoursSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator, unique_id)
        self._attr_icon = "mdi:clock"


class RCETomorrowMaxPriceHourStartTimestampSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price_hour_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        if not max_price_records:
            return None
        
        try:
            start_time_str = max_price_records[0]["period"].split(" - ")[0]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowMaxPriceHourEndTimestampSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price_hour_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        if not max_price_records:
            return None
        
        try:
            end_time_str = max_price_records[-1]["period"].split(" - ")[1]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowMinPriceHourStartTimestampSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price_hour_start")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        if not min_price_records:
            return None
        
        try:
            start_time_str = min_price_records[0]["period"].split(" - ")[0]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {start_time_str}:00"
            start_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(start_datetime)
        except (ValueError, KeyError, IndexError):
            return None


class RCETomorrowMinPriceHourEndTimestampSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price_hour_end")
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-end"

    @property
    def native_value(self) -> datetime | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        if not min_price_records:
            return None
        
        try:
            end_time_str = min_price_records[-1]["period"].split(" - ")[1]
            tomorrow_str = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            datetime_str = f"{tomorrow_str} {end_time_str}:00"
            end_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt_util.as_local(end_datetime)
        except (ValueError, KeyError, IndexError):
            return None
