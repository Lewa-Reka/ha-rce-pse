"""Tests for RCE PSE specific sensors."""
from __future__ import annotations

from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from homeassistant.util import dt as dt_util

from custom_components.rce_pse.sensors.today_main import RCETodayMainSensor
from custom_components.rce_pse.sensors.today_stats import (
    RCETodayAvgPriceSensor,
    RCETodayMaxPriceSensor,
    RCETodayMinPriceSensor,
    RCETodayMedianPriceSensor,
    RCETodayCurrentVsAverageSensor,
)
from custom_components.rce_pse.sensors.today_prices import (
    RCENextHourPriceSensor,
    RCENext2HoursPriceSensor,
    RCENext3HoursPriceSensor,
    RCEPreviousHourPriceSensor,
)
from custom_components.rce_pse.sensors.today_hours import (
    RCETodayMinPriceRangeSensor,
    RCETodayMaxPriceRangeSensor,
)


class TestTodayMainSensors:
    """Test class for today's main price sensors."""

    def test_today_main_price_sensor_initialization(self, mock_coordinator):
        """Test today main price sensor initialization."""
        sensor = RCETodayMainSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_today_main_price_sensor_state_with_data(self, mock_coordinator):
        """Test today main price sensor state calculation."""
        sensor = RCETodayMainSensor(mock_coordinator)
        
        # Mock get_current_price_data to return specific data
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = {"rce_pln": "350.50"}
            
            state = sensor.native_value
            assert state == 350.5

    def test_today_main_price_sensor_state_no_data(self, mock_coordinator):
        """Test today main price sensor state when no data."""
        sensor = RCETodayMainSensor(mock_coordinator)
        
        # Mock get_current_price_data to return None
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = None
            
            state = sensor.native_value
            assert state is None


class TestTodayStatsSensors:
    """Test class for today's statistics sensors."""

    def test_today_average_price_sensor(self, mock_coordinator):
        """Test today average price sensor."""
        sensor = RCETodayAvgPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_today_average_price_calculation(self, mock_coordinator):
        """Test today average price calculation."""
        sensor = RCETodayAvgPriceSensor(mock_coordinator)
        
        # Mock today's data
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "350.00"},
                {"rce_pln": "400.00"},
                {"rce_pln": "320.00"},
            ]
            
            state = sensor.native_value
            assert state == 342.5  # Average of [300, 350, 400, 320]

    def test_today_max_price_sensor(self, mock_coordinator):
        """Test today maximum price sensor."""
        sensor = RCETodayMaxPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_max_price"

    def test_today_max_price_calculation(self, mock_coordinator):
        """Test today maximum price calculation."""
        sensor = RCETodayMaxPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "450.00"},  # Max
                {"rce_pln": "350.00"},
            ]
            
            state = sensor.native_value
            assert state == 450.0

    def test_today_min_price_sensor(self, mock_coordinator):
        """Test today minimum price sensor."""
        sensor = RCETodayMinPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_min_price"

    def test_today_min_price_calculation(self, mock_coordinator):
        """Test today minimum price calculation."""
        sensor = RCETodayMinPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "250.00"},  # Min
                {"rce_pln": "350.00"},
            ]
            
            state = sensor.native_value
            assert state == 250.0

    def test_today_median_price_sensor(self, mock_coordinator):
        """Test today median price sensor."""
        sensor = RCETodayMedianPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_median_price"

    def test_today_median_price_calculation(self, mock_coordinator):
        """Test today median price calculation."""
        sensor = RCETodayMedianPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "350.00"},  # Median
                {"rce_pln": "400.00"},
            ]
            
            state = sensor.native_value
            assert state == 350.0

    def test_today_current_vs_average_sensor(self, mock_coordinator):
        """Test today current vs average sensor."""
        sensor = RCETodayCurrentVsAverageSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_current_vs_average"
        assert sensor._attr_native_unit_of_measurement == "%"

    def test_today_current_vs_average_calculation(self, mock_coordinator):
        """Test current vs average percentage calculation."""
        sensor = RCETodayCurrentVsAverageSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "400.00"},
            ]  # Average = 350
            
            with patch.object(sensor, "get_current_price_data") as mock_current:
                mock_current.return_value = {"rce_pln": "420.00"}  # +20% from 350
                
                state = sensor.native_value
                assert state == pytest.approx(20.0)

    def test_stats_sensors_no_data(self, mock_coordinator):
        """Test statistics sensors behavior when no data available."""
        sensors = [
            RCETodayAvgPriceSensor(mock_coordinator),
            RCETodayMaxPriceSensor(mock_coordinator),
            RCETodayMinPriceSensor(mock_coordinator),
            RCETodayMedianPriceSensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = []
                
                state = sensor.native_value
                assert state is None


class TestTodayPriceSensors:
    """Test class for future price sensors."""

    def test_next_hour_price_sensor(self, mock_coordinator):
        """Test next hour price sensor."""
        sensor = RCENextHourPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_next_hour_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_next_hour_price_calculation(self, mock_coordinator):
        """Test next hour price calculation."""
        sensor = RCENextHourPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
            mock_future_price.return_value = 375.50
            
            state = sensor.native_value
            assert state == 375.5
            mock_future_price.assert_called_once_with(1)

    def test_price_in_2_hours_sensor(self, mock_coordinator):
        """Test price in 2 hours sensor."""
        sensor = RCENext2HoursPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_next_2_hours_price"

    def test_price_in_2_hours_calculation(self, mock_coordinator):
        """Test price in 2 hours calculation."""
        sensor = RCENext2HoursPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
            mock_future_price.return_value = 325.25
            
            state = sensor.native_value
            assert state == 325.25
            mock_future_price.assert_called_once_with(2)

    def test_price_in_3_hours_sensor(self, mock_coordinator):
        """Test price in 3 hours sensor."""
        sensor = RCENext3HoursPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_next_3_hours_price"

    def test_price_in_3_hours_calculation(self, mock_coordinator):
        """Test price in 3 hours calculation."""
        sensor = RCENext3HoursPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
            mock_future_price.return_value = 410.75
            
            state = sensor.native_value
            assert state == 410.75
            mock_future_price.assert_called_once_with(3)

    def test_previous_hour_price_sensor(self, mock_coordinator):
        """Test previous hour price sensor."""
        sensor = RCEPreviousHourPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_previous_hour_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_previous_hour_price_calculation(self, mock_coordinator):
        """Test previous hour price calculation."""
        sensor = RCEPreviousHourPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_past_hour") as mock_past_price:
            mock_past_price.return_value = 295.30
            
            state = sensor.native_value
            assert state == 295.30
            mock_past_price.assert_called_once_with(1)

    def test_future_price_sensors_no_data(self, mock_coordinator):
        """Test future price sensors when no data available."""
        sensors = [
            RCENextHourPriceSensor(mock_coordinator),
            RCENext2HoursPriceSensor(mock_coordinator),
            RCENext3HoursPriceSensor(mock_coordinator),
            RCEPreviousHourPriceSensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            if isinstance(sensor, RCEPreviousHourPriceSensor):
                with patch.object(sensor, "get_price_at_past_hour") as mock_past_price:
                    mock_past_price.return_value = None
                    
                    state = sensor.native_value
                    assert state is None
            else:
                with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
                    mock_future_price.return_value = None
                    
                    state = sensor.native_value
                    assert state is None


class TestSensorAttributes:
    """Test class for sensor attributes."""

    def test_sensor_extra_state_attributes(self, mock_coordinator):
        """Test sensor extra state attributes."""
        # Test sensor który ma extra_state_attributes (RCETodayMainSensor)
        sensor = RCETodayMainSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "350.00"},
                {"rce_pln": "400.00"},
            ]
            
            attrs = sensor.extra_state_attributes
            
            # RCETodayMainSensor ma extra_state_attributes
            assert attrs is not None
            assert "data_points" in attrs
            assert "last_update" in attrs
            assert "prices" in attrs
            assert attrs["data_points"] == 3

    def test_sensor_device_info_consistency(self, mock_coordinator):
        """Test that all sensors have consistent device info."""
        sensors = [
            RCETodayMainSensor(mock_coordinator),
            RCETodayAvgPriceSensor(mock_coordinator),
            RCENextHourPriceSensor(mock_coordinator),
        ]
        
        device_infos = [sensor.device_info for sensor in sensors]
        
        # All should have the same device info
        first_device_info = device_infos[0]
        for device_info in device_infos[1:]:
            assert device_info == first_device_info


class TestTodayRangeSensors:
    """Test class for time range sensors."""

    def test_today_min_price_range_sensor(self, mock_coordinator):
        """Test today min price range sensor."""
        sensor = RCETodayMinPriceRangeSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_min_price_range"
        assert sensor._attr_icon == "mdi:clock-time-four"

    def test_today_min_price_range_calculation(self, mock_coordinator):
        """Test today min price range calculation."""
        sensor = RCETodayMinPriceRangeSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00", "period": "10:00 - 11:00", "dtime": "2024-01-01 10:00:00"},
                {"rce_pln": "250.00", "period": "12:00 - 13:00", "dtime": "2024-01-01 12:00:00"},  # Min
                {"rce_pln": "250.00", "period": "13:00 - 14:00", "dtime": "2024-01-01 13:00:00"},  # Min
                {"rce_pln": "350.00", "period": "15:00 - 16:00", "dtime": "2024-01-01 15:00:00"},
            ]
            
            state = sensor.native_value
            assert state == "12:00 - 14:00"

    def test_today_max_price_range_sensor(self, mock_coordinator):
        """Test today max price range sensor."""
        sensor = RCETodayMaxPriceRangeSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_max_price_range"
        assert sensor._attr_icon == "mdi:clock-time-four"

    def test_today_max_price_range_calculation(self, mock_coordinator):
        """Test today max price range calculation."""
        sensor = RCETodayMaxPriceRangeSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00", "period": "10:00 - 11:00", "dtime": "2024-01-01 10:00:00"},
                {"rce_pln": "450.00", "period": "12:00 - 13:00", "dtime": "2024-01-01 12:00:00"},  # Max
                {"rce_pln": "450.00", "period": "13:00 - 14:00", "dtime": "2024-01-01 13:00:00"},  # Max
                {"rce_pln": "350.00", "period": "15:00 - 16:00", "dtime": "2024-01-01 15:00:00"},
            ]
            
            state = sensor.native_value
            assert state == "12:00 - 14:00"

    def test_range_sensors_no_data(self, mock_coordinator):
        """Test range sensors when no data available."""
        sensors = [
            RCETodayMinPriceRangeSensor(mock_coordinator),
            RCETodayMaxPriceRangeSensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = []
                
                state = sensor.native_value
                assert state is None 