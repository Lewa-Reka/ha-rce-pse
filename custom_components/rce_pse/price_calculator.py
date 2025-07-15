from __future__ import annotations

import statistics
from datetime import datetime, timedelta

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