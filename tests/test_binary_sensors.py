from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from homeassistant.util import dt as dt_util

from custom_components.rce_pse.binary_sensors.price_windows import (
    RCETodayMinPriceWindowBinarySensor,
    RCETodayMaxPriceWindowBinarySensor,
)
from custom_components.rce_pse.binary_sensors.custom_windows import (
    RCETodayCheapestWindowBinarySensor,
    RCETodayExpensiveWindowBinarySensor,
)


class TestTodayPriceWindowBinarySensors:

    def test_today_min_price_window_binary_sensor_initialization(self, mock_coordinator):
        sensor = RCETodayMinPriceWindowBinarySensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_min_price_window_active"
        assert sensor._attr_icon == "mdi:clock-check"

    def test_today_max_price_window_binary_sensor_initialization(self, mock_coordinator):
        sensor = RCETodayMaxPriceWindowBinarySensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_max_price_window_active"
        assert sensor._attr_icon == "mdi:clock-alert"

    def test_today_min_price_window_active_when_in_window(self, mock_coordinator):
        sensor = RCETodayMinPriceWindowBinarySensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {
                    "period": "02:00 - 02:15",
                    "rce_pln": "250.00",
                    "dtime": "2024-01-15 02:15:00"
                },
                {
                    "period": "02:15 - 02:30",
                    "rce_pln": "250.00",
                    "dtime": "2024-01-15 02:30:00"
                }
            ]
            
            with patch.object(sensor, "is_current_time_in_window") as mock_in_window:
                mock_in_window.return_value = True
                
                state = sensor.is_on
                assert state is True

    def test_today_min_price_window_inactive_when_outside_window(self, mock_coordinator):
        sensor = RCETodayMinPriceWindowBinarySensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {
                    "period": "02:00 - 02:15",
                    "rce_pln": "250.00",
                    "dtime": "2024-01-15 02:15:00"
                }
            ]
            
            with patch.object(sensor, "is_current_time_in_window") as mock_in_window:
                mock_in_window.return_value = False
                
                state = sensor.is_on
                assert state is False

    def test_today_max_price_window_active_when_in_window(self, mock_coordinator):
        sensor = RCETodayMaxPriceWindowBinarySensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {
                    "period": "18:00 - 18:15",
                    "rce_pln": "450.00",
                    "dtime": "2024-01-15 18:15:00"
                }
            ]
            
            with patch.object(sensor, "is_current_time_in_window") as mock_in_window:
                mock_in_window.return_value = True
                
                state = sensor.is_on
                assert state is True

    def test_today_max_price_window_inactive_when_outside_window(self, mock_coordinator):
        sensor = RCETodayMaxPriceWindowBinarySensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {
                    "period": "18:00 - 18:15",
                    "rce_pln": "450.00",
                    "dtime": "2024-01-15 18:15:00"
                }
            ]
            
            with patch.object(sensor, "is_current_time_in_window") as mock_in_window:
                mock_in_window.return_value = False
                
                state = sensor.is_on
                assert state is False

    def test_price_window_binary_sensors_no_data(self, mock_coordinator):
        sensors = [
            RCETodayMinPriceWindowBinarySensor(mock_coordinator),
            RCETodayMaxPriceWindowBinarySensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = []
                
                state = sensor.is_on
                assert state is False

    def test_price_window_binary_sensors_no_extreme_records(self, mock_coordinator):
        sensors = [
            RCETodayMinPriceWindowBinarySensor(mock_coordinator),
            RCETodayMaxPriceWindowBinarySensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = [
                    {"period": "10:00 - 10:15", "rce_pln": "300.00"}
                ]
                
                with patch.object(sensor.calculator, "find_extreme_price_records") as mock_find:
                    mock_find.return_value = []
                    
                    state = sensor.is_on
                    assert state is False


class TestTodayCustomWindowBinarySensors:

    def test_today_cheapest_window_binary_sensor_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETodayCheapestWindowBinarySensor(mock_coordinator, mock_config_entry)
        
        assert sensor._attr_unique_id == "rce_pse_today_cheapest_window_active"
        assert sensor._attr_icon == "mdi:clock-check"

    def test_today_expensive_window_binary_sensor_initialization(self, mock_coordinator):
        mock_config_entry = Mock()
        sensor = RCETodayExpensiveWindowBinarySensor(mock_coordinator, mock_config_entry)
        
        assert sensor._attr_unique_id == "rce_pse_today_expensive_window_active"
        assert sensor._attr_icon == "mdi:clock-alert"

    def test_today_cheapest_window_active_when_in_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        
        sensor = RCETodayCheapestWindowBinarySensor(mock_coordinator, mock_config_entry)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {
                    "period": "23:00 - 23:15",
                    "rce_pln": "200.00",
                    "dtime": "2024-01-15 23:15:00"
                },
                {
                    "period": "23:15 - 23:30",
                    "rce_pln": "200.00",
                    "dtime": "2024-01-15 23:30:00"
                }
            ]
            
            with patch.object(sensor.calculator, "find_optimal_window") as mock_find_window:
                mock_find_window.return_value = [
                    {"dtime": "2024-01-15 23:15:00"},
                    {"dtime": "2024-01-15 23:30:00"}
                ]
                
                with patch.object(sensor, "is_current_time_in_window") as mock_in_window:
                    mock_in_window.return_value = True
                    
                    state = sensor.is_on
                    assert state is True

    def test_today_expensive_window_active_when_in_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        
        sensor = RCETodayExpensiveWindowBinarySensor(mock_coordinator, mock_config_entry)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {
                    "period": "18:00 - 18:15",
                    "rce_pln": "450.00",
                    "dtime": "2024-01-15 18:15:00"
                }
            ]
            
            with patch.object(sensor.calculator, "find_optimal_window") as mock_find_window:
                mock_find_window.return_value = [
                    {"dtime": "2024-01-15 18:15:00"}
                ]
                
                with patch.object(sensor, "is_current_time_in_window") as mock_in_window:
                    mock_in_window.return_value = True
                    
                    state = sensor.is_on
                    assert state is True

    def test_custom_window_binary_sensors_no_data(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        
        sensors = [
            RCETodayCheapestWindowBinarySensor(mock_coordinator, mock_config_entry),
            RCETodayExpensiveWindowBinarySensor(mock_coordinator, mock_config_entry),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = []
                
                state = sensor.is_on
                assert state is False

    def test_custom_window_binary_sensors_no_optimal_window(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        
        sensors = [
            RCETodayCheapestWindowBinarySensor(mock_coordinator, mock_config_entry),
            RCETodayExpensiveWindowBinarySensor(mock_coordinator, mock_config_entry),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = [
                    {"period": "10:00 - 10:15", "rce_pln": "300.00"}
                ]
                
                with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                    mock_find.return_value = []
                    
                    state = sensor.is_on
                    assert state is False

    def test_custom_window_binary_sensors_exception_handling(self, mock_coordinator):
        mock_config_entry = Mock()
        mock_config_entry.data = {}
        mock_config_entry.options = {}
        
        sensors = [
            RCETodayCheapestWindowBinarySensor(mock_coordinator, mock_config_entry),
            RCETodayExpensiveWindowBinarySensor(mock_coordinator, mock_config_entry),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = [
                    {
                        "period": "10:00 - 10:15",
                        "rce_pln": "300.00",
                        "dtime": "invalid_datetime"
                    }
                ]
                
                with patch.object(sensor.calculator, "find_optimal_window") as mock_find:
                    mock_find.return_value = [
                        {"dtime": "invalid_datetime"}
                    ]
                    
                    state = sensor.is_on
                    assert state is False


class TestBinarySensorDeviceInfo:

    def test_binary_sensor_device_info_consistency(self, mock_coordinator):
        sensors = [
            RCETodayMinPriceWindowBinarySensor(mock_coordinator),
            RCETodayMaxPriceWindowBinarySensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            device_info = sensor.device_info
            
            assert device_info["name"] == "RCE PSE"
            assert device_info["model"] == "RCE PSE"
            assert device_info["entry_type"] == "service"
            assert ("rce_pse", "rce_pse") in device_info["identifiers"]

    def test_custom_binary_sensor_device_info_consistency(self, mock_coordinator):
        mock_config_entry = Mock()
        sensors = [
            RCETodayCheapestWindowBinarySensor(mock_coordinator, mock_config_entry),
            RCETodayExpensiveWindowBinarySensor(mock_coordinator, mock_config_entry),
        ]
        
        for sensor in sensors:
            device_info = sensor.device_info
            
            assert device_info["name"] == "RCE PSE"
            assert device_info["model"] == "RCE PSE"
            assert device_info["entry_type"] == "service"
            assert ("rce_pse", "rce_pse") in device_info["identifiers"]


class TestBinarySensorAvailability:

    def test_binary_sensor_availability_with_data(self, mock_coordinator):
        mock_coordinator.last_update_success = True
        mock_coordinator.data = {"raw_data": [{"test": "data"}]}
        
        sensor = RCETodayMinPriceWindowBinarySensor(mock_coordinator)
        
        assert sensor.available is True

    def test_binary_sensor_availability_no_data(self, mock_coordinator):
        mock_coordinator.last_update_success = True
        mock_coordinator.data = None
        
        sensor = RCETodayMinPriceWindowBinarySensor(mock_coordinator)
        
        assert sensor.available is False

    def test_binary_sensor_availability_update_failed(self, mock_coordinator):
        mock_coordinator.last_update_success = False
        mock_coordinator.data = {"raw_data": [{"test": "data"}]}
        
        sensor = RCETodayMinPriceWindowBinarySensor(mock_coordinator)
        
        assert sensor.available is False 