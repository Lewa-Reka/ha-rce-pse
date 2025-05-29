"""Tests for RCE PSE base sensor classes."""
from __future__ import annotations

import pytest
from unittest.mock import Mock

from custom_components.rce_pse.sensors.base import PriceCalculator, RCEBaseSensor


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