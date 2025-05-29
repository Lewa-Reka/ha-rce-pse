"""Today's statistics sensors for RCE PSE integration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayStatsSensor(RCEBaseSensor):
    """Base class for today's statistics sensors."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str, unit: str = "PLN/MWh", icon: str = "mdi:cash") -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id)
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon


class RCETodayAvgPriceSensor(RCETodayStatsSensor):
    """Today's average price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_avg_price")

    @property
    def native_value(self) -> float | None:
        """Return today's average price."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return round(self.calculator.calculate_average(prices), 2)


class RCETodayMaxPriceSensor(RCETodayStatsSensor):
    """Today's maximum price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_max_price")

    @property
    def native_value(self) -> float | None:
        """Return today's maximum price."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return max(prices) if prices else None


class RCETodayMinPriceSensor(RCETodayStatsSensor):
    """Today's minimum price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_min_price")

    @property
    def native_value(self) -> float | None:
        """Return today's minimum price."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return min(prices) if prices else None


class RCETodayMedianPriceSensor(RCETodayStatsSensor):
    """Today's median price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_median_price")

    @property
    def native_value(self) -> float | None:
        """Return today's median price."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        prices = self.calculator.get_prices_from_data(today_data)
        return round(self.calculator.calculate_median(prices), 2)


class RCETodayCurrentVsAverageSensor(RCETodayStatsSensor):
    """Today's current vs average sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_current_vs_average", "%", "mdi:percent")

    @property
    def native_value(self) -> float | None:
        """Return percentage difference between current and average price."""
        current_data = self.get_current_price_data()
        today_data = self.get_today_data()
        
        if not current_data or not today_data:
            return None
        
        current_price = float(current_data["rce_pln"])
        prices = self.calculator.get_prices_from_data(today_data)
        avg_price = self.calculator.calculate_average(prices)
        
        percentage = self.calculator.calculate_percentage_difference(current_price, avg_price)
        return round(percentage, 1) 