from __future__ import annotations

from datetime import timedelta
from typing import Any, TYPE_CHECKING

from homeassistant.util import dt as dt_util

from .base import RCEPriceSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowMainSensor(RCEPriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_price")
        self._attr_native_unit_of_measurement = self.native_price_unit()
        self._attr_icon = "mdi:cash"

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def scan_interval(self) -> timedelta:
        return timedelta(minutes=1)

    @property
    def native_value(self) -> float | None:
        now = dt_util.now()
        
        tomorrow_price_record = self.get_tomorrow_price_at_time(now)
        if not tomorrow_price_record:
            return None
        
        return self.round_display_price(float(tomorrow_price_record["rce_pln"]))

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return {
                "last_update": self.coordinator.data.get("last_update") if self.coordinator.data else None,
                "status": "Data not available yet",
                "data_points": 0,
                "prices": [],
            }
        excluded_keys = {"rce_pln_neg_to_zero", "publication_ts"}
        sanitized_tomorrow_data = self.round_price_records_for_attributes(
            [{k: v for k, v in record.items() if k not in excluded_keys} for record in tomorrow_data]
        )
        
        attributes = {
            "last_update": self.coordinator.data.get("last_update") if self.coordinator.data else None,
            "status": "Available",
            "data_points": len(tomorrow_data),
            "prices": sanitized_tomorrow_data,
        }
        
        return attributes