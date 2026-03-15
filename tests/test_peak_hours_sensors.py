from __future__ import annotations

from unittest.mock import patch

from custom_components.rce_pse.sensors.peak_hours import (
    RCETodayPeakHoursSensor,
    RCETomorrowPeakHoursSensor,
)


class TestTodayPeakHoursSensor:

    def test_initialization(self, mock_coordinator):
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        assert sensor._attr_unique_id == "rce_pse_today_peak_hours"
        assert sensor._attr_icon == "mdi:flash"

    def test_native_value_with_data_returns_translated_text(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = [
            {"dtime": "2025-05-29 07:00", "business_date": "2025-05-29", "usage_fcst": 0},
            {"dtime": "2025-05-29 08:00", "business_date": "2025-05-29", "usage_fcst": 1},
        ]
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        sensor.hass = mock_coordinator.hass
        with patch.object(sensor, 'get_today_pdgsz_data') as mock_get:
            mock_get.return_value = mock_coordinator.data["pdgsz_data"]
            with patch.object(sensor, '_get_current_hour_for_state', return_value=7):
                assert sensor.native_value == "Recommended usage"
            with patch.object(sensor, '_get_current_hour_for_state', return_value=8):
                assert sensor.native_value == "Normal usage"

    def test_native_value_empty_data_returns_none(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        with patch.object(sensor, 'get_today_pdgsz_data', return_value=[]):
            assert sensor.native_value is None

    def test_extra_state_attributes_values_filtered_with_state_and_display_state(self, mock_coordinator):
        today = "2025-05-29"
        records = [
            {"dtime": f"{today} 07:00", "business_date": today, "usage_fcst": 0},
            {"dtime": f"{today} 08:00", "business_date": today, "usage_fcst": 2},
        ]
        mock_coordinator.data["pdgsz_data"] = records
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        sensor.hass = mock_coordinator.hass
        with patch.object(sensor, 'get_today_pdgsz_data') as mock_get:
            mock_get.return_value = records
            attrs = sensor.extra_state_attributes
            assert "values" in attrs
            values = attrs["values"]
            assert len(values) == 2
            assert values[0] == {
                "dtime": f"{today} 07:00",
                "usage_fcst": 0,
                "business_date": today,
                "state": "recommended_usage",
                "display_state": "Recommended usage",
            }
            assert values[1] == {
                "dtime": f"{today} 08:00",
                "usage_fcst": 2,
                "business_date": today,
                "state": "recommended_saving",
                "display_state": "Recommended saving",
            }

    def test_available_when_coordinator_has_data(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        assert sensor.available is True

    def test_available_when_no_pdgsz_data_key_native_value_none(self, mock_coordinator):
        if "pdgsz_data" in mock_coordinator.data:
            del mock_coordinator.data["pdgsz_data"]
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        assert sensor.available is True
        with patch.object(sensor, 'get_today_pdgsz_data', return_value=[]):
            assert sensor.native_value is None


class TestTomorrowPeakHoursSensor:

    def test_initialization(self, mock_coordinator):
        sensor = RCETomorrowPeakHoursSensor(mock_coordinator)
        assert sensor._attr_unique_id == "rce_pse_tomorrow_peak_hours"

    def test_available_when_coordinator_has_data_like_tomorrow_price(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETomorrowPeakHoursSensor(mock_coordinator)
        assert sensor.available is True

    def test_native_value_none_when_no_tomorrow_data_shows_unknown(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETomorrowPeakHoursSensor(mock_coordinator)
        with patch.object(sensor, 'get_tomorrow_pdgsz_data', return_value=[]):
            assert sensor.native_value is None
