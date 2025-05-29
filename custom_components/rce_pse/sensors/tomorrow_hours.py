"""Tomorrow's min/max price hours sensors for RCE PSE integration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETomorrowHoursSensor(RCEBaseSensor):
    """Base class for tomorrow's hours sensors."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id)
        self._attr_icon = "mdi:clock"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.is_tomorrow_data_available()


class RCETomorrowMaxPriceHourStartSensor(RCETomorrowHoursSensor):
    """Tomorrow's max price hour start sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_max_price_hour_start")

    @property
    def native_value(self) -> str | None:
        """Return hour when max price starts."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        return max_price_records[0]["period"].split(" - ")[0] if max_price_records else None


class RCETomorrowMaxPriceHourEndSensor(RCETomorrowHoursSensor):
    """Tomorrow's max price hour end sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_max_price_hour_end")

    @property
    def native_value(self) -> str | None:
        """Return hour when max price ends."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=True)
        return max_price_records[-1]["period"].split(" - ")[1] if max_price_records else None


class RCETomorrowMinPriceHourStartSensor(RCETomorrowHoursSensor):
    """Tomorrow's min price hour start sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_min_price_hour_start")

    @property
    def native_value(self) -> str | None:
        """Return hour when min price starts."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        return min_price_records[0]["period"].split(" - ")[0] if min_price_records else None


class RCETomorrowMinPriceHourEndSensor(RCETomorrowHoursSensor):
    """Tomorrow's min price hour end sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "tomorrow_min_price_hour_end")

    @property
    def native_value(self) -> str | None:
        """Return hour when min price ends."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(tomorrow_data, is_max=False)
        return min_price_records[-1]["period"].split(" - ")[1] if min_price_records else None 