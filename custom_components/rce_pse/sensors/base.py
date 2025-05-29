"""Base sensor class for RCE PSE integration."""
from __future__ import annotations

import statistics
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from ..const import DOMAIN, MANUFACTURER

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class PriceCalculator:
    """Helper class for price calculations."""
    
    @staticmethod
    def get_prices_from_data(data: list[dict]) -> list[float]:
        """Extract prices from data records."""
        return [float(record["rce_pln"]) for record in data]
    
    @staticmethod
    def calculate_average(prices: list[float]) -> float:
        """Calculate average price."""
        return sum(prices) / len(prices) if prices else 0.0
    
    @staticmethod
    def calculate_median(prices: list[float]) -> float:
        """Calculate median price."""
        return statistics.median(prices) if prices else 0.0
    
    @staticmethod
    def get_hourly_prices(data: list[dict]) -> dict[str, float]:
        """Get hourly prices dictionary."""
        hourly_prices = {}
        for record in data:
            try:
                period = record["period"]
                # Check if period follows the expected format "HH:MM - HH:MM"
                if " - " not in period:
                    continue
                hour_part = period.split(" - ")[0]
                # Validate that hour part is in format "HH:MM"
                if ":" not in hour_part or len(hour_part) < 5:
                    continue
                hour = hour_part[:2]
                # Validate that hour is numeric
                if not hour.isdigit():
                    continue
                if hour not in hourly_prices:
                    hourly_prices[hour] = float(record["rce_pln"])
            except (ValueError, KeyError, IndexError):
                continue
        return hourly_prices
    
    @staticmethod
    def calculate_percentage_difference(current: float, reference: float) -> float:
        """Calculate percentage difference between current and reference value."""
        if reference == 0:
            return 0.0
        return ((current - reference) / reference) * 100
    
    @staticmethod
    def find_extreme_price_records(data: list[dict], is_max: bool = True) -> list[dict]:
        """Find records with extreme (min or max) prices."""
        if not data:
            return []
        
        prices = PriceCalculator.get_prices_from_data(data)
        extreme_price = max(prices) if is_max else min(prices)
        
        extreme_records = [
            record for record in data 
            if float(record["rce_pln"]) == extreme_price
        ]
        
        return sorted(extreme_records, key=lambda x: x["dtime"])


class RCEBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for RCE PSE sensors."""

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"rce_pse_{unique_id}"
        self._attr_has_entity_name = True
        self._attr_translation_key = f"rce_pse_{unique_id}"
        self.calculator = PriceCalculator()

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, "rce_pse")},
            "name": "RCE PSE",
            "model": "RCE PSE",
            "entry_type": "service",
            "manufacturer": MANUFACTURER,
        }

    def get_today_data(self) -> list[dict]:
        """Get today's data from coordinator."""
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        
        today = dt_util.now().strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == today
        ]

    def get_tomorrow_data(self) -> list[dict]:
        """Get tomorrow's data from coordinator."""
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == tomorrow
        ]

    def is_tomorrow_data_available(self) -> bool:
        """Check if tomorrow's data is available (after 14:00)."""
        now = dt_util.now()
        return now.hour >= 14

    def get_tomorrow_price_at_hour(self, hour: int) -> dict | None:
        """Get tomorrow's price data for specific hour."""
        if not self.is_tomorrow_data_available():
            return None
            
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        for record in tomorrow_data:
            try:
                period_start = record["period"].split(" - ")[0]
                record_hour = int(period_start[:2])
                if record_hour == hour:
                    return record
            except (ValueError, KeyError, IndexError):
                continue
        
        return None

    def get_current_price_data(self) -> dict | None:
        """Get current price data based on time."""
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None
        
        now = dt_util.now()
        
        for record in self.coordinator.data["raw_data"]:
            try:
                record_time = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                if now.replace(tzinfo=None) < record_time:
                    return record
            except (ValueError, KeyError):
                continue
        
        return None

    def get_price_at_future_hour(self, hours_ahead: int) -> float | None:
        """Get price at specific number of hours ahead."""
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None
        
        target_time = dt_util.now() + timedelta(hours=hours_ahead)
        
        for record in self.coordinator.data["raw_data"]:
            try:
                record_time = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                if target_time.replace(tzinfo=None) <= record_time:
                    return float(record["rce_pln"])
            except (ValueError, KeyError):
                continue
        
        return None

    def get_data_summary(self, data: list[dict]) -> dict[str, any]:
        """Get summary statistics for data."""
        if not data:
            return {}
        
        prices = self.calculator.get_prices_from_data(data)
        return {
            "count": len(prices),
            "average": round(self.calculator.calculate_average(prices), 2),
            "median": round(self.calculator.calculate_median(prices), 2),
            "min": min(prices),
            "max": max(prices),
            "range": max(prices) - min(prices),
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success 
            and self.coordinator.data is not None
            and self.coordinator.data.get("raw_data") is not None
        ) 