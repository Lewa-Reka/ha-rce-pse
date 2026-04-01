from __future__ import annotations

from custom_components.rce_pse.config_flow import (
    migrate_legacy_time_values,
    migrate_option_defaults,
    migrate_price_unit_in_mapping,
)
from custom_components.rce_pse.const import (
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_ENABLE_CHEAPEST_WINDOW,
    CONF_ENABLE_EXPENSIVE_WINDOW,
    CONF_ENABLE_HIGH_PRICE_THRESHOLD,
    CONF_ENABLE_LOW_PRICE_THRESHOLD,
    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
    CONF_LITE_MODE,
    CONF_PRICE_UNIT,
    UNIT_PLN_KWH,
    UNIT_PLN_MWH,
)


def test_migrate_legacy_time_values_maps_ints_to_hhmm():
    out = migrate_legacy_time_values(
        {
            CONF_CHEAPEST_TIME_WINDOW_START: 6,
            CONF_CHEAPEST_TIME_WINDOW_END: 24,
            CONF_CHEAPEST_WINDOW_DURATION_HOURS: 2,
        }
    )
    assert out[CONF_CHEAPEST_TIME_WINDOW_START] == "06:00"
    assert out[CONF_CHEAPEST_TIME_WINDOW_END] == "00:00"
    assert out[CONF_CHEAPEST_WINDOW_DURATION_HOURS] == "02:00"


def test_migrate_legacy_time_values_string_digits():
    out = migrate_legacy_time_values(
        {
            CONF_CHEAPEST_TIME_WINDOW_START: "8",
            CONF_CHEAPEST_TIME_WINDOW_END: "24",
            CONF_CHEAPEST_WINDOW_DURATION_HOURS: "3",
        }
    )
    assert out[CONF_CHEAPEST_TIME_WINDOW_START] == "08:00"
    assert out[CONF_CHEAPEST_TIME_WINDOW_END] == "00:00"
    assert out[CONF_CHEAPEST_WINDOW_DURATION_HOURS] == "03:00"


def test_migrate_price_unit_in_mapping_legacy_keys():
    assert migrate_price_unit_in_mapping({CONF_PRICE_UNIT: "pln_mwh"})[CONF_PRICE_UNIT] == UNIT_PLN_MWH
    assert migrate_price_unit_in_mapping({CONF_PRICE_UNIT: "pln_kwh"})[CONF_PRICE_UNIT] == UNIT_PLN_KWH


def test_migrate_price_unit_in_mapping_unchanged_when_canonical():
    assert migrate_price_unit_in_mapping({CONF_PRICE_UNIT: UNIT_PLN_MWH})[CONF_PRICE_UNIT] == UNIT_PLN_MWH
    assert migrate_price_unit_in_mapping({CONF_PRICE_UNIT: UNIT_PLN_KWH})[CONF_PRICE_UNIT] == UNIT_PLN_KWH


def test_migrate_option_defaults_adds_missing_flags():
    out = migrate_option_defaults({})
    assert out[CONF_LITE_MODE] is False
    assert out[CONF_ENABLE_CHEAPEST_WINDOW] is True
    assert out[CONF_ENABLE_EXPENSIVE_WINDOW] is True
    assert out[CONF_ENABLE_SECOND_EXPENSIVE_WINDOW] is True
    assert out[CONF_ENABLE_LOW_PRICE_THRESHOLD] is True
    assert out[CONF_ENABLE_HIGH_PRICE_THRESHOLD] is True


def test_migrate_option_defaults_preserves_existing_flags():
    out = migrate_option_defaults(
        {
            CONF_LITE_MODE: True,
            CONF_ENABLE_CHEAPEST_WINDOW: False,
            CONF_ENABLE_LOW_PRICE_THRESHOLD: False,
        }
    )
    assert out[CONF_LITE_MODE] is True
    assert out[CONF_ENABLE_CHEAPEST_WINDOW] is False
    assert out[CONF_ENABLE_LOW_PRICE_THRESHOLD] is False
