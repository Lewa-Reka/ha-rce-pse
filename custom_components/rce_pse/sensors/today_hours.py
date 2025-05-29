"""Today's min/max price hours sensors for RCE PSE integration."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .base import RCEBaseSensor

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayHoursSensor(RCEBaseSensor):
    """Base class for today's hours sensors."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, unique_id)
        self._attr_icon = "mdi:clock"


class RCETodayMaxPriceHourStartSensor(RCETodayHoursSensor):
    """Today's max price hour start sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_max_price_hour_start")

    @property
    def native_value(self) -> str | None:
        """Return hour when max price starts."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        return max_price_records[0]["period"].split(" - ")[0] if max_price_records else None


class RCETodayMaxPriceHourEndSensor(RCETodayHoursSensor):
    """Today's max price hour end sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_max_price_hour_end")

    @property
    def native_value(self) -> str | None:
        """Return hour when max price ends."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        max_price_records = self.calculator.find_extreme_price_records(today_data, is_max=True)
        return max_price_records[-1]["period"].split(" - ")[1] if max_price_records else None


class RCETodayMinPriceHourStartSensor(RCETodayHoursSensor):
    """Today's min price hour start sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_min_price_hour_start")

    @property
    def native_value(self) -> str | None:
        """Return hour when min price starts."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        return min_price_records[0]["period"].split(" - ")[0] if min_price_records else None


class RCETodayMinPriceHourEndSensor(RCETodayHoursSensor):
    """Today's min price hour end sensor."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "today_min_price_hour_end")

    @property
    def native_value(self) -> str | None:
        """Return hour when min price ends."""
        today_data = self.get_today_data()
        if not today_data:
            return None
        
        min_price_records = self.calculator.find_extreme_price_records(today_data, is_max=False)
        return min_price_records[-1]["period"].split(" - ")[1] if min_price_records else None 