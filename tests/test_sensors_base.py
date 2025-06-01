"""Tests for RCE PSE base sensor classes."""
from __future__ import annotations

import pytest
from unittest.mock import Mock

from custom_components.rce_pse.sensors.base import PriceCalculator, RCEBaseSensor
from custom_components.rce_pse.sensors.custom_windows import RCECustomWindowSensor


class TestPriceCalculator:
    """Test class for PriceCalculator helper."""

    def test_get_prices_from_data(self):
        """Test extracting prices from data records."""
        data = [
            {"rce_pln": "350.00", "period": "00:00 - 01:00"},
            {"rce_pln": "320.50", "period": "01:00 - 02:00"},
            {"rce_pln": "280.75", "period": "02:00 - 03:00"},
        ]
        
        prices = PriceCalculator.get_prices_from_data(data)
        
        assert prices == [350.0, 320.5, 280.75]

    def test_get_prices_from_empty_data(self):
        """Test extracting prices from empty data."""
        prices = PriceCalculator.get_prices_from_data([])
        assert prices == []

    def test_calculate_average(self):
        """Test average price calculation."""
        prices = [350.0, 320.0, 280.0]
        average = PriceCalculator.calculate_average(prices)
        assert average == 316.6666666666667

    def test_calculate_average_empty_list(self):
        """Test average calculation with empty list."""
        average = PriceCalculator.calculate_average([])
        assert average == 0.0

    def test_calculate_median(self):
        """Test median price calculation."""
        prices = [350.0, 320.0, 280.0, 400.0, 290.0]
        median = PriceCalculator.calculate_median(prices)
        assert median == 320.0

    def test_calculate_median_empty_list(self):
        """Test median calculation with empty list."""
        median = PriceCalculator.calculate_median([])
        assert median == 0.0

    def test_get_hourly_prices(self):
        """Test extracting hourly prices."""
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
        """Test hourly prices extraction with invalid period formats."""
        data = [
            {"period": "00:00 - 01:00", "rce_pln": "350.00"},  # Valid
            {"period": "invalid", "rce_pln": "320.00"},        # Invalid
            {"period": "01", "rce_pln": "280.00"},             # Invalid
            {"period": "02:00 - 03:00", "rce_pln": "300.00"},  # Valid
        ]
        
        hourly_prices = PriceCalculator.get_hourly_prices(data)
        
        assert hourly_prices == {
            "00": 350.0,
            "02": 300.0,
        }

    def test_calculate_percentage_difference(self):
        """Test percentage difference calculation."""
        # Current higher than reference
        diff = PriceCalculator.calculate_percentage_difference(350.0, 300.0)
        assert diff == pytest.approx(16.666666666666668)
        
        # Current lower than reference  
        diff = PriceCalculator.calculate_percentage_difference(250.0, 300.0)
        assert diff == pytest.approx(-16.666666666666668)
        
        # Equal values
        diff = PriceCalculator.calculate_percentage_difference(300.0, 300.0)
        assert diff == 0.0

    def test_calculate_percentage_difference_zero_reference(self):
        """Test percentage difference with zero reference."""
        diff = PriceCalculator.calculate_percentage_difference(350.0, 0.0)
        assert diff == 0.0

    def test_find_extreme_price_records_max(self):
        """Test finding records with maximum price."""
        data = [
            {"dtime": "2024-01-01 10:00:00", "rce_pln": "350.00"},
            {"dtime": "2024-01-01 11:00:00", "rce_pln": "450.00"},  # Max
            {"dtime": "2024-01-01 12:00:00", "rce_pln": "300.00"},
            {"dtime": "2024-01-01 13:00:00", "rce_pln": "450.00"},  # Max
        ]
        
        max_records = PriceCalculator.find_extreme_price_records(data, is_max=True)
        
        assert len(max_records) == 2
        assert all(float(record["rce_pln"]) == 450.0 for record in max_records)
        # Should be sorted by dtime
        assert max_records[0]["dtime"] == "2024-01-01 11:00:00"
        assert max_records[1]["dtime"] == "2024-01-01 13:00:00"

    def test_find_extreme_price_records_min(self):
        """Test finding records with minimum price."""
        data = [
            {"dtime": "2024-01-01 10:00:00", "rce_pln": "350.00"},
            {"dtime": "2024-01-01 11:00:00", "rce_pln": "200.00"},  # Min
            {"dtime": "2024-01-01 12:00:00", "rce_pln": "300.00"},
            {"dtime": "2024-01-01 09:00:00", "rce_pln": "200.00"},  # Min
        ]
        
        min_records = PriceCalculator.find_extreme_price_records(data, is_max=False)
        
        assert len(min_records) == 2
        assert all(float(record["rce_pln"]) == 200.0 for record in min_records)
        # Should be sorted by dtime
        assert min_records[0]["dtime"] == "2024-01-01 09:00:00"
        assert min_records[1]["dtime"] == "2024-01-01 11:00:00"

    def test_find_extreme_price_records_empty_data(self):
        """Test finding extreme price records with empty data."""
        max_records = PriceCalculator.find_extreme_price_records([], is_max=True)
        min_records = PriceCalculator.find_extreme_price_records([], is_max=False)
        
        assert max_records == []
        assert min_records == []

    def test_find_optimal_window_cheapest(self):
        """Test finding optimal cheapest window with 15-minute intervals."""
        # Simulate 15-minute intervals: dtime is END of each period
        data = [
            {"rce_pln": "400.00", "dtime": "2024-01-01 09:00:00"},  # 08:45-09:00 (outside window)
            {"rce_pln": "300.00", "dtime": "2024-01-01 10:15:00"},  # 10:00-10:15 (cheapest window start)
            {"rce_pln": "280.00", "dtime": "2024-01-01 10:30:00"},  # 10:15-10:30
            {"rce_pln": "250.00", "dtime": "2024-01-01 10:45:00"},  # 10:30-10:45 
            {"rce_pln": "260.00", "dtime": "2024-01-01 11:00:00"},  # 10:45-11:00
            {"rce_pln": "270.00", "dtime": "2024-01-01 11:15:00"},  # 11:00-11:15
            {"rce_pln": "280.00", "dtime": "2024-01-01 11:30:00"},  # 11:15-11:30
            {"rce_pln": "290.00", "dtime": "2024-01-01 11:45:00"},  # 11:30-11:45
            {"rce_pln": "300.00", "dtime": "2024-01-01 12:00:00"},  # 11:45-12:00 (cheapest window end)
            {"rce_pln": "350.00", "dtime": "2024-01-01 15:45:00"},  # 15:30-15:45
            {"rce_pln": "450.00", "dtime": "2024-01-01 16:00:00"},  # 15:45-16:00 (window end)
            {"rce_pln": "500.00", "dtime": "2024-01-01 17:00:00"},  # 16:45-17:00 (outside window)
        ]
        
        # Find cheapest 2-hour window (8 periods) between 10:00-16:00
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 2, is_max=False)
        
        assert len(optimal_window) == 8  # 2 hours = 8 * 15-minute periods
        # Should be the window with average price 278.75: from 10:00-10:15 to 11:45-12:00
        assert optimal_window[0]["dtime"] == "2024-01-01 10:15:00"  # First period: 10:00-10:15
        assert optimal_window[-1]["dtime"] == "2024-01-01 12:00:00"  # Last period: 11:45-12:00

    def test_find_optimal_window_most_expensive(self):
        """Test finding optimal most expensive window with 15-minute intervals."""
        data = [
            {"rce_pln": "200.00", "dtime": "2024-01-01 10:15:00"},  # 10:00-10:15
            {"rce_pln": "450.00", "dtime": "2024-01-01 11:00:00"},  # 10:45-11:00 (expensive start)
            {"rce_pln": "500.00", "dtime": "2024-01-01 11:15:00"},  # 11:00-11:15
            {"rce_pln": "480.00", "dtime": "2024-01-01 11:30:00"},  # 11:15-11:30
            {"rce_pln": "470.00", "dtime": "2024-01-01 11:45:00"},  # 11:30-11:45 (expensive end)
            {"rce_pln": "300.00", "dtime": "2024-01-01 12:00:00"},  # 11:45-12:00
        ]
        
        # Find most expensive 1-hour window (4 periods) between 10:00-16:00
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=True)
        
        assert len(optimal_window) == 4  # 1 hour = 4 * 15-minute periods
        assert optimal_window[0]["dtime"] == "2024-01-01 11:00:00"  # 10:45-11:00
        assert optimal_window[-1]["dtime"] == "2024-01-01 11:45:00"  # 11:30-11:45

    def test_find_optimal_window_no_continuous_hours(self):
        """Test finding optimal window with non-continuous 15-minute periods."""
        data = [
            {"rce_pln": "300.00", "dtime": "2024-01-01 10:15:00"},  # 10:00-10:15
            {"rce_pln": "250.00", "dtime": "2024-01-01 12:15:00"},  # 12:00-12:15 (gap - missing 10:15-12:00)
            {"rce_pln": "280.00", "dtime": "2024-01-01 12:30:00"},  # 12:15-12:30
            {"rce_pln": "270.00", "dtime": "2024-01-01 12:45:00"},  # 12:30-12:45
            {"rce_pln": "260.00", "dtime": "2024-01-01 13:00:00"},  # 12:45-13:00
        ]
        
        # Try to find 1-hour continuous window (4 periods)
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=False)
        
        assert len(optimal_window) == 4  # Should find the continuous 12:00-13:00 window
        assert optimal_window[0]["dtime"] == "2024-01-01 12:15:00"
        assert optimal_window[-1]["dtime"] == "2024-01-01 13:00:00"

    def test_find_optimal_window_insufficient_data(self):
        """Test finding optimal window with insufficient 15-minute periods."""
        data = [
            {"rce_pln": "300.00", "dtime": "2024-01-01 10:15:00"},  # Only 1 period
            {"rce_pln": "320.00", "dtime": "2024-01-01 10:30:00"},  # Only 2 periods
        ]
        
        # Try to find 1-hour window (4 periods) with only 2 periods of data
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=False)
        
        assert optimal_window == []

    def test_find_optimal_window_outside_time_range(self):
        """Test finding optimal window outside specified time range."""
        data = [
            {"rce_pln": "100.00", "dtime": "2024-01-01 09:00:00"},   # 08:45-09:00 (outside)
            {"rce_pln": "200.00", "dtime": "2024-01-01 09:30:00"},   # 09:15-09:30 (outside)
            {"rce_pln": "500.00", "dtime": "2024-01-01 17:00:00"},   # 16:45-17:00 (outside)
        ]
        
        # Try to find window between 10:00-16:00 but no data in range
        optimal_window = PriceCalculator.find_optimal_window(data, 10, 16, 1, is_max=False)
        
        assert optimal_window == []

    def test_find_optimal_window_empty_data(self):
        """Test finding optimal window with empty data."""
        optimal_window = PriceCalculator.find_optimal_window([], 10, 16, 2, is_max=False)
        assert optimal_window == []


class TestRCEBaseSensor:
    """Test class for RCE base sensor."""

    def test_sensor_initialization(self, mock_coordinator):
        """Test base sensor initialization."""
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        assert sensor._attr_unique_id == "rce_pse_test_sensor"
        assert sensor._attr_has_entity_name is True
        assert sensor._attr_translation_key == "rce_pse_test_sensor"
        assert sensor.calculator is not None

    def test_device_info(self, mock_coordinator):
        """Test device info property."""
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        device_info = sensor.device_info
        
        assert device_info["name"] == "RCE PSE"
        assert device_info["model"] == "RCE PSE"
        assert device_info["entry_type"] == "service"
        assert device_info["manufacturer"] == "Lewa-Reka"
        assert ("rce_pse", "rce_pse") in device_info["identifiers"]

    def test_get_today_data(self, mock_coordinator, coordinator_data):
        """Test getting today's data."""
        from homeassistant.util import dt as dt_util
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        today = dt_util.now().strftime("%Y-%m-%d")
        
        today_data = sensor.get_today_data()
        
        assert len(today_data) == 4  # 4 records for today in sample data
        assert all(record["business_date"] == today for record in today_data)

    def test_get_tomorrow_data(self, mock_coordinator, coordinator_data):
        """Test getting tomorrow's data."""
        from homeassistant.util import dt as dt_util
        from datetime import timedelta
        
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        tomorrow_data = sensor.get_tomorrow_data()
        
        assert len(tomorrow_data) == 3  # 3 records for tomorrow in sample data
        assert all(record["business_date"] == tomorrow for record in tomorrow_data)

    def test_get_data_summary(self, mock_coordinator):
        """Test getting data summary statistics."""
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
        """Test getting summary statistics for empty data."""
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        summary = sensor.get_data_summary([])
        
        assert summary == {}

    def test_available_property_with_data(self, mock_coordinator):
        """Test sensor availability when data is present."""
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        # Mock coordinator with successful last update
        mock_coordinator.last_update_success = True
        
        assert sensor.available is True

    def test_available_property_no_data(self, mock_coordinator):
        """Test sensor availability when no data."""
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        
        # Mock coordinator with failed last update
        mock_coordinator.last_update_success = False
        
        assert sensor.available is False


class TestRCECustomWindowSensor:
    """Test class for RCE custom window sensor."""

    def test_get_config_value_from_options(self, mock_coordinator):
        """Test getting config value from options when available."""
        # Mock config entry with both data and options
        mock_config_entry = Mock()
        mock_config_entry.data = {"test_key": "data_value"}
        mock_config_entry.options = {"test_key": "options_value"}
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        # Should return value from options (higher priority)
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "options_value"

    def test_get_config_value_from_data_fallback(self, mock_coordinator):
        """Test getting config value from data when options not available."""
        # Mock config entry with only data
        mock_config_entry = Mock()
        mock_config_entry.data = {"test_key": "data_value"}
        mock_config_entry.options = None
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        # Should return value from data
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "data_value"

    def test_get_config_value_from_data_when_not_in_options(self, mock_coordinator):
        """Test getting config value from data when key not in options."""
        # Mock config entry with options but key not present there
        mock_config_entry = Mock()
        mock_config_entry.data = {"test_key": "data_value"}
        mock_config_entry.options = {"other_key": "options_value"}
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        # Should return value from data as fallback
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "data_value"

    def test_get_config_value_default(self, mock_coordinator):
        """Test getting default value when key not found anywhere."""
        # Mock config entry without the key
        mock_config_entry = Mock()
        mock_config_entry.data = {"other_key": "data_value"}
        mock_config_entry.options = {"other_key": "options_value"}
        
        sensor = RCECustomWindowSensor(mock_coordinator, mock_config_entry, "test_sensor")
        
        # Should return default value
        value = sensor.get_config_value("test_key", "default_value")
        assert value == "default_value" 