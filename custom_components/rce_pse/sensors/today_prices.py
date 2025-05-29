"""Today's price sensors for RCE PSE integration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCEFuturePriceSensor(RCEBaseSensor):
    """Base class for future price sensors."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str, hours_ahead: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id)
        self._hours_ahead = hours_ahead
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        """Return price for specified hours ahead."""
        return self.get_price_at_future_hour(self._hours_ahead)


class RCENextHourPriceSensor(RCEFuturePriceSensor):
    """Next hour RCE price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "next_hour_price", 1)


class RCENext2HoursPriceSensor(RCEFuturePriceSensor):
    """Price in 2 hours sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "next_2_hours_price", 2)


class RCENext3HoursPriceSensor(RCEFuturePriceSensor):
    """Price in 3 hours sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "next_3_hours_price", 3) 