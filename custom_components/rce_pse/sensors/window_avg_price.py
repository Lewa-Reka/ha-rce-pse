from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from ..coordinator import RCEPSEDataUpdateCoordinator
from ..const import (
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
)
from .custom_windows import RCECustomWindowSensor


class RCETodayCheapestWindowAvgPriceSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_cheapest_window_avg_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return None

        prices = self.calculator.get_prices_from_data(optimal_window)
        return round(self.calculator.calculate_average(prices), 2)


class RCETodayExpensiveWindowAvgPriceSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_expensive_window_avg_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        prices = self.calculator.get_prices_from_data(optimal_window)
        return round(self.calculator.calculate_average(prices), 2)


class RCETodaySecondExpensiveWindowAvgPriceSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "today_second_expensive_window_avg_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        today_data = self.get_today_data()
        if not today_data:
            return None

        start_s = self.get_config_value(
            CONF_SECOND_EXPENSIVE_TIME_WINDOW_START, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START
        )
        end_s = self.get_config_value(
            CONF_SECOND_EXPENSIVE_TIME_WINDOW_END, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END
        )
        duration = self.get_config_value(
            CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS
        )

        optimal_window = self.find_optimal_window_for_data(
            today_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        prices = self.calculator.get_prices_from_data(optimal_window)
        return round(self.calculator.calculate_average(prices), 2)


class RCETomorrowCheapestWindowAvgPriceSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_cheapest_window_avg_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

        start_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=False
        )

        if not optimal_window:
            return None

        prices = self.calculator.get_prices_from_data(optimal_window)
        return round(self.calculator.calculate_average(prices), 2)


class RCETomorrowExpensiveWindowAvgPriceSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_expensive_window_avg_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

        start_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
        end_s = self.get_config_value(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
        duration = self.get_config_value(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        prices = self.calculator.get_prices_from_data(optimal_window)
        return round(self.calculator.calculate_average(prices), 2)


class RCETomorrowSecondExpensiveWindowAvgPriceSensor(RCECustomWindowSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        super().__init__(coordinator, config_entry, "tomorrow_second_expensive_window_avg_price")
        self._attr_native_unit_of_measurement = "PLN/MWh"
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        tomorrow_data = self.get_tomorrow_data()
        if not tomorrow_data:
            return None

        start_s = self.get_config_value(
            CONF_SECOND_EXPENSIVE_TIME_WINDOW_START, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START
        )
        end_s = self.get_config_value(
            CONF_SECOND_EXPENSIVE_TIME_WINDOW_END, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END
        )
        duration = self.get_config_value(
            CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS
        )

        optimal_window = self.find_optimal_window_for_data(
            tomorrow_data, start_s, end_s, duration, is_max=True
        )

        if not optimal_window:
            return None

        prices = self.calculator.get_prices_from_data(optimal_window)
        return round(self.calculator.calculate_average(prices), 2)
