from __future__ import annotations

import pytest
from unittest.mock import Mock, MagicMock
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.rce_pse.const import CONF_CHEAPEST_TIME_WINDOW_START, CONF_CHEAPEST_TIME_WINDOW_END, CONF_CHEAPEST_WINDOW_DURATION_HOURS
from custom_components.rce_pse.sensors.base import PriceCalculator, RCEBaseSensor
from custom_components.rce_pse.sensors.custom_windows import RCECustomWindowSensor


class TestPriceCalculator:

    def test_get_prices_from_data(self):
        data = [
            {"rce_pln": "350.00", "period": "00:00 - 01:00"},
            {"rce_pln": "320.50", "period": "01:00 - 02:00"},
            {"rce_pln": "280.75", "period": "02:00 - 03:00"},
        ]
        
        prices = PriceCalculator.get_prices_from_data(data)
        
        assert prices == [350.0, 320.5, 280.75]

    def test_get_prices_from_empty_data(self):
        prices = PriceCalculator.get_prices_from_data([])
        assert prices == []

    def test_calculate_average(self):
        prices = [350.0, 320.0, 280.0]
        average = PriceCalculator.calculate_average(prices)
        assert average == 316.6666666666667

    def test_calculate_average_empty_list(self):
        average = PriceCalculator.calculate_average([])
        assert average == 0.0

    def test_calculate_median(self):
        prices = [350.0, 320.0, 280.0, 400.0, 290.0]
        median = PriceCalculator.calculate_median(prices)
        assert median == 320.0

    def test_calculate_median_empty_list(self):
        median = PriceCalculator.calculate_median([])
        assert median == 0.0

    def test_get_hourly_prices(self):
        data = [
            {"period": "00:00 - 01:00", "rce_pln": "350.00"},
            {"period": "01:00 - 02:00", "rce_pln": "320.00"},
            {"period": "02:00 - 03:00", "rce_pln": "280.00"},
        ]
        
        hourly_prices = PriceCalculator.get_hourly_prices(data)
        
        assert hourly_prices == {
            "00": 350.0,
            "01": 320.0,
            "02": 280.0,
        }

    def test_get_hourly_prices_with_invalid_periods(self):
        data = [
            {"period": "00:00 - 01:00", "rce_pln": "350.00"},
            {"period": "invalid", "rce_pln": "320.00"},
            {"period": "01", "rce_pln": "280.00"},
            {"period": "02:00 - 03:00", "rce_pln": "300.00"},
        ]
        
        hourly_prices = PriceCalculator.get_hourly_prices(data)
        
        assert hourly_prices == {
            "00": 350.0,
            "02": 300.0,
        }

    def test_calculate_percentage_difference(self):
        diff = PriceCalculator.calculate_percentage_difference(350.0, 300.0)
        assert diff == pytest.approx(16.666666666666668)
        
        diff = PriceCalculator.calculate_percentage_difference(250.0, 300.0)
        assert diff == pytest.approx(-16.666666666666668)
        
        diff = PriceCalculator.calculate_percentage_difference(300.0, 300.0)
        assert diff == 0.0

    def test_calculate_percentage_difference_zero_reference(self):
        diff = PriceCalculator.calculate_percentage_difference(350.0, 0.0)
        assert diff == 0.0

    def test_find_extreme_price_records_max(self):
        data = [
            {"dtime": "2024-01-01 10:00:00", "rce_pln": "350.00"},
            {"dtime": "2024-01-01 11:00:00", "rce_pln": "450.00"},
            {"dtime": "2024-01-01 12:00:00", "rce_pln": "300.00"},
            {"dtime": "2024-01-01 13:00:00", "rce_pln": "450.00"},
        ]
        
        max_records = PriceCalculator.find_extreme_price_records(data, is_max=True)
        
        assert len(max_records) == 2
        assert all(float(record["rce_pln"]) == 450.0 for record in max_records)
        assert max_records[0]["dtime"] == "2024-01-01 11:00:00"
        assert max_records[1]["dtime"] == "2024-01-01 13:00:00"

    def test_find_extreme_price_records_min(self):
        data = [
            {"dtime": "2024-01-01 10:00:00", "rce_pln": "350.00"},
            {"dtime": "2024-01-01 11:00:00", "rce_pln": "200.00"},
            {"dtime": "2024-01-01 12:00:00", "rce_pln": "300.00"},
            {"dtime": "2024-01-01 09:00:00", "rce_pln": "200.00"},
        ]
        
        min_records = PriceCalculator.find_extreme_price_records(data, is_max=False)
        
        assert len(min_records) == 2
        assert all(float(record["rce_pln"]) == 200.0 for record in min_records)
        assert min_records[0]["dtime"] == "2024-01-01 09:00:00"
        assert min_records[1]["dtime"] == "2024-01-01 11:00:00"

    def test_find_extreme_price_records_empty_data(self):
        max_records = PriceCalculator.find_extreme_price_records([], is_max=True)
        min_records = PriceCalculator.find_extreme_price_records([], is_max=False)
        
        assert max_records == []
        assert min_records == []

    def test_find_optimal_window_cheapest(self):
        data = [
            {"rce_pln": "400.00", "dtime": "2024-01-01 09:00:00"},
            {"rce_pln": "300.00", "dtime": "2024-01-01 10:15:00"},
            {"rce_pln": "280.00", "dtime": "2024-01-01 10:30:00"},
            {"rce_pln": "250.00", "dtime": "2024-01-01 10:45:00"},
            {"rce_pln": "260.00", "dtime": "2024-01-01 11:00:00"},
            {"rce_pln": "270.00", "dtime": "2024-01-01 11:15:00"},
            {"rce_pln": "280.00", "dtime": "2024-01-01 11:30:00"},
            {"rce_pln": "290.00", "dtime": "2024-01-01 11:45:00"},
            {"rce_pln": "300.00", "dtime": "2024-01-01 12:00:00"},
            {"rce_pln": "350.00", "dtime": "2024-01-01 15:45:00"},
            {"rce_pln": "450.00", "dtime": "2024-01-01 16:00:00"},
            {"rce_pln": "500.00", "dtime": "2024-01-01 17:00:00"},
        ]
        
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 2, is_max=False)
        
        assert len(optimal_window) == 8
        assert optimal_window[0]["dtime"] == "2024-01-01 10:15:00"
        assert optimal_window[-1]["dtime"] == "2024-01-01 12:00:00"

    def test_find_optimal_window_most_expensive(self):
        data = [
            {"rce_pln": "200.00", "dtime": "2024-01-01 10:15:00"},
            {"rce_pln": "450.00", "dtime": "2024-01-01 11:00:00"},
            {"rce_pln": "500.00", "dtime": "2024-01-01 11:15:00"},
            {"rce_pln": "480.00", "dtime": "2024-01-01 11:30:00"},
            {"rce_pln": "470.00", "dtime": "2024-01-01 11:45:00"},
            {"rce_pln": "300.00", "dtime": "2024-01-01 12:00:00"},
        ]
        
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=True)
        
        assert len(optimal_window) == 4
        assert optimal_window[0]["dtime"] == "2024-01-01 11:00:00"
        assert optimal_window[-1]["dtime"] == "2024-01-01 11:45:00"

    def test_find_optimal_window_no_continuous_hours(self):
        data = [
            {"rce_pln": "300.00", "dtime": "2024-01-01 10:15:00"},
            {"rce_pln": "250.00", "dtime": "2024-01-01 12:15:00"},
            {"rce_pln": "280.00", "dtime": "2024-01-01 12:30:00"},
            {"rce_pln": "270.00", "dtime": "2024-01-01 12:45:00"},
            {"rce_pln": "260.00", "dtime": "2024-01-01 13:00:00"},
        ]
        
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=False)
        
        assert len(optimal_window) == 4
        assert optimal_window[0]["dtime"] == "2024-01-01 12:15:00"
        assert optimal_window[-1]["dtime"] == "2024-01-01 13:00:00"

    def test_find_optimal_window_insufficient_data(self):
        data = [
            {"rce_pln": "300.00", "dtime": "2024-01-01 10:15:00"},
            {"rce_pln": "320.00", "dtime": "2024-01-01 10:30:00"},
        ]
        
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=False)
        
        assert optimal_window == []

    def test_find_optimal_window_outside_time_range(self):
        data = [
            {"rce_pln": "100.00", "dtime": "2024-01-01 09:00:00"},
            {"rce_pln": "200.00", "dtime": "2024-01-01 09:30:00"},
            {"rce_pln": "500.00", "dtime": "2024-01-01 17:00:00"},
        ]
        
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=False)
        
        assert optimal_window == []

    def test_find_optimal_window_empty_data(self):
        optimal_window = PriceCalculator.find_optimal_window([], 10, 16, 2, is_max=False)
        
        assert optimal_window == []

    def test_find_optimal_window_with_float_duration(self):
        data = [
            {"dtime": "2024-01-01 10:15:00", "rce_pln": "100.0"},
            {"dtime": "2024-01-01 10:30:00", "rce_pln": "120.0"},
            {"dtime": "2024-01-01 10:45:00", "rce_pln": "80.0"},
            {"dtime": "2024-01-01 11:00:00", "rce_pln": "90.0"},
            {"dtime": "2024-01-01 11:15:00", "rce_pln": "70.0"},
            {"dtime": "2024-01-01 11:30:00", "rce_pln": "110.0"},
            {"dtime": "2024-01-01 11:45:00", "rce_pln": "95.0"},
            {"dtime": "2024-01-01 12:00:00", "rce_pln": "85.0"},
        ]
        
        optimal_window_float = PriceCalculator.find_optimal_window(data, 10, 16, 2.0, is_max=False)
        optimal_window_int = PriceCalculator.find_optimal_window(data, 10, 16, 2, is_max=False)
        
        assert optimal_window_float == optimal_window_int
        assert len(optimal_window_float) == 8


class TestRCEBaseSensor:

    def test_sensor_initialization(self, mock_coordinator):
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        assert sensor._attr_unique_id == "rce_pse_test_sensor"
        assert sensor._attr_has_entity_name is True
        assert sensor._attr_translation_key == "rce_pse_test_sensor"
        assert sensor.calculator is not None

    def test_device_info(self, mock_coordinator):
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        device_info = sensor.device_info
        
        assert device_info["name"] == "RCE PSE"
        assert device_info["model"] == "RCE PSE"
        assert device_info["entry_type"] == "service"
        assert device_info["manufacturer"] == "Lewa-Reka"
        assert ("rce_pse", "rce_pse") in device_info["identifiers"]

    def test_get_today_data(self, mock_coordinator, coordinator_data):
        from homeassistant.util import dt as dt_util
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        today = dt_util.now().strftime("%Y-%m-%d")
        
        today_data = sensor.get_today_data()
        
        assert len(today_data) == 4
        assert all(record["business_date"] == today for record in today_data)

    def test_get_tomorrow_data(self, mock_coordinator, coordinator_data):
        from homeassistant.util import dt as dt_util
        from datetime import timedelta
        from unittest.mock import patch
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            tomorrow_data = sensor.get_tomorrow_data()
            
            assert len(tomorrow_data) == 3
            assert all(record["business_date"] == tomorrow for record in tomorrow_data)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            tomorrow_data = sensor.get_tomorrow_data()
            
            assert len(tomorrow_data) == 0

    def test_get_data_summary(self, mock_coordinator):
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        test_data = [
            {"rce_pln": "300.00"},
            {"rce_pln": "350.00"},
            {"rce_pln": "400.00"},
            {"rce_pln": "250.00"},
        ]
        
        summary = sensor.get_data_summary(test_data)
        
        assert summary["count"] == 4
        assert summary["average"] == 325.0
        assert summary["median"] == 325.0
        assert summary["min"] == 250.0
        assert summary["max"] == 400.0
        assert summary["range"] == 150.0

    def test_get_data_summary_empty_data(self, mock_coordinator):
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        summary = sensor.get_data_summary([])
        
        assert summary == {}

    def test_available_property_with_data(self, mock_coordinator):
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        mock_coordinator.last_update_success = True
        
        assert sensor.available is True

    def test_available_property_no_data(self, mock_coordinator):
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        mock_coordinator.last_update_success = False
        
        assert sensor.available is False

    def test_get_tomorrow_price_at_time_exact_match(self, mock_coordinator):
        from unittest.mock import patch
        from datetime import datetime
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "300.00"},
            {"period": "10:15 - 10:30", "rce_pln": "310.00"},
            {"period": "10:30 - 10:45", "rce_pln": "320.00"},
            {"period": "10:45 - 11:00", "rce_pln": "330.00"},
        ]
        
        with patch.object(sensor, 'get_tomorrow_data', return_value=tomorrow_data):
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 10, 0))
            assert result is not None
            assert result["rce_pln"] == "300.00"
            
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 10, 15))
            assert result is not None
            assert result["rce_pln"] == "310.00"
            
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 10, 30))
            assert result is not None
            assert result["rce_pln"] == "320.00"
            
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 10, 45))
            assert result is not None
            assert result["rce_pln"] == "330.00"

    def test_get_tomorrow_price_at_time_no_match(self, mock_coordinator):
        from unittest.mock import patch
        from datetime import datetime
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "300.00"},
            {"period": "10:15 - 10:30", "rce_pln": "310.00"},
        ]
        
        with patch.object(sensor, 'get_tomorrow_data', return_value=tomorrow_data):
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 11, 0))
            assert result is None

    def test_get_tomorrow_price_at_time_no_data(self, mock_coordinator):
        from unittest.mock import patch
        from datetime import datetime
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        with patch.object(sensor, 'get_tomorrow_data', return_value=[]):
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 10, 0))
            assert result is None

    def test_get_tomorrow_price_at_time_invalid_period_format(self, mock_coordinator):
        from unittest.mock import patch
        from datetime import datetime
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        tomorrow_data = [
            {"period": "invalid", "rce_pln": "300.00"},
            {"period": "10:15 - 10:30", "rce_pln": "310.00"},
        ]
        
        with patch.object(sensor, 'get_tomorrow_data', return_value=tomorrow_data):
            result = sensor.get_tomorrow_price_at_time(datetime(2024, 1, 1, 10, 15))
            assert result is not None
            assert result["rce_pln"] == "310.00"


class TestRCECustomWindowSensor:

    def test_get_config_value_from_options(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {"test_key": "data_value"}
        mock_config_entry.options = {"test_key": "options_value"}
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "options_value"

    def test_get_config_value_from_data_fallback(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {"test_key": "data_value"}
        mock_config_entry.options = None
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "data_value"

    def test_get_config_value_from_data_when_not_in_options(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {"test_key": "data_value"}
        mock_config_entry.options = {"other_key": "options_value"}
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "data_value"

    def test_get_config_value_default(self):
        config_entry = MockConfigEntry(
            domain="rce_pse",
            data={},
            options={}
        )
        coordinator = MagicMock()
        sensor = RCECustomWindowSensor(coordinator, config_entry, "test")
        
        value = sensor.get_config_value("non_existent_key", "default_value")
        assert value == "default_value"

    def test_get_config_value_converts_float_to_int_for_window_keys(self):
        config_entry = MockConfigEntry(
            domain="rce_pse",
            data={
                CONF_CHEAPEST_TIME_WINDOW_START: 8.0,
                CONF_CHEAPEST_TIME_WINDOW_END: 20.0,
                CONF_CHEAPEST_WINDOW_DURATION_HOURS: 2.0,
                "other_key": 5.5
            },
            options={}
        )
        coordinator = MagicMock()
        sensor = RCECustomWindowSensor(coordinator, config_entry, "test")
        
        assert sensor.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, 0) == 8
        assert type(sensor.get_config_value(CONF_CHEAPEST_TIME_WINDOW_START, 0)) == int
        
        assert sensor.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, 24) == 20
        assert type(sensor.get_config_value(CONF_CHEAPEST_TIME_WINDOW_END, 24)) == int
        
        assert sensor.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, 2) == 2
        assert type(sensor.get_config_value(CONF_CHEAPEST_WINDOW_DURATION_HOURS, 2)) == int
        
        assert sensor.get_config_value("other_key", 0) == 5.5
        assert type(sensor.get_config_value("other_key", 0)) == float 