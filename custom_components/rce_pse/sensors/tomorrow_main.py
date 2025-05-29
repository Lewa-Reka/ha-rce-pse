"""Main tomorrow RCE PSE sensor."""
from __future__ import annotations

from datetime import timedelta
from typing import Any, TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowMainSensor(RCEBaseSensor):
    """Representation of tomorrow's RCE PSE sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.is_tomorrow_data_available()

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
        """Return tomorrow's average price as main value."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return round(self.calculator.calculate_average(prices), 2)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return tomorrow's data as attributes."""
        if not self.is_tomorrow_data_available():
            return {
                "available_after": "14:00 CET",
                "status": "Data not available yet",
                "data_points": 0,
                "prices": [],
            }
            
        tomorrow_data = self.get_tomorrow_data()
        
        attributes = {
            "last_update": self.coordinator.data.get("last_update") if self.coordinator.data else None,
            "data_points": len(tomorrow_data),
            "prices": tomorrow_data,
            "available_after": "14:00 CET",
            "status": "Available",
        }
        
        return attributes 