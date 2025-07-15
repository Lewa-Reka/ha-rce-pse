from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.util import dt as dt_util
from .base import RCEBaseBinarySensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayMinPriceWindowBinarySensor(RCEBaseBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price_window_active")
        self._attr_icon = "mdi:clock-check"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        if not min_price_records:
            return False
        
        start_time = min_price_records[0]["period"].split(" - ")[0]
        end_time = min_price_records[-1]["period"].split(" - ")[1]
        
        return self.is_current_time_in_window(start_time, end_time)


class RCETodayMaxPriceWindowBinarySensor(RCEBaseBinarySensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price_window_active")
        self._attr_icon = "mdi:clock-alert"

    @property
    def is_on(self) -> bool:
        today_data = self.get_today_data()
        if not today_data:
            return False
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        if not max_price_records:
            return False
        
        start_time = max_price_records[0]["period"].split(" - ")[0]
        end_time = max_price_records[-1]["period"].split(" - ")[1]
        
        return self.is_current_time_in_window(start_time, end_time)