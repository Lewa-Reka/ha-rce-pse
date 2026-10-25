from __future__ import annotations

from unittest.mock import Mock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from custom_components.rce_pse.const import (
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_ENABLE_CHEAPEST_WINDOW,
    CONF_ENABLE_EXPENSIVE_WINDOW,
    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
    CONF_LITE_MODE,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_WINDOW_DURATION_HOURS,
    DOMAIN,
)
from custom_components.rce_pse.select import (
    RCEWindowTimeSelectEntity,
    async_setup_entry,
)
from custom_components.rce_pse.time_window import duration_options, start_time_options


def _config_entry(**options) -> Mock:
    mock_entry = Mock(spec=ConfigEntry)
    mock_entry.entry_id = "entry"
    mock_entry.data = {}
    mock_entry.options = options
    return mock_entry


class TestRCEWindowTimeSelectEntity:

    def test_initialization(self, mock_coordinator):
        config_entry = _config_entry()
        entity = RCEWindowTimeSelectEntity(
            mock_coordinator,
            config_entry,
            "cheapest_window_duration_hours",
            CONF_CHEAPEST_WINDOW_DURATION_HOURS,
            duration_options(),
            DEFAULT_WINDOW_DURATION_HOURS,
            "mdi:timer-outline",
        )

        assert entity._attr_unique_id == "rce_pse_cheapest_window_duration_hours"
        assert entity._attr_translation_key == "rce_pse_cheapest_window_duration_hours"
        assert entity._attr_entity_category == EntityCategory.CONFIG
        assert entity._attr_icon == "mdi:timer-outline"
        assert entity.current_option == DEFAULT_WINDOW_DURATION_HOURS
        assert "02:00" in entity.options
        assert entity.available is True

    def test_current_option_reads_from_options(self, mock_coordinator):
        config_entry = _config_entry(**{CONF_CHEAPEST_TIME_WINDOW_START: "06:15"})
        entity = RCEWindowTimeSelectEntity(
            mock_coordinator,
            config_entry,
            "cheapest_time_window_start",
            CONF_CHEAPEST_TIME_WINDOW_START,
            start_time_options(),
            DEFAULT_TIME_WINDOW_START,
            "mdi:clock-start",
        )

        assert entity.current_option == "06:15"

    def test_available_when_coordinator_has_no_data(self, mock_coordinator):
        mock_coordinator.last_update_success = False
        mock_coordinator.data = None
        config_entry = _config_entry()
        entity = RCEWindowTimeSelectEntity(
            mock_coordinator,
            config_entry,
            "cheapest_window_duration_hours",
            CONF_CHEAPEST_WINDOW_DURATION_HOURS,
            duration_options(),
            DEFAULT_WINDOW_DURATION_HOURS,
            "mdi:timer-outline",
        )

        assert entity.available is True

    @pytest.mark.asyncio
    async def test_async_select_option_updates_config_entry(self, mock_hass, mock_coordinator):
        config_entry = _config_entry(
            **{
                CONF_LITE_MODE: False,
                CONF_CHEAPEST_WINDOW_DURATION_HOURS: "02:00",
            }
        )
        entity = RCEWindowTimeSelectEntity(
            mock_coordinator,
            config_entry,
            "cheapest_window_duration_hours",
            CONF_CHEAPEST_WINDOW_DURATION_HOURS,
            duration_options(),
            DEFAULT_WINDOW_DURATION_HOURS,
            "mdi:timer-outline",
        )
        entity.hass = mock_hass
        mock_hass.config_entries = Mock()

        await entity.async_select_option("01:30")

        kwargs = mock_hass.config_entries.async_update_entry.call_args.kwargs
        assert kwargs["options"][CONF_CHEAPEST_WINDOW_DURATION_HOURS] == "01:30"
        assert kwargs["options"][CONF_LITE_MODE] is False


class TestSelectSetup:

    @pytest.mark.asyncio
    async def test_setup_adds_all_window_selects(self, mock_hass, mock_coordinator):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = _config_entry()
        added_entities = []

        await async_setup_entry(mock_hass, mock_entry, added_entities.extend)

        unique_ids = {entity._attr_unique_id for entity in added_entities}
        assert len(added_entities) == 9
        assert "rce_pse_cheapest_time_window_start" in unique_ids
        assert "rce_pse_cheapest_time_window_end" in unique_ids
        assert "rce_pse_cheapest_window_duration_hours" in unique_ids
        assert "rce_pse_expensive_time_window_start" in unique_ids
        assert "rce_pse_expensive_window_duration_hours" in unique_ids
        assert "rce_pse_second_expensive_time_window_start" in unique_ids
        assert "rce_pse_second_expensive_window_duration_hours" in unique_ids

    @pytest.mark.asyncio
    async def test_setup_in_lite_mode_adds_no_entities(self, mock_hass, mock_coordinator):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = _config_entry(**{CONF_LITE_MODE: True})
        added_entities = []

        await async_setup_entry(mock_hass, mock_entry, added_entities.extend)

        assert added_entities == []

    @pytest.mark.asyncio
    async def test_setup_skips_disabled_windows(self, mock_hass, mock_coordinator):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = _config_entry(
            **{
                CONF_ENABLE_CHEAPEST_WINDOW: False,
                CONF_ENABLE_EXPENSIVE_WINDOW: False,
                CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: True,
            }
        )
        added_entities = []

        await async_setup_entry(mock_hass, mock_entry, added_entities.extend)

        unique_ids = {entity._attr_unique_id for entity in added_entities}
        assert len(added_entities) == 3
        assert "rce_pse_cheapest_window_duration_hours" not in unique_ids
        assert "rce_pse_expensive_window_duration_hours" not in unique_ids
        assert "rce_pse_second_expensive_window_duration_hours" in unique_ids
