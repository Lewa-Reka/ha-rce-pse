from __future__ import annotations

from unittest.mock import patch

from custom_components.rce_pse.sensors.peak_hours import (
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


class TestTodayPeakHoursSensor:

    def test_initialization(self, mock_coordinator):
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        assert sensor._attr_unique_id == "rce_pse_today_peak_hours"
        assert sensor._attr_icon == "mdi:flash"

    def test_native_value_with_data(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = [
            {"dtime": "2025-05-29 07:00", "business_date": "2025-05-29", "usage_fcst": 0},
            {"dtime": "2025-05-29 08:00", "business_date": "2025-05-29", "usage_fcst": 1},
        ]
        with patch.object(mock_coordinator, 'data', mock_coordinator.data):
            sensor = RCETodayPeakHoursSensor(mock_coordinator)
            with patch.object(sensor, 'get_today_pdgsz_data') as mock_get:
                mock_get.return_value = mock_coordinator.data["pdgsz_data"]
                assert sensor.native_value == 2

    def test_native_value_empty_data(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        with patch.object(sensor, 'get_today_pdgsz_data', return_value=[]):
            assert sensor.native_value is None

    def test_extra_state_attributes_with_data(self, mock_coordinator):
        today = "2025-05-29"
        mock_coordinator.data["pdgsz_data"] = [
            {"dtime": f"{today} 07:00", "business_date": today, "usage_fcst": 0},
            {"dtime": f"{today} 08:00", "business_date": today, "usage_fcst": 2},
        ]
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        with patch.object(sensor, 'get_today_pdgsz_data') as mock_get:
            mock_get.return_value = mock_coordinator.data["pdgsz_data"]
            attrs = sensor.extra_state_attributes
            assert "recommended_usage" in attrs
            assert "recommended_saving" in attrs
            assert attrs["recommended_usage"] == ["07:00–08:00"]
            assert attrs["recommended_saving"] == ["08:00–09:00"]

    def test_available_when_pdgsz_data_present(self, mock_coordinator):
        mock_coordinator.data["pdgsz_data"] = []
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        assert sensor.available is True

    def test_not_available_when_no_pdgsz_data_key(self, mock_coordinator):
        if "pdgsz_data" in mock_coordinator.data:
            del mock_coordinator.data["pdgsz_data"]
        sensor = RCETodayPeakHoursSensor(mock_coordinator)
        assert sensor.available is False


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
