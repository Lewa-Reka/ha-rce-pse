from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.util import dt as dt_util

from ..const import CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES
from ..time_window import parse_pse_dtime
from ..shared_base import RCEBaseCommonEntity

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCEBaseSensor(RCEBaseCommonEntity, SensorEntity):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator, unique_id)

    def _period_slots_multiplier(self) -> int:
        use_hourly = self.coordinator._get_config_value(
            CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES
        )
        return 4 if use_hourly else 1

    def get_tomorrow_price_at_time(self, target_time: datetime) -> dict | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None
        
        target_hour = target_time.hour
        target_minute = (target_time.minute // 15) * 15
        
        for record in tomorrow_data:
            try:
                period_start = record["period"].split(" - ")[0]
                record_hour = int(period_start[:2])
                record_minute = int(period_start[3:5])
                if record_hour == target_hour and record_minute == target_minute:
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
                period_end = parse_pse_dtime(record["dtime"])
                period_start = period_end - timedelta(minutes=15)
                
                if period_start <= now.replace(tzinfo=None) <= period_end:
                    return record
                    
            except (ValueError, KeyError):
                continue
        
        return None

    def get_price_at_future_period(self, periods_ahead: int) -> float | None:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None

        slots = periods_ahead * self._period_slots_multiplier()
        target_time = dt_util.now().replace(tzinfo=None) + timedelta(minutes=15 * slots)

        for record in self.coordinator.data["raw_data"]:
            try:
                period_end = parse_pse_dtime(record["dtime"])
                period_start = period_end - timedelta(minutes=15)
                if period_start <= target_time <= period_end:
                    return float(record["rce_pln"])
            except (ValueError, KeyError):
                continue
        return None

    def get_price_at_past_period(self, periods_back: int) -> float | None:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return None

        slots = periods_back * self._period_slots_multiplier()
        target_time = dt_util.now().replace(tzinfo=None) - timedelta(minutes=15 * slots)
        closest_record = None
        closest_diff = None

        for record in self.coordinator.data["raw_data"]:
            try:
                period_end = parse_pse_dtime(record["dtime"])
                period_start = period_end - timedelta(minutes=15)
                if period_start <= target_time <= period_end:
                    return float(record["rce_pln"])
                if period_end <= target_time:
                    diff = abs((target_time - period_end).total_seconds())
                    if closest_diff is None or diff < closest_diff:
                        closest_diff = diff
                        closest_record = record
            except (ValueError, KeyError):
                continue
        return float(closest_record["rce_pln"]) if closest_record else None

    def get_data_summary(self, data: list[dict]) -> dict[str, Any]:
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

 