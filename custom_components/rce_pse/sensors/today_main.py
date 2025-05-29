"""Main today RCE PSE sensor."""
from __future__ import annotations

from datetime import timedelta
from typing import Any, TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayMainSensor(RCEBaseSensor):
    """Representation of a RCE PSE main sensor for today."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state."""
        return True

    @property
    def scan_interval(self) -> timedelta:
        """Return the scan interval."""
        return timedelta(minutes=1)

    @property
    def native_value(self) -> float | None:
        """Return current price based on time comparison."""
        current_data = self.get_current_price_data()
        if current_data:
            return float(current_data["rce_pln"])
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return today's data as attributes."""
        today_data = self.get_today_data()
        
        attributes = {
            "last_update": self.coordinator.data.get("last_update") if self.coordinator.data else None,
            "data_points": len(today_data),
            "prices": today_data,
        }
        
        return attributes 