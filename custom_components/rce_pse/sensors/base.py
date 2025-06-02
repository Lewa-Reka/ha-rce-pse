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
    
    @staticmethod
    def get_prices_from_data(data: list[dict]) -> list[float]:
        return [float(record["rce_pln"]) for record in data]
    
    @staticmethod
    def calculate_average(prices: list[float]) -> float:
        return sum(prices) / len(prices) if prices else 0.0
    
    @staticmethod
    def calculate_median(prices: list[float]) -> float:
        return statistics.median(prices) if prices else 0.0
    
    @staticmethod
    def get_hourly_prices(data: list[dict]) -> dict[str, float]:
        hourly_prices = {}
        for record in data:
            try:
                period = record["period"]
                if " - " not in period:
                    continue
                hour_part = period.split(" - ")[0]

                if ":" not in hour_part or len(hour_part) < 5:
                    continue
                hour = hour_part[:2]

                if not hour.isdigit():
                    continue
                if hour not in hourly_prices:
                    hourly_prices[hour] = float(record["rce_pln"])
            except (ValueError, KeyError, IndexError):
                continue
        return hourly_prices
    
    @staticmethod
    def calculate_percentage_difference(current: float, reference: float) -> float:
        if reference == 0:
            return 0.0
        return ((current - reference) / reference) * 100
    
    @staticmethod
    def find_extreme_price_records(data: list[dict], is_max: bool = True) -> list[dict]:
        if not data:
            return []
        
        prices = PriceCalculator.get_prices_from_data(data)
        extreme_price = max(prices) if is_max else min(prices)
        
        extreme_records = [
            record for record in data 
            if float(record["rce_pln"]) == extreme_price
        ]
        
        return sorted(extreme_records, key=lambda x: x["dtime"])

    @staticmethod
    def find_optimal_window(data: list[dict], window_start_hour: int, window_end_hour: int, 
                          duration_hours: int, is_max: bool = False) -> list[dict]:
        if not data or duration_hours <= 0:
            return []
        
        duration_periods = int(duration_hours) * 4
        
        filtered_data = []
        for record in data:
            try:
                end_time = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                
                start_time = end_time - timedelta(minutes=15)
                
                if start_time.hour >= window_start_hour and start_time.hour < window_end_hour:
                    filtered_data.append(record)
                    
            except (ValueError, KeyError):
                continue
        
        if len(filtered_data) < duration_periods:
            return []
        
        filtered_data.sort(key=lambda x: x["dtime"])
        
        best_window = []
        best_avg_price = None
        
        for i in range(len(filtered_data) - duration_periods + 1):
            window = filtered_data[i:i + duration_periods]
            
            is_continuous = True
            for j in range(len(window) - 1):
                try:
                    curr_time = datetime.strptime(window[j]["dtime"], "%Y-%m-%d %H:%M:%S")
                    next_time = datetime.strptime(window[j + 1]["dtime"], "%Y-%m-%d %H:%M:%S")
                    
                    if next_time != curr_time + timedelta(minutes=15):
                        is_continuous = False
                        break
                except (ValueError, KeyError):
                    is_continuous = False
                    break
            
            if not is_continuous:
                continue
            
            try:
                window_prices = [float(record["rce_pln"]) for record in window]
                avg_price = sum(window_prices) / len(window_prices)
                
                if best_avg_price is None:
                    best_window = window
                    best_avg_price = avg_price
                elif (is_max and avg_price > best_avg_price) or (not is_max and avg_price < best_avg_price):
                    best_window = window
                    best_avg_price = avg_price
            except (ValueError, KeyError):
                continue
        
        return best_window


class RCEBaseSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"rce_pse_{unique_id}"
        self._attr_has_entity_name = True
        self._attr_translation_key = f"rce_pse_{unique_id}"
        self.calculator = PriceCalculator()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "rce_pse")},
            "name": "RCE PSE",
            "model": "RCE PSE",
            "entry_type": "service",
            "manufacturer": MANUFACTURER,
        }

    def get_today_data(self) -> list[dict]:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        
        today = dt_util.now().strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == today
        ]

    def get_tomorrow_data(self) -> list[dict]:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == tomorrow
        ]

    def is_tomorrow_data_available(self) -> bool:
        now = dt_util.now()
        return now.hour >= 14

    def get_tomorrow_price_at_hour(self, hour: int) -> dict | None:
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
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None
        
        now = dt_util.now()
        
        for record in self.coordinator.data["raw_data"]:
            try:
                period_end = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                period_start = period_end - timedelta(minutes=15)
                
                if period_start <= now.replace(tzinfo=None) <= period_end:
                    return record
                    
            except (ValueError, KeyError):
                continue
        
        return None

    def get_price_at_future_hour(self, hours_ahead: int) -> float | None:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None
        
        target_time = dt_util.now() + timedelta(hours=hours_ahead)
        
        for record in self.coordinator.data["raw_data"]:
            try:
                period_end = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                period_start = period_end - timedelta(minutes=15)
                
                if period_start <= target_time.replace(tzinfo=None) <= period_end:
                    return float(record["rce_pln"])
                    
            except (ValueError, KeyError):
                continue
        
        return None

    def get_price_at_past_hour(self, hours_back: int) -> float | None:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None
        
        target_time = dt_util.now() - timedelta(hours=hours_back)
        closest_record = None
        closest_diff = None
        
        for record in self.coordinator.data["raw_data"]:
            try:
                period_end = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                period_start = period_end - timedelta(minutes=15)
                
                if period_start <= target_time.replace(tzinfo=None) <= period_end:
                    return float(record["rce_pln"])
                elif period_end <= target_time.replace(tzinfo=None):
                    diff = abs((target_time.replace(tzinfo=None) - period_end).total_seconds())
                    if closest_diff is None or diff < closest_diff:
                        closest_diff = diff
                        closest_record = record
            except (ValueError, KeyError):
                continue
        
        return float(closest_record["rce_pln"]) if closest_record else None

    def get_data_summary(self, data: list[dict]) -> dict[str, any]:
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
        return (
            self.coordinator.last_update_success 
            and self.coordinator.data is not None
            and self.coordinator.data.get("raw_data") is not None
        ) 