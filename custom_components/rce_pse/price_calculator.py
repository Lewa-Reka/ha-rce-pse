from __future__ import annotations

import statistics
from datetime import timedelta

from .time_window import (
    parse_pse_dtime,
    period_bounds_for_record,
    search_window_exclusive_end,
    search_window_inclusive_start,
    period_overlaps_search,
)


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
    def find_optimal_window(
        data: list[dict],
        business_date: str,
        search_start_hhmm: str,
        search_end_hhmm: str,
        duration_minutes: int,
        is_max: bool = False,
    ) -> list[dict]:
        if not data or duration_minutes <= 0 or duration_minutes % 15 != 0:
            return []

        duration_periods = duration_minutes // 15

        search_start = search_window_inclusive_start(business_date, search_start_hhmm)
        search_end_exclusive = search_window_exclusive_end(business_date, search_end_hhmm)

        filtered_data = []
        for record in data:
            try:
                bd = record.get("business_date")
                if bd is not None and bd != business_date:
                    continue
                period_start, period_end = period_bounds_for_record(record)
                if period_overlaps_search(
                    period_start, period_end, search_start, search_end_exclusive
                ):
                    filtered_data.append(record)
            except (ValueError, KeyError):
                continue

        if len(filtered_data) < duration_periods:
            return []

        filtered_data.sort(key=lambda x: parse_pse_dtime(x["dtime"]))

        best_window = []
        best_avg_price = None

        for i in range(len(filtered_data) - duration_periods + 1):
            window = filtered_data[i : i + duration_periods]

            is_continuous = True
            for j in range(len(window) - 1):
                try:
                    curr_time = parse_pse_dtime(window[j]["dtime"])
                    next_time = parse_pse_dtime(window[j + 1]["dtime"])
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
                elif (is_max and avg_price > best_avg_price) or (
                    not is_max and avg_price < best_avg_price
                ):
                    best_window = window
                    best_avg_price = avg_price
            except (ValueError, KeyError):
                continue

        return best_window

    @staticmethod
    def find_first_window_below_threshold(data: list[dict], threshold: float) -> list[dict]:
        if not data:
            return []
        sorted_data = sorted(data, key=lambda x: x.get("dtime", ""))
        current_window: list[dict] = []
        for record in sorted_data:
            try:
                price = float(record["rce_pln"])
                if price > threshold:
                    if current_window:
                        return current_window
                    current_window = []
                    continue
                if not current_window:
                    current_window = [record]
                    continue
                prev_time = parse_pse_dtime(current_window[-1]["dtime"])
                curr_time = parse_pse_dtime(record["dtime"])
                if curr_time == prev_time + timedelta(minutes=15):
                    current_window.append(record)
                else:
                    if current_window:
                        return current_window
                    current_window = [record]
            except (ValueError, KeyError):
                if current_window:
                    return current_window
                current_window = []
        return current_window