from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowStatsSensor(RCEBaseSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str, unit: str = "PLN/MWh", icon: str = "mdi:cash") -> None:
        super().__init__(coordinator, unique_id)
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

    @property
    def available(self) -> bool:
        return super().available and self.is_tomorrow_data_available()


class RCETomorrowAvgPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_avg_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return round(self.calculator.calculate_average(prices), 2)


class RCETomorrowMaxPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_max_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return max(prices) if prices else None


class RCETomorrowMinPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_min_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return min(prices) if prices else None


class RCETomorrowMedianPriceSensor(RCETomorrowStatsSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "tomorrow_median_price")

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return round(self.calculator.calculate_median(prices), 2)


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