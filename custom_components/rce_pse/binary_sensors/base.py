from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from ..const import DOMAIN, MANUFACTURER
from ..price_calculator import PriceCalculator
from ..shared_base import RCEBaseCommonEntity

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCEBaseBinarySensor(RCEBaseCommonEntity, BinarySensorEntity):
    def __init__(self, coordinator, unique_id):
        super().__init__(coordinator, unique_id)

    def is_current_time_in_window(self, start_time_str: str, end_time_str: str, target_date: str = None) -> bool:
        if not start_time_str or not end_time_str:
            return False
        try:
            if target_date is None:
                target_date = dt_util.now().strftime("%Y-%m-%d")
            start_datetime_str = f"{target_date} {start_time_str}:00"
            end_datetime_str = f"{target_date} {end_time_str}:00"
            start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S")
            current_time = dt_util.now().replace(tzinfo=None)
            return start_datetime <= current_time <= end_datetime
        except (ValueError, KeyError):
            return False 