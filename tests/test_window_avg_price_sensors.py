from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from custom_components.rce_pse.sensors.window_avg_price import (
    RCETodayCheapestWindowAvgPriceSensor,
    RCETodayExpensiveWindowAvgPriceSensor,
    RCETodaySecondExpensiveWindowAvgPriceSensor,
    RCETomorrowCheapestWindowAvgPriceSensor,
    RCETomorrowExpensiveWindowAvgPriceSensor,
    RCETomorrowSecondExpensiveWindowAvgPriceSensor,
)

SAMPLE_WINDOW_DATA = [
    {"rce_pln": "200.00", "period": "02:00 - 02:15", "dtime": "2024-01-15 02:15:00"},
    {"rce_pln": "210.00", "period": "02:15 - 02:30", "dtime": "2024-01-15 02:30:00"},
    {"rce_pln": "220.00", "period": "02:30 - 02:45", "dtime": "2024-01-15 02:45:00"},
    {"rce_pln": "230.00", "period": "02:45 - 03:00", "dtime": "2024-01-15 03:00:00"},
]

EXPECTED_AVG = round((200.0 + 210.0 + 220.0 + 230.0) / 4, 2)  # 215.0


class TestTodayCheapestWindowAvgPriceSensor:

    def test_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETodayCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        assert sensor._attr_unique_id == "rce_pse_today_cheapest_window_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodayCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = SAMPLE_WINDOW_DATA

                value = sensor.native_value
                assert value == EXPECTED_AVG

    def test_native_value_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodayCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = []

            value = sensor.native_value
            assert value is None

    def test_native_value_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodayCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = []

                value = sensor.native_value
                assert value is None


class TestTodayExpensiveWindowAvgPriceSensor:

    def test_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETodayExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        assert sensor._attr_unique_id == "rce_pse_today_expensive_window_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodayExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = SAMPLE_WINDOW_DATA

                value = sensor.native_value
                assert value == EXPECTED_AVG

    def test_native_value_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodayExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = []

            value = sensor.native_value
            assert value is None

    def test_native_value_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodayExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = []

                value = sensor.native_value
                assert value is None


class TestTodaySecondExpensiveWindowAvgPriceSensor:

    def test_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETodaySecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        assert sensor._attr_unique_id == "rce_pse_today_second_expensive_window_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodaySecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = SAMPLE_WINDOW_DATA

                value = sensor.native_value
                assert value == EXPECTED_AVG

    def test_native_value_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodaySecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = []

            value = sensor.native_value
            assert value is None

    def test_native_value_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETodaySecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = []

                value = sensor.native_value
                assert value is None


class TestTomorrowCheapestWindowAvgPriceSensor:

    def test_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETomorrowCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        assert sensor._attr_unique_id == "rce_pse_tomorrow_cheapest_window_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = SAMPLE_WINDOW_DATA

                value = sensor.native_value
                assert value == EXPECTED_AVG

    def test_native_value_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = []

            value = sensor.native_value
            assert value is None

    def test_native_value_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowCheapestWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = []

                value = sensor.native_value
                assert value is None


class TestTomorrowExpensiveWindowAvgPriceSensor:

    def test_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETomorrowExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        assert sensor._attr_unique_id == "rce_pse_tomorrow_expensive_window_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = SAMPLE_WINDOW_DATA

                value = sensor.native_value
                assert value == EXPECTED_AVG

    def test_native_value_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = []

            value = sensor.native_value
            assert value is None

    def test_native_value_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = []

                value = sensor.native_value
                assert value is None


class TestTomorrowSecondExpensiveWindowAvgPriceSensor:

    def test_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETomorrowSecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        assert sensor._attr_unique_id == "rce_pse_tomorrow_second_expensive_window_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowSecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = SAMPLE_WINDOW_DATA

                value = sensor.native_value
                assert value == EXPECTED_AVG

    def test_native_value_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowSecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = []

            value = sensor.native_value
            assert value is None

    def test_native_value_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        sensor = RCETomorrowSecondExpensiveWindowAvgPriceSensor(mock_coordinator, mock_config_entry)

        with patch.object(sensor, "get_tomorrow_data") as mock_tomorrow_data:
            mock_tomorrow_data.return_value = SAMPLE_WINDOW_DATA

            with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                mock_find.return_value = []

                value = sensor.native_value
                assert value is None
