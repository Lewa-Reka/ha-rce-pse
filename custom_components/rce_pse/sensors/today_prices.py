from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCENextPeriodPriceSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "next_period_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        return self.get_price_at_future_period(1)


class RCEPreviousPeriodPriceSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "previous_period_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        return self.get_price_at_past_period(1)
