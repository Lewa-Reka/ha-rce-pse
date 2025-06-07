from __future__ import annotations

from datetime import timedelta
from typing import Any, TYPE_CHECKING

from homeassistant.util import dt as dt_util

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowMainSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def available(self) -> bool:
        return super().available and self.is_tomorrow_data_available()

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def scan_interval(self) -> timedelta:
        return timedelta(minutes=1)

    @property
    def native_value(self) -> float | None:
        if not self.is_tomorrow_data_available():
            return None
            
        current_hour = dt_util.now().hour
        
        tomorrow_price_record = self.get_tomorrow_price_at_hour(current_hour)
        if not tomorrow_price_record:
            return None
        
        return round(float(tomorrow_price_record["rce_pln"]), 2)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if not self.is_tomorrow_data_available():
            return {
                "available_after": "14:00 CET",
                "status": "Data not available yet",
                "data_points": 0,
                "prices": [],
                "current_hour": dt_util.now().hour,
            }
            
        current_hour = dt_util.now().hour
        tomorrow_data = self.get_tomorrow_data()
        tomorrow_price_record = self.get_tomorrow_price_at_hour(current_hour)
        
        attributes = {
            "last_update": self.coordinator.data.get("last_update") if self.coordinator.data else None,
            "data_points": len(tomorrow_data),
            "prices": tomorrow_data,
            "available_after": "14:00 CET",
            "status": "Available",
            "current_hour": current_hour,
            "tomorrow_price_for_hour": tomorrow_price_record,
        }
        
        return attributes 