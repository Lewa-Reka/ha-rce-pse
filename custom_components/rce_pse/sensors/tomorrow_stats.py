from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT, DISPLAY_PRICE_DECIMALS
from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowStatsSensor(RCEBaseSensor):

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
        if resolved == "%":
            self._attr_suggested_display_precision = 1
        else:
            self._attr_suggested_display_precision = DISPLAY_PRICE_DECIMALS


class RCETomorrowAvgPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_avg_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return self.round_display_price(self.calculator.calculate_average(prices))


class RCETomorrowMaxPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return self.round_display_price(max(prices)) if prices else None


class RCETomorrowMinPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return self.round_display_price(min(prices)) if prices else None


class RCETomorrowMedianPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_median_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return self.round_display_price(self.calculator.calculate_median(prices))


class RCETomorrowTodayAvgComparisonSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_vs_today_avg", "%", "mdi:percent")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        today_data = self.get_today_data()
        
        if not tomorrow_data or not today_data:
            return None
        
        tomorrow_prices = self.calculator.get_prices_from_data(tomorrow_data)
        today_prices = self.calculator.get_prices_from_data(today_data)
        
        tomorrow_avg = self.calculator.calculate_average(tomorrow_prices)
        today_avg = self.calculator.calculate_average(today_prices)
        
        percentage = self.calculator.calculate_percentage_difference(tomorrow_avg, today_avg)
        return round(percentage, 1) 