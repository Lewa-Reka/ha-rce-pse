from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEPriceSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCENextPeriodPriceSensor(RCEPriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "next_period_price")
        self._attr_native_unit_of_measurement = self.native_price_unit()
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        v = self.get_price_at_future_period(1)
        return None if v is None else self.round_display_price(v)


class RCEPreviousPeriodPriceSensor(RCEPriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "previous_period_price")
        self._attr_native_unit_of_measurement = self.native_price_unit()
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        v = self.get_price_at_past_period(1)
        return None if v is None else self.round_display_price(v)
