from __future__ import annotations

from custom_components.rce_pse.config_flow import migrate_legacy_time_values
from custom_components.rce_pse.const import (
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
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
