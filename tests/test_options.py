from __future__ import annotations

from unittest.mock import Mock

import pytest
from homeassistant.config_entries import ConfigEntry

from custom_components.rce_pse.const import (
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_ENABLE_CHEAPEST_WINDOW,
    CONF_LITE_MODE,
    CONF_LOW_PRICE_THRESHOLD,
    CONF_PRICE_UNIT,
    UNIT_PLN_KWH,
)
from custom_components.rce_pse.options import (
    async_set_entry_option,
    get_effective_options,
    get_reload_options_snapshot,
)


def test_get_effective_options_merges_data_and_options():
    config_entry = Mock(spec=ConfigEntry)
    config_entry.data = {
        CONF_LITE_MODE: False,
        CONF_CHEAPEST_WINDOW_DURATION_HOURS: "02:00",
        CONF_LOW_PRICE_THRESHOLD: 0.0,
    }
    config_entry.options = {
        CONF_CHEAPEST_WINDOW_DURATION_HOURS: "03:00",
    }

    effective = get_effective_options(config_entry)

    assert effective[CONF_LITE_MODE] is False
    assert effective[CONF_CHEAPEST_WINDOW_DURATION_HOURS] == "03:00"
    assert effective[CONF_LOW_PRICE_THRESHOLD] == 0.0
    assert effective[CONF_ENABLE_CHEAPEST_WINDOW] is True


def test_get_reload_options_snapshot_ignores_window_duration():
    config_entry = Mock(spec=ConfigEntry)
    config_entry.data = {CONF_LITE_MODE: False}
    config_entry.options = {CONF_CHEAPEST_WINDOW_DURATION_HOURS: "02:00"}
    first = get_reload_options_snapshot(config_entry)

    config_entry.options = {CONF_CHEAPEST_WINDOW_DURATION_HOURS: "04:00"}
    second = get_reload_options_snapshot(config_entry)

    assert first == second


def test_get_reload_options_snapshot_changes_with_lite_mode():
    config_entry = Mock(spec=ConfigEntry)
    config_entry.data = {CONF_LITE_MODE: False}
    config_entry.options = {}
    first = get_reload_options_snapshot(config_entry)

    config_entry.options = {CONF_LITE_MODE: True}
    second = get_reload_options_snapshot(config_entry)

    assert first != second


@pytest.mark.asyncio
async def test_async_set_entry_option_writes_full_options(mock_hass):
    config_entry = Mock(spec=ConfigEntry)
    config_entry.data = {
        CONF_LITE_MODE: False,
        CONF_PRICE_UNIT: UNIT_PLN_KWH,
        CONF_CHEAPEST_WINDOW_DURATION_HOURS: "02:00",
    }
    config_entry.options = {}
    mock_hass.config_entries = Mock()

    await async_set_entry_option(
        mock_hass, config_entry, CONF_CHEAPEST_WINDOW_DURATION_HOURS, "01:30"
    )

    mock_hass.config_entries.async_update_entry.assert_called_once()
    kwargs = mock_hass.config_entries.async_update_entry.call_args.kwargs
    options = kwargs["options"]
    assert options[CONF_CHEAPEST_WINDOW_DURATION_HOURS] == "01:30"
    assert options[CONF_LITE_MODE] is False
    assert options[CONF_PRICE_UNIT] == UNIT_PLN_KWH
