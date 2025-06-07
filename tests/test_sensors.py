from __future__ import annotations

from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from homeassistant.util import dt as dt_util

from custom_components.rce_pse.sensors.today_main import RCETodayMainSensor
from custom_components.rce_pse.sensors.tomorrow_main import RCETomorrowMainSensor
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

    def test_today_main_price_sensor_initialization(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_today_main_price_sensor_state_with_data(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = {"rce_pln": "350.50"}
            
            state = sensor.native_value
            assert state == 350.5

    def test_today_main_price_sensor_state_no_data(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = None
            
            state = sensor.native_value
            assert state is None


class TestTodayStatsSensors:

    def test_today_average_price_sensor(self, mock_coordinator):
        sensor = RCETodayAvgPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_avg_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_today_average_price_calculation(self, mock_coordinator):
        sensor = RCETodayAvgPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "350.00"},
                {"rce_pln": "400.00"},
                {"rce_pln": "320.00"},
            ]
            
            state = sensor.native_value
            assert state == 342.5

    def test_today_max_price_sensor(self, mock_coordinator):
        sensor = RCETodayMaxPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_max_price"

    def test_today_max_price_calculation(self, mock_coordinator):
        sensor = RCETodayMaxPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "450.00"},
                {"rce_pln": "350.00"},
            ]
            
            state = sensor.native_value
            assert state == 450.0

    def test_today_min_price_sensor(self, mock_coordinator):
        sensor = RCETodayMinPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_min_price"

    def test_today_min_price_calculation(self, mock_coordinator):
        sensor = RCETodayMinPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "250.00"},
                {"rce_pln": "350.00"},
            ]
            
            state = sensor.native_value
            assert state == 250.0

    def test_today_median_price_sensor(self, mock_coordinator):
        sensor = RCETodayMedianPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_median_price"

    def test_today_median_price_calculation(self, mock_coordinator):
        sensor = RCETodayMedianPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "350.00"},
                {"rce_pln": "400.00"},
            ]
            
            state = sensor.native_value
            assert state == 350.0

    def test_today_current_vs_average_sensor(self, mock_coordinator):
        sensor = RCETodayCurrentVsAverageSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_current_vs_average"
        assert sensor._attr_native_unit_of_measurement == "%"

    def test_today_current_vs_average_calculation(self, mock_coordinator):
        sensor = RCETodayCurrentVsAverageSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "400.00"},
            ]
            
            with patch.object(sensor, "get_current_price_data") as mock_current:
                mock_current.return_value = {"rce_pln": "420.00"}
                
                state = sensor.native_value
                assert state == pytest.approx(20.0)

    def test_stats_sensors_no_data(self, mock_coordinator):
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

    def test_next_hour_price_sensor(self, mock_coordinator):
        sensor = RCENextHourPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_next_hour_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_next_hour_price_calculation(self, mock_coordinator):
        sensor = RCENextHourPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
            mock_future_price.return_value = 375.50
            
            state = sensor.native_value
            assert state == 375.5
            mock_future_price.assert_called_once_with(1)

    def test_price_in_2_hours_sensor(self, mock_coordinator):
        sensor = RCENext2HoursPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_next_2_hours_price"

    def test_price_in_2_hours_calculation(self, mock_coordinator):
        sensor = RCENext2HoursPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
            mock_future_price.return_value = 325.25
            
            state = sensor.native_value
            assert state == 325.25
            mock_future_price.assert_called_once_with(2)

    def test_price_in_3_hours_sensor(self, mock_coordinator):
        sensor = RCENext3HoursPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_next_3_hours_price"

    def test_price_in_3_hours_calculation(self, mock_coordinator):
        sensor = RCENext3HoursPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_future_hour") as mock_future_price:
            mock_future_price.return_value = 410.75
            
            state = sensor.native_value
            assert state == 410.75
            mock_future_price.assert_called_once_with(3)

    def test_previous_hour_price_sensor(self, mock_coordinator):
        sensor = RCEPreviousHourPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_previous_hour_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_previous_hour_price_calculation(self, mock_coordinator):
        sensor = RCEPreviousHourPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_price_at_past_hour") as mock_past_price:
            mock_past_price.return_value = 295.30
            
            state = sensor.native_value
            assert state == 295.30
            mock_past_price.assert_called_once_with(1)

    def test_future_price_sensors_no_data(self, mock_coordinator):
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

    def test_sensor_extra_state_attributes(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00"},
                {"rce_pln": "350.00"},
                {"rce_pln": "400.00"},
            ]
            
            attrs = sensor.extra_state_attributes
            
            assert attrs is not None
            assert "data_points" in attrs
            assert "last_update" in attrs
            assert "prices" in attrs
            assert attrs["data_points"] == 3

    def test_sensor_device_info_consistency(self, mock_coordinator):
        sensors = [
            RCETodayMainSensor(mock_coordinator),
            RCETodayAvgPriceSensor(mock_coordinator),
            RCENextHourPriceSensor(mock_coordinator),
        ]
        
        device_infos = [sensor.device_info for sensor in sensors]
        
        first_device_info = device_infos[0]
        for device_info in device_infos[1:]:
            assert device_info == first_device_info


class TestTodayRangeSensors:

    def test_today_min_price_range_sensor(self, mock_coordinator):
        sensor = RCETodayMinPriceRangeSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_min_price_range"
        assert sensor._attr_icon == "mdi:clock-time-four"

    def test_today_min_price_range_calculation(self, mock_coordinator):
        sensor = RCETodayMinPriceRangeSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00", "period": "10:00 - 11:00", "dtime": "2024-01-01 10:00:00"},
                {"rce_pln": "250.00", "period": "12:00 - 13:00", "dtime": "2024-01-01 12:00:00"},
                {"rce_pln": "250.00", "period": "13:00 - 14:00", "dtime": "2024-01-01 13:00:00"},
                {"rce_pln": "350.00", "period": "15:00 - 16:00", "dtime": "2024-01-01 15:00:00"},
            ]
            
            state = sensor.native_value
            assert state == "12:00 - 14:00"

    def test_today_max_price_range_sensor(self, mock_coordinator):
        sensor = RCETodayMaxPriceRangeSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_max_price_range"
        assert sensor._attr_icon == "mdi:clock-time-four"

    def test_today_max_price_range_calculation(self, mock_coordinator):
        sensor = RCETodayMaxPriceRangeSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00", "period": "10:00 - 11:00", "dtime": "2024-01-01 10:00:00"},
                {"rce_pln": "450.00", "period": "12:00 - 13:00", "dtime": "2024-01-01 12:00:00"},
                {"rce_pln": "450.00", "period": "13:00 - 14:00", "dtime": "2024-01-01 13:00:00"},
                {"rce_pln": "350.00", "period": "15:00 - 16:00", "dtime": "2024-01-01 15:00:00"},
            ]
            
            state = sensor.native_value
            assert state == "12:00 - 14:00"

    def test_range_sensors_no_data(self, mock_coordinator):
        sensors = [
            RCETodayMinPriceRangeSensor(mock_coordinator),
            RCETodayMaxPriceRangeSensor(mock_coordinator),
        ]
        
        for sensor in sensors:
            with patch.object(sensor, "get_today_data") as mock_today_data:
                mock_today_data.return_value = []
                
                state = sensor.native_value
                assert state is None


class TestTomorrowMainSensor:

    def test_tomorrow_main_sensor_initialization(self, mock_coordinator):
        
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_tomorrow_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_tomorrow_main_sensor_availability(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        

        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            with patch('custom_components.rce_pse.sensors.base.RCEBaseSensor.available', new_callable=lambda: property(lambda self: True)):
                assert not sensor.available
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('custom_components.rce_pse.sensors.base.RCEBaseSensor.available', new_callable=lambda: property(lambda self: True)):
                assert sensor.available

    def test_tomorrow_price_returns_current_hour_price(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "350.00", "business_date": "2024-01-02"},
            {"period": "11:00 - 11:15", "rce_pln": "375.50", "business_date": "2024-01-02"},
            {"period": "12:00 - 12:15", "rce_pln": "400.25", "business_date": "2024-01-02"},
        ]
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                with patch.object(sensor, 'get_tomorrow_price_at_hour') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "350.00"}
                    
                    price = sensor.native_value
                    assert price == 350.00
                    mock_get_price.assert_called_once_with(10)

                mock_now.return_value.hour = 11
                with patch.object(sensor, 'get_tomorrow_price_at_hour') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "375.50"}
                    
                    price = sensor.native_value
                    assert price == 375.50
                    mock_get_price.assert_called_once_with(11)

    def test_tomorrow_price_no_data_for_hour(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 13
                with patch.object(sensor, 'get_tomorrow_price_at_hour', return_value=None):
                    
                    price = sensor.native_value
                    assert price is None

    def test_tomorrow_price_data_not_available_yet(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            price = sensor.native_value
            assert price is None

    def test_tomorrow_price_returns_hourly_price_not_average(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "300.00"},
            {"period": "11:00 - 11:15", "rce_pln": "400.00"},
            {"period": "12:00 - 12:15", "rce_pln": "425.00"},
        ]
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 11
                
                with patch.object(sensor, 'get_tomorrow_price_at_hour') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "400.00"}
                    
                    price = sensor.native_value
                    
                    assert price == 400.00
                    assert price != 375.0 

    def test_tomorrow_price_extra_state_attributes_data_available(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "350.00"},
            {"period": "11:00 - 11:15", "rce_pln": "375.50"},
        ]
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                with patch.object(sensor, 'get_tomorrow_data', return_value=tomorrow_data):
                    with patch.object(sensor, 'get_tomorrow_price_at_hour') as mock_get_price:
                        mock_get_price.return_value = {"rce_pln": "350.00", "period": "10:00 - 10:15"}
                        
                        attrs = sensor.extra_state_attributes
                        
                        assert attrs is not None
                        assert attrs["status"] == "Available"
                        assert attrs["current_hour"] == 10
                        assert attrs["data_points"] == 2
                        assert attrs["available_after"] == "14:00 CET"
                        assert "tomorrow_price_for_hour" in attrs
                        assert attrs["tomorrow_price_for_hour"]["rce_pln"] == "350.00"

    def test_tomorrow_price_extra_state_attributes_data_not_available(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                
                attrs = sensor.extra_state_attributes
                
                assert attrs is not None
                assert attrs["status"] == "Data not available yet"
                assert attrs["current_hour"] == 10
                assert attrs["data_points"] == 0
                assert attrs["prices"] == []
                assert attrs["available_after"] == "14:00 CET"

    def test_tomorrow_price_with_rounding(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                
                with patch.object(sensor, 'get_tomorrow_price_at_hour') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "350.456789"}
                    
                    price = sensor.native_value
                    assert price == 350.46 

    def test_tomorrow_price_sensor_scan_interval(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        assert sensor.scan_interval == timedelta(minutes=1)
        assert sensor.should_poll is True 