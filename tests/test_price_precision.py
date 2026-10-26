from __future__ import annotations

from unittest.mock import Mock, patch

from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy

from custom_components.rce_pse.config_flow import SECTION_THRESHOLDS, _rce_form_schema
from custom_components.rce_pse.const import (
    CONF_HIGH_PRICE_THRESHOLD,
    CONF_LOW_PRICE_THRESHOLD,
    CONF_PRICE_UNIT,
    CURRENCY_PLN,
    DISPLAY_PRICE_DECIMALS,
    DISPLAY_PRICE_DECIMALS_KWH,
    THRESHOLD_STEP,
    THRESHOLD_STEP_KWH,
    UNIT_PLN_KWH,
    UNIT_PLN_MWH,
    display_price_decimals,
    threshold_selector_step_for_unit,
    threshold_step_for_unit,
)
from custom_components.rce_pse.number import RCEPriceThresholdNumberEntity
from custom_components.rce_pse.sensors.base import RCEBaseSensor
from custom_components.rce_pse.sensors.peak_hours import RCETodayPeakHoursSensor
from custom_components.rce_pse.sensors.today_hours import RCETodayMaxPriceHourStartTimestampSensor
from custom_components.rce_pse.sensors.today_main import RCETodayMainSensor
from custom_components.rce_pse.sensors.today_prices import RCENextPeriodPriceSensor
from custom_components.rce_pse.sensors.today_stats import (
    RCETodayAvgPriceSensor,
    RCETodayCurrentVsAverageSensor,
)
from custom_components.rce_pse.sensors.window_avg_price import RCETodayCheapestWindowAvgPriceSensor


def _set_price_unit(mock_coordinator, unit: str) -> None:
    def _get(key, default):
        if key == CONF_PRICE_UNIT:
            return unit
        return default

    mock_coordinator._get_config_value.side_effect = _get


def _threshold_selector_config(current_data: dict, field: str):
    schema = _rce_form_schema(current_data)
    for key, val in schema.schema.items():
        if getattr(key, "schema", None) != SECTION_THRESHOLDS:
            continue
        inner = val.schema
        for inner_key, inner_val in inner.schema.items():
            if getattr(inner_key, "schema", None) == field:
                return inner_val.config
    raise AssertionError(f"selector for {field} not found")


class TestUnitConstants:

    def test_units_use_iso_currency_and_energy(self):
        assert CURRENCY_PLN == "PLN"
        assert UNIT_PLN_MWH == f"{CURRENCY_PLN}/{UnitOfEnergy.MEGA_WATT_HOUR}"
        assert UNIT_PLN_KWH == f"{CURRENCY_PLN}/{UnitOfEnergy.KILO_WATT_HOUR}"

    def test_display_price_decimals_by_unit(self):
        assert display_price_decimals(UNIT_PLN_MWH) == DISPLAY_PRICE_DECIMALS
        assert display_price_decimals(UNIT_PLN_KWH) == DISPLAY_PRICE_DECIMALS_KWH
        assert display_price_decimals(UNIT_PLN_MWH) == 2
        assert display_price_decimals(UNIT_PLN_KWH) == 5

    def test_threshold_step_by_unit(self):
        assert threshold_step_for_unit(UNIT_PLN_MWH) == THRESHOLD_STEP
        assert threshold_step_for_unit(UNIT_PLN_KWH) == THRESHOLD_STEP_KWH
        assert threshold_step_for_unit(UNIT_PLN_MWH) == 0.01
        assert threshold_step_for_unit(UNIT_PLN_KWH) == 0.00001
        assert threshold_selector_step_for_unit(UNIT_PLN_MWH) == THRESHOLD_STEP
        assert threshold_selector_step_for_unit(UNIT_PLN_KWH) == "any"


class TestDisplayRounding:

    def test_mwh_state_keeps_two_decimals(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        with patch.object(sensor, "get_current_price_data") as mock_current:
            mock_current.return_value = {"rce_pln": "564.637"}
            assert sensor.native_value == 564.64

    def test_kwh_state_keeps_five_decimals(self, mock_coordinator):
        _set_price_unit(mock_coordinator, UNIT_PLN_KWH)
        sensor = RCETodayMainSensor(mock_coordinator)
        with patch.object(sensor, "get_current_price_data") as mock_current:
            mock_current.return_value = {"rce_pln": "0.564636"}
            assert sensor.native_value == 0.56464

    def test_kwh_state_keeps_api_scale_maximum(self, mock_coordinator):
        _set_price_unit(mock_coordinator, UNIT_PLN_KWH)
        sensor = RCETodayMainSensor(mock_coordinator)
        with patch.object(sensor, "get_current_price_data") as mock_current:
            mock_current.return_value = {"rce_pln": "5.555556"}
            assert sensor.native_value == 5.55556

    def test_kwh_prices_attribute_keeps_five_decimals(self, mock_coordinator):
        _set_price_unit(mock_coordinator, UNIT_PLN_KWH)
        sensor = RCETodayMainSensor(mock_coordinator)
        with patch.object(sensor, "get_today_data") as mock_today:
            mock_today.return_value = [
                {"rce_pln": "0.564636", "start_dtime": "2024-01-01 00:00:00"},
                {"rce_pln": "5.555554", "start_dtime": "2024-01-01 00:15:00"},
            ]
            attrs = sensor.extra_state_attributes
            assert attrs is not None
            prices = attrs["prices"]
            assert prices[0]["rce_pln"] == 0.56464
            assert prices[1]["rce_pln"] == 5.55555

    def test_mwh_prices_attribute_keeps_two_decimals(self, mock_coordinator):
        sensor = RCETodayMainSensor(mock_coordinator)
        with patch.object(sensor, "get_today_data") as mock_today:
            mock_today.return_value = [
                {"rce_pln": "564.637", "start_dtime": "2024-01-01 00:00:00"},
            ]
            attrs = sensor.extra_state_attributes
            assert attrs is not None
            prices = attrs["prices"]
            assert prices[0]["rce_pln"] == 564.64

    def test_kwh_data_summary_uses_five_decimals(self, mock_coordinator):
        _set_price_unit(mock_coordinator, UNIT_PLN_KWH)
        sensor = RCEBaseSensor(mock_coordinator, "test_sensor")
        summary = sensor.get_data_summary(
            [{"rce_pln": "0.564631"}, {"rce_pln": "0.564639"}]
        )
        assert summary["average"] == 0.56463
        assert summary["median"] == 0.56463


class TestDisplayPrecisionAndStateClass:

    def test_suggested_display_precision_follows_unit(self, mock_coordinator):
        mwh_sensor = RCETodayMainSensor(mock_coordinator)
        assert mwh_sensor._attr_suggested_display_precision == DISPLAY_PRICE_DECIMALS

        _set_price_unit(mock_coordinator, UNIT_PLN_KWH)
        kwh_sensor = RCETodayMainSensor(mock_coordinator)
        assert kwh_sensor._attr_suggested_display_precision == DISPLAY_PRICE_DECIMALS_KWH

        percent_sensor = RCETodayCurrentVsAverageSensor(mock_coordinator)
        assert percent_sensor._attr_suggested_display_precision == 1

    def test_price_sensors_use_measurement_state_class(self, mock_coordinator):
        mock_entry = Mock(spec=ConfigEntry)
        sensors = [
            RCETodayMainSensor(mock_coordinator),
            RCETodayAvgPriceSensor(mock_coordinator),
            RCETodayCurrentVsAverageSensor(mock_coordinator),
            RCENextPeriodPriceSensor(mock_coordinator),
            RCETodayCheapestWindowAvgPriceSensor(mock_coordinator, mock_entry),
        ]
        for sensor in sensors:
            assert sensor.state_class == SensorStateClass.MEASUREMENT

    def test_timestamp_and_peak_sensors_have_no_state_class(self, mock_coordinator):
        timestamp = RCETodayMaxPriceHourStartTimestampSensor(mock_coordinator)
        peak = RCETodayPeakHoursSensor(mock_coordinator)
        assert timestamp.state_class is None
        assert peak.state_class is None


class TestThresholdStep:

    def test_number_entity_step_follows_unit(self, mock_coordinator):
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.options = {}
        mock_entry.data = {}
        mwh_entity = RCEPriceThresholdNumberEntity(
            mock_coordinator,
            mock_entry,
            "low_price_threshold",
            CONF_LOW_PRICE_THRESHOLD,
            0.0,
        )
        assert mwh_entity.native_step == THRESHOLD_STEP

        _set_price_unit(mock_coordinator, UNIT_PLN_KWH)
        kwh_entity = RCEPriceThresholdNumberEntity(
            mock_coordinator,
            mock_entry,
            "low_price_threshold",
            CONF_LOW_PRICE_THRESHOLD,
            0.0,
        )
        assert kwh_entity.native_step == THRESHOLD_STEP_KWH

    def test_config_flow_threshold_selectors_follow_unit(self):
        mwh = _threshold_selector_config({}, CONF_LOW_PRICE_THRESHOLD)
        assert mwh["step"] == THRESHOLD_STEP
        assert mwh["unit_of_measurement"] == UNIT_PLN_MWH

        kwh = _threshold_selector_config(
            {CONF_PRICE_UNIT: UNIT_PLN_KWH}, CONF_HIGH_PRICE_THRESHOLD
        )
        assert kwh["step"] == "any"
        assert kwh["unit_of_measurement"] == UNIT_PLN_KWH
