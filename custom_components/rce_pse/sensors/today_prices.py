from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCEFuturePriceSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str, hours_ahead: int) -> None:
        super().__init__(coordinator, unique_id)
        self._hours_ahead = hours_ahead
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        return self.get_price_at_future_hour(self._hours_ahead)


class RCENextHourPriceSensor(RCEFuturePriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "next_hour_price", 1)


class RCENext2HoursPriceSensor(RCEFuturePriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "next_2_hours_price", 2)


class RCENext3HoursPriceSensor(RCEFuturePriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "next_3_hours_price", 3)


class RCEPreviousHourPriceSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "previous_hour_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        return self.get_price_at_past_hour(1) 