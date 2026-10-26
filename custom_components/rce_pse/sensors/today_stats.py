from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorStateClass

from ..const import CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT
from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayStatsSensor(RCEBaseSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        unique_id: str,
        unit: str | None = None,
        icon: str = "mdi:cash",
    ) -> None:
        super().__init__(coordinator, unique_id)
        resolved = unit if unit is not None else coordinator._get_config_value(
            CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT
        )
        self._attr_native_unit_of_measurement = resolved
        self._attr_icon = icon
        self._attr_state_class = SensorStateClass.MEASUREMENT
        if resolved == "%":
            self._attr_suggested_display_precision = 1
        else:
            self._attr_suggested_display_precision = self.display_price_decimals_for_entity()


class RCETodayAvgPriceSensor(RCETodayStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_avg_price")

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return self.round_display_price(self.calculator.calculate_average(prices))


class RCETodayMaxPriceSensor(RCETodayStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_max_price")

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return self.round_display_price(max(prices)) if prices else None


class RCETodayMinPriceSensor(RCETodayStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_min_price")

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return self.round_display_price(min(prices)) if prices else None


class RCETodayMedianPriceSensor(RCETodayStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_median_price")

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return self.round_display_price(self.calculator.calculate_median(prices))


class RCETodayCurrentVsAverageSensor(RCETodayStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_current_vs_average", "%", "mdi:percent")

    @property
    def native_value(self) -> float | None:
        current_data = self.get_current_price_data()
        today_data = self.get_today_data()
        
        if not current_data or not today_data:
            return None
        
        current_price = float(current_data["rce_pln"])
        prices = self.calculator.get_prices_from_data(today_data)
        avg_price = self.calculator.calculate_average(prices)
        
        percentage = self.calculator.calculate_percentage_difference(current_price, avg_price)
        return round(percentage, 1) 