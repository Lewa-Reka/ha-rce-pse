from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from ..const import DOMAIN, MANUFACTURER
from ..sensors.base import PriceCalculator

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCEBaseBinarySensor(CoordinatorEntity, BinarySensorEntity):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"rce_pse_{unique_id}"
        self._attr_has_entity_name = True
        self._attr_translation_key = f"rce_pse_{unique_id}"
        self.calculator = PriceCalculator()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "rce_pse")},
            "name": "RCE PSE",
            "model": "RCE PSE",
            "entry_type": "service",
            "manufacturer": MANUFACTURER,
        }

    def get_today_data(self) -> list[dict]:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        
        today = dt_util.now().strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == today
        ]

    def get_tomorrow_data(self) -> list[dict]:
        if not self.is_tomorrow_data_available():
            return []
            
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == tomorrow
        ]

    def is_tomorrow_data_available(self) -> bool:
        now = dt_util.now()
        return now.hour >= 14

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
            
            if start_datetime <= current_time <= end_datetime:
                return True
                
            return False
        except (ValueError, KeyError):
            return False

    @property
    def available(self) -> bool:
        return (
            self.coordinator.last_update_success 
            and self.coordinator.data is not None
            and self.coordinator.data.get("raw_data") is not None
        ) 