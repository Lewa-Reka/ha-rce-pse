from __future__ import annotations

from unittest.mock import patch

from custom_components.rce_pse.sensors.peak_hours import (
    _pdgsz_records_to_hourly_state,
    _pdgsz_records_to_ranges,
    RCETodayPeakHoursSensor,
    RCETomorrowPeakHoursSensor,
)


class TestPdgszRecordsToRanges:

    def test_empty_records_returns_all_keys_empty(self):
        result = _pdgsz_records_to_ranges([])
        assert result["recommended_usage"] == []
        assert result["normal_usage"] == []
        assert result["recommended_saving"] == []
        assert result["required_restriction"] == []

    def test_single_hour_single_category(self):
        records = [
            {"dtime": "2025-05-29 07:00", "business_date": "2025-05-29", "usage_fcst": 0},
        ]
        result = _pdgsz_records_to_ranges(records)
        assert result["recommended_usage"] == ["07:00–08:00"]
        assert result["normal_usage"] == []
        assert result["recommended_saving"] == []
        assert result["required_restriction"] == []

    def test_consecutive_same_fcst_merged(self):
        records = [
            {"dtime": "2025-05-29 07:00", "business_date": "2025-05-29", "usage_fcst": 0},
            {"dtime": "2025-05-29 08:00", "business_date": "2025-05-29", "usage_fcst": 0},
            {"dtime": "2025-05-29 09:00", "business_date": "2025-05-29", "usage_fcst": 0},
        ]
        result = _pdgsz_records_to_ranges(records)
        assert result["recommended_usage"] == ["07:00–10:00"]
        assert result["normal_usage"] == []

    def test_two_categories_two_ranges(self):
        records = [
            {"dtime": "2025-05-29 06:00", "business_date": "2025-05-29", "usage_fcst": 1},
            {"dtime": "2025-05-29 07:00", "business_date": "2025-05-29", "usage_fcst": 1},
            {"dtime": "2025-05-29 08:00", "business_date": "2025-05-29", "usage_fcst": 2},
            {"dtime": "2025-05-29 09:00", "business_date": "2025-05-29", "usage_fcst": 2},
        ]
        result = _pdgsz_records_to_ranges(records)
        assert result["normal_usage"] == ["06:00–08:00"]
        assert result["recommended_saving"] == ["08:00–10:00"]

    def test_usage_fcst_3_maps_to_required_restriction(self):
        records = [
            {"dtime": "2025-05-29 18:00", "business_date": "2025-05-29", "usage_fcst": 3},
        ]
        result = _pdgsz_records_to_ranges(records)
        assert result["required_restriction"] == ["18:00–19:00"]
        assert result["recommended_usage"] == []


class TestPdgszRecordsToHourlyState:

    def test_empty_returns_empty_dict(self):
        assert _pdgsz_records_to_hourly_state([]) == {}

    def test_maps_hour_to_attr_key(self):
        records = [
            {"dtime": "2025-05-29 07:00", "business_date": "2025-05-29", "usage_fcst": 0},
            {"dtime": "2025-05-29 08:00", "business_date": "2025-05-29", "usage_fcst": 2},
        ]
        result = _pdgsz_records_to_hourly_state(records)
        assert result[7] == "recommended_usage"
        assert result[8] == "recommended_saving"

    def test_skips_invalid_dtime(self):
        records = [
            {"dtime": "no-space", "usage_fcst": 0},
        ]
        assert _pdgsz_records_to_hourly_state(records) == {}


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

    def test_extra_state_attributes_records_and_hourly_states(self, mock_coordinator):
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
            assert "records" in attrs
            assert attrs["records"] == records
            assert "hourly_states" in attrs
            hourly = attrs["hourly_states"]
            assert len(hourly) == 24
            assert hourly[7] == {"hour": "07:00", "state": "recommended_usage", "state_display": "Recommended usage"}
            assert hourly[8] == {"hour": "08:00", "state": "recommended_saving", "state_display": "Recommended saving"}
            assert hourly[0]["state"] is None
            assert hourly[0]["state_display"] == ""

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

    def test_not_available_before_14(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETomorrowPeakHoursSensor(mock_coordinator)
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=False):
            assert sensor.available is False

    def test_available_after_14_when_pdgsz_present(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETomorrowPeakHoursSensor(mock_coordinator)
        with patch.object(sensor, 'is_tomorrow_data_available', return_value=True):
            assert sensor.available is True
