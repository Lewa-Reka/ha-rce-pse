from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

import pytest

from custom_components.rce_pse.sensors.today_main import RCETodayMainSensor, RCETodayProsumerSellingPriceSensor
from custom_components.rce_pse.sensors.tomorrow_main import RCETomorrowMainSensor
from custom_components.rce_pse.sensors.today_stats import (
    RCETodayAvgPriceSensor,
    RCETodayMaxPriceSensor,
    RCETodayMinPriceSensor,
    RCETodayMedianPriceSensor,
    RCETodayCurrentVsAverageSensor,
)
from custom_components.rce_pse.sensors.today_prices import (
    RCENextPeriodPriceSensor,
    RCEPreviousPeriodPriceSensor,
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

    def test_today_prosumer_selling_price_sensor_initialization(self, mock_coordinator):
        sensor = RCETodayProsumerSellingPriceSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_today_prosumer_selling_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_today_prosumer_selling_price_sensor_state_with_data(self, mock_coordinator):
        sensor = RCETodayProsumerSellingPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = {"rce_pln_neg_to_zero": "350.50"}
            
            state = sensor.native_value
            assert state == 431.12

    def test_today_prosumer_selling_price_sensor_state_no_data(self, mock_coordinator):
        sensor = RCETodayProsumerSellingPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = None
            
            state = sensor.native_value
            assert state is None

    def test_today_prosumer_selling_price_sensor_negative_price(self, mock_coordinator):
        sensor = RCETodayProsumerSellingPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = {"rce_pln_neg_to_zero": "0.00"}
            
            state = sensor.native_value
            assert state == 0

    def test_today_prosumer_selling_price_sensor_negative_to_zero_conversion(self, mock_coordinator):
        sensor = RCETodayProsumerSellingPriceSensor(mock_coordinator)
        
        with patch.object(sensor, "get_current_price_data") as mock_current_price:
            mock_current_price.return_value = {
                "rce_pln": "-50.25", 
                "rce_pln_neg_to_zero": "0.00" 
            }
            
            state = sensor.native_value
            assert state == 0


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

    def test_next_period_price_sensor(self, mock_coordinator):
        sensor = RCENextPeriodPriceSensor(mock_coordinator)

        assert sensor._attr_unique_id == "rce_pse_next_period_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_next_period_price_calculation(self, mock_coordinator):
        sensor = RCENextPeriodPriceSensor(mock_coordinator)

        with patch.object(sensor, "get_price_at_future_period") as mock_future_price:
            mock_future_price.return_value = 375.50

            state = sensor.native_value
            assert state == 375.5
            mock_future_price.assert_called_once_with(1)

    def test_previous_period_price_sensor(self, mock_coordinator):
        sensor = RCEPreviousPeriodPriceSensor(mock_coordinator)

        assert sensor._attr_unique_id == "rce_pse_previous_period_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"

    def test_previous_period_price_calculation(self, mock_coordinator):
        sensor = RCEPreviousPeriodPriceSensor(mock_coordinator)

        with patch.object(sensor, "get_price_at_past_period") as mock_past_price:
            mock_past_price.return_value = 295.30

            state = sensor.native_value
            assert state == 295.30
            mock_past_price.assert_called_once_with(1)

    def test_period_price_sensors_no_data(self, mock_coordinator):
        sensors = [
            RCENextPeriodPriceSensor(mock_coordinator),
            RCEPreviousPeriodPriceSensor(mock_coordinator),
        ]

        for sensor in sensors:
            if isinstance(sensor, RCEPreviousPeriodPriceSensor):
                with patch.object(sensor, "get_price_at_past_period") as mock_past_price:
                    mock_past_price.return_value = None

                    state = sensor.native_value
                    assert state is None
            else:
                with patch.object(sensor, "get_price_at_future_period") as mock_future_price:
                    mock_future_price.return_value = None

                    state = sensor.native_value
                    assert state is None

    def test_period_slots_multiplier_1_when_hourly_disabled(self, mock_coordinator):
        mock_coordinator._get_config_value.return_value = False
        sensor = RCENextPeriodPriceSensor(mock_coordinator)
        assert sensor._period_slots_multiplier() == 1

    def test_period_slots_multiplier_4_when_hourly_enabled(self, mock_coordinator):
        mock_coordinator._get_config_value.return_value = True
        sensor = RCENextPeriodPriceSensor(mock_coordinator)
        assert sensor._period_slots_multiplier() == 4

    def test_next_period_uses_future_period_with_15min_when_hourly_disabled(
        self, mock_coordinator, coordinator_data
    ):
        mock_coordinator._get_config_value.return_value = False
        sensor = RCENextPeriodPriceSensor(mock_coordinator)
        with patch("custom_components.rce_pse.sensors.base.dt_util.now") as mock_now:
            from datetime import datetime
            mock_now.return_value = datetime(2025, 3, 14, 10, 7, 0)
            raw = list(coordinator_data["raw_data"])
            raw.append({
                "dtime": "2025-03-14 10:30:00",
                "period": "10:15 - 10:30",
                "rce_pln": "388.50",
                "business_date": "2025-03-14",
                "publication_ts": "2025-03-14T23:00:00Z",
            })
            mock_coordinator.data = {"raw_data": raw, "last_update": ""}
            value = sensor.get_price_at_future_period(1)
            assert value == 388.5

    def test_next_period_uses_hour_when_hourly_enabled(self, mock_coordinator):
        mock_coordinator._get_config_value.return_value = True
        sensor = RCENextPeriodPriceSensor(mock_coordinator)
        raw = [{
            "dtime": "2025-03-14 11:15:00",
            "period": "11:00 - 11:15",
            "rce_pln": "450.00",
            "business_date": "2025-03-14",
            "publication_ts": "2025-03-14T23:00:00Z",
        }]
        mock_coordinator.data = {"raw_data": raw, "last_update": ""}
        with patch("custom_components.rce_pse.sensors.base.dt_util.now") as mock_now:
            from datetime import datetime
            mock_now.return_value = datetime(2025, 3, 14, 10, 0, 0)
            value = sensor.get_price_at_future_period(1)
            assert value == 450.0

    def test_previous_period_uses_past_period_with_15min_when_hourly_disabled(
        self, mock_coordinator, coordinator_data
    ):
        mock_coordinator._get_config_value.return_value = False
        sensor = RCEPreviousPeriodPriceSensor(mock_coordinator)
        with patch("custom_components.rce_pse.sensors.base.dt_util.now") as mock_now:
            from datetime import datetime
            mock_now.return_value = datetime(2025, 3, 14, 10, 22, 0)
            raw = list(coordinator_data["raw_data"])
            raw.append({
                "dtime": "2025-03-14 10:15:00",
                "period": "10:00 - 10:15",
                "rce_pln": "362.00",
                "business_date": "2025-03-14",
                "publication_ts": "2025-03-14T23:00:00Z",
            })
            mock_coordinator.data = {"raw_data": raw, "last_update": ""}
            value = sensor.get_price_at_past_period(1)
            assert value == 362.0

    def test_previous_period_uses_hour_when_hourly_enabled(self, mock_coordinator):
        mock_coordinator._get_config_value.return_value = True
        sensor = RCEPreviousPeriodPriceSensor(mock_coordinator)
        raw = [{
            "dtime": "2025-03-14 11:30:00",
            "period": "11:15 - 11:30",
            "rce_pln": "450.00",
            "business_date": "2025-03-14",
            "publication_ts": "2025-03-14T23:00:00Z",
        }]
        mock_coordinator.data = {"raw_data": raw, "last_update": ""}
        with patch("custom_components.rce_pse.sensors.base.dt_util.now") as mock_now:
            from datetime import datetime
            mock_now.return_value = datetime(2025, 3, 14, 12, 30, 0)
            value = sensor.get_price_at_past_period(1)
            assert value == 450.0


class TestSensorAttributes:

    def test_sensor_extra_state_attributes(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        
        with patch.object(sensor, "get_today_data") as mock_today_data:
            mock_today_data.return_value = [
                {"rce_pln": "300.00", "rce_pln_neg_to_zero": "0.00", "publication_ts": "2024-01-01T10:00:00Z"},
                {"rce_pln": "350.00", "publication_ts": "2024-01-01T10:15:00Z"},
                {"rce_pln": "400.00", "rce_pln_neg_to_zero": "0.00"},
            ]
            
            attrs = sensor.extra_state_attributes
            
            assert attrs is not None
            assert "data_points" in attrs
            assert "last_update" in attrs
            assert "prices" in attrs
            assert attrs["data_points"] == 3
            for rec in attrs["prices"]:
                assert "rce_pln_neg_to_zero" not in rec
                assert "publication_ts" not in rec

    def test_sensor_device_info_consistency(self, mock_coordinator):
        sensors = [
            RCETodayMainSensor(mock_coordinator),
            RCETodayAvgPriceSensor(mock_coordinator),
            RCENextPeriodPriceSensor(mock_coordinator),
        ]
        
        device_infos = [sensor.device_info for sensor in sensors]
        
        first_device_info = device_infos[0]
        for device_info in device_infos[1:]:
            assert device_info == first_device_info


class TestTomorrowMainSensor:

    def test_tomorrow_main_sensor_initialization(self, mock_coordinator):
        
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        assert sensor._attr_unique_id == "rce_pse_tomorrow_price"
        assert sensor._attr_native_unit_of_measurement == "PLN/MWh"
        assert sensor._attr_icon == "mdi:cash"

    def test_tomorrow_main_sensor_unknown_when_no_data(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        with patch('custom_components.rce_pse.sensors.base.RCEBaseSensor.available', new_callable=lambda: property(lambda self: True)):
            with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
                assert sensor.available
                assert sensor.native_value is None
            with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
                assert sensor.available

    def test_tomorrow_price_returns_current_hour_price(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)

        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                mock_now.return_value.minute = 0
                with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "350.00"}
                    
                    price = sensor.native_value
                    assert price == 350.00
                    mock_get_price.assert_called_once_with(mock_now.return_value)

                mock_now.return_value.hour = 11
                mock_now.return_value.minute = 0
                with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "375.50"}
                    
                    price = sensor.native_value
                    assert price == 375.50
                    mock_get_price.assert_called_once_with(mock_now.return_value)

    def test_tomorrow_price_no_data_for_hour(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 13
                mock_now.return_value.minute = 0
                with patch.object(sensor, 'get_tomorrow_price_at_time', return_value=None):
                    
                    price = sensor.native_value
                    assert price is None

    def test_tomorrow_price_data_not_available_yet(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            price = sensor.native_value
            assert price is None

    def test_tomorrow_price_returns_hourly_price_not_average(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)

        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 11
                mock_now.return_value.minute = 0
                
                with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "400.00"}
                    
                    price = sensor.native_value
                    
                    assert price == 400.00
                    assert price != 375.0 

    def test_tomorrow_price_extra_state_attributes_data_available(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "350.00", "rce_pln_neg_to_zero": "0.00", "publication_ts": "2024-01-01T10:00:00Z"},
            {"period": "11:00 - 11:15", "rce_pln": "375.50", "publication_ts": "2024-01-01T11:00:00Z"},
        ]
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                mock_now.return_value.minute = 0
                mock_now.return_value.isoformat.return_value = "2024-01-01T10:00:00+00:00"
                with patch.object(sensor, 'get_tomorrow_data', return_value=tomorrow_data):
                    with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                        mock_get_price.return_value = {"rce_pln": "350.00", "period": "10:00 - 10:15"}
                        
                        attrs = sensor.extra_state_attributes
                        
                        assert attrs is not None
                        assert attrs["status"] == "Available"
                        assert attrs["current_hour"] == 10
                        assert attrs["current_minute"] == 0
                        assert attrs["current_time"] == "2024-01-01T10:00:00+00:00"
                        assert attrs["data_points"] == 2
                        assert attrs["available_after"] == "14:00 CET"
                        assert "tomorrow_price_for_hour" in attrs
                        assert attrs["tomorrow_price_for_hour"]["rce_pln"] == "350.00"
                        for rec in attrs["prices"]:
                            assert "rce_pln_neg_to_zero" not in rec
                            assert "publication_ts" not in rec

    def test_tomorrow_price_extra_state_attributes_data_not_available(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                mock_now.return_value.minute = 30
                mock_now.return_value.isoformat.return_value = "2024-01-01T10:30:00+00:00"
                
                attrs = sensor.extra_state_attributes
                
                assert attrs is not None
                assert attrs["status"] == "Data not available yet"
                assert attrs["current_hour"] == 10
                assert attrs["current_minute"] == 30
                assert attrs["current_time"] == "2024-01-01T10:30:00+00:00"
                assert attrs["data_points"] == 0
                assert attrs["prices"] == []
                assert attrs["available_after"] == "14:00 CET"

    def test_tomorrow_price_with_rounding(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                mock_now.return_value.hour = 10
                mock_now.return_value.minute = 0
                
                with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                    mock_get_price.return_value = {"rce_pln": "350.456789"}
                    
                    price = sensor.native_value
                    assert price == 350.46 

    def test_tomorrow_price_sensor_scan_interval(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        assert sensor.scan_interval == timedelta(minutes=1)
        assert sensor.should_poll is True

    def test_tomorrow_price_updates_every_15_minutes(self, mock_coordinator):
        sensor = RCETomorrowMainSensor(mock_coordinator)
        
        tomorrow_data = [
            {"period": "10:00 - 10:15", "rce_pln": "300.00"},
            {"period": "10:15 - 10:30", "rce_pln": "310.00"},
            {"period": "10:30 - 10:45", "rce_pln": "320.00"},
            {"period": "10:45 - 11:00", "rce_pln": "330.00"},
        ]
        
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            with patch('homeassistant.util.dt.now') as mock_now:
                with patch.object(sensor, 'get_tomorrow_data', return_value=tomorrow_data):
                    mock_now.return_value.hour = 10
                    mock_now.return_value.minute = 5
                    with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                        mock_get_price.return_value = {"rce_pln": "300.00"}
                        price = sensor.native_value
                        assert price == 300.00
                        mock_get_price.assert_called_once_with(mock_now.return_value)
                    
                    mock_now.return_value.minute = 18
                    with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                        mock_get_price.return_value = {"rce_pln": "310.00"}
                        price = sensor.native_value
                        assert price == 310.00
                        mock_get_price.assert_called_once_with(mock_now.return_value)
                    
                    mock_now.return_value.minute = 35
                    with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                        mock_get_price.return_value = {"rce_pln": "320.00"}
                        price = sensor.native_value
                        assert price == 320.00
                        mock_get_price.assert_called_once_with(mock_now.return_value)
                    
                    mock_now.return_value.minute = 50
                    with patch.object(sensor, 'get_tomorrow_price_at_time') as mock_get_price:
                        mock_get_price.return_value = {"rce_pln": "330.00"}
                        price = sensor.native_value
                        assert price == 330.00
                        mock_get_price.assert_called_once_with(mock_now.return_value) 