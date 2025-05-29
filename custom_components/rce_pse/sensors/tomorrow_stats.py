"""Tomorrow's statistics sensors for RCE PSE integration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowStatsSensor(RCEBaseSensor):
    """Base class for tomorrow's statistics sensors."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str, unit: str = "PLN/MWh", icon: str = "mdi:cash") -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id)
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.is_tomorrow_data_available()


class RCETomorrowAvgPriceSensor(RCETomorrowStatsSensor):
    """Tomorrow's average price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_avg_price")

    @property
    def native_value(self) -> float | None:
        """Return tomorrow's average price."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return round(self.calculator.calculate_average(prices), 2)


class RCETomorrowMaxPriceSensor(RCETomorrowStatsSensor):
    """Tomorrow's maximum price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_max_price")

    @property
    def native_value(self) -> float | None:
        """Return tomorrow's maximum price."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return max(prices) if prices else None


class RCETomorrowMinPriceSensor(RCETomorrowStatsSensor):
    """Tomorrow's minimum price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_min_price")

    @property
    def native_value(self) -> float | None:
        """Return tomorrow's minimum price."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return min(prices) if prices else None


class RCETomorrowMedianPriceSensor(RCETomorrowStatsSensor):
    """Tomorrow's median price sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_median_price")

    @property
    def native_value(self) -> float | None:
        """Return tomorrow's median price."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        prices = self.calculator.get_prices_from_data(tomorrow_data)
        return round(self.calculator.calculate_median(prices), 2)


class RCETomorrowTodayAvgComparisonSensor(RCETomorrowStatsSensor):
    """Tomorrow vs today average comparison sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_vs_today_avg", "%", "mdi:percent")

    @property
    def native_value(self) -> float | None:
        """Return percentage difference between tomorrow and today average price."""
        if not self.is_tomorrow_data_available():
            return None
            
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