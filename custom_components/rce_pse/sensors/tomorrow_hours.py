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

    @property
    def available(self) -> bool:
        return super().available and self.is_tomorrow_data_available()


class RCETomorrowMaxPriceHourStartSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price_hour_start")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        return max_price_records[0]["period"].split(" - ")[0] if max_price_records else None


class RCETomorrowMaxPriceHourEndSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price_hour_end")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        return max_price_records[-1]["period"].split(" - ")[1] if max_price_records else None


class RCETomorrowMinPriceHourStartSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price_hour_start")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        return min_price_records[0]["period"].split(" - ")[0] if min_price_records else None


class RCETomorrowMinPriceHourEndSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price_hour_end")

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        return min_price_records[-1]["period"].split(" - ")[1] if min_price_records else None


class RCETomorrowMaxPriceHourStartTimestampSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price_hour_start_timestamp")
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
        super().__init__(coordinator, "tomorrow_max_price_hour_end_timestamp")
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
        super().__init__(coordinator, "tomorrow_min_price_hour_start_timestamp")
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
        super().__init__(coordinator, "tomorrow_min_price_hour_end_timestamp")
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


class RCETomorrowMinPriceRangeSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        if not min_price_records:
            return None
            
        start_time = min_price_records[0]["period"].split(" - ")[0]
        end_time = min_price_records[-1]["period"].split(" - ")[1]
        return f"{start_time} - {end_time}"


class RCETomorrowMaxPriceRangeSensor(RCETomorrowHoursSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price_range")
        self._attr_icon = "mdi:clock-time-four"

    @property
    def native_value(self) -> str | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        if not max_price_records:
            return None
            
        start_time = max_price_records[0]["period"].split(" - ")[0]
        end_time = max_price_records[-1]["period"].split(" - ")[1]
        return f"{start_time} - {end_time}" 