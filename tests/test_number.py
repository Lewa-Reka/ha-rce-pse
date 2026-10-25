from __future__ import annotations

from unittest.mock import Mock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from custom_components.rce_pse.const import (
    CONF_ENABLE_HIGH_PRICE_THRESHOLD,
    CONF_ENABLE_LOW_PRICE_THRESHOLD,
    CONF_HIGH_PRICE_THRESHOLD,
    CONF_LITE_MODE,
    CONF_LOW_PRICE_THRESHOLD,
    DEFAULT_HIGH_PRICE_THRESHOLD,
    DEFAULT_LOW_PRICE_THRESHOLD,
    DOMAIN,
    THRESHOLD_MAX,
    THRESHOLD_MIN,
    THRESHOLD_STEP,
)
from custom_components.rce_pse.number import (
    RCEPriceThresholdNumberEntity,
    async_setup_entry,
)


def _config_entry(**options) -> Mock:
    mock_entry = Mock(spec=ConfigEntry)
    mock_entry.entry_id = "entry"
    mock_entry.data = {}
    mock_entry.options = options
    return mock_entry


class TestRCEPriceThresholdNumberEntity:

    def test_initialization(self, mock_coordinator):
        config_entry = _config_entry()
        entity = RCEPriceThresholdNumberEntity(
            mock_coordinator,
            config_entry,
            "low_price_threshold",
            CONF_LOW_PRICE_THRESHOLD,
            DEFAULT_LOW_PRICE_THRESHOLD,
        )

        assert entity._attr_unique_id == "rce_pse_low_price_threshold"
        assert entity._attr_translation_key == "rce_pse_low_price_threshold"
        assert entity._attr_entity_category == EntityCategory.CONFIG
        assert entity.native_min_value == THRESHOLD_MIN
        assert entity.native_max_value == THRESHOLD_MAX
        assert entity.native_step == THRESHOLD_STEP
        assert entity.native_value == DEFAULT_LOW_PRICE_THRESHOLD
        assert entity.native_unit_of_measurement == "PLN/MWh"
        assert entity.available is True

    def test_native_value_reads_from_options(self, mock_coordinator):
        config_entry = _config_entry(**{CONF_HIGH_PRICE_THRESHOLD: 450.5})
        entity = RCEPriceThresholdNumberEntity(
            mock_coordinator,
            config_entry,
            "high_price_threshold",
            CONF_HIGH_PRICE_THRESHOLD,
            DEFAULT_HIGH_PRICE_THRESHOLD,
        )

        assert entity.native_value == 450.5

    def test_available_when_coordinator_has_no_data(self, mock_coordinator):
        mock_coordinator.last_update_success = False
        mock_coordinator.data = None
        config_entry = _config_entry()
        entity = RCEPriceThresholdNumberEntity(
            mock_coordinator,
            config_entry,
            "low_price_threshold",
            CONF_LOW_PRICE_THRESHOLD,
            DEFAULT_LOW_PRICE_THRESHOLD,
        )

        assert entity.available is True

    @pytest.mark.asyncio
    async def test_async_set_native_value_updates_config_entry(
        self, mock_hass, mock_coordinator
    ):
        config_entry = _config_entry(
            **{
                CONF_LITE_MODE: False,
                CONF_LOW_PRICE_THRESHOLD: 0.0,
            }
        )
        entity = RCEPriceThresholdNumberEntity(
            mock_coordinator,
            config_entry,
            "low_price_threshold",
            CONF_LOW_PRICE_THRESHOLD,
            DEFAULT_LOW_PRICE_THRESHOLD,
        )
        entity.hass = mock_hass
        mock_hass.config_entries = Mock()

        await entity.async_set_native_value(12.5)

        kwargs = mock_hass.config_entries.async_update_entry.call_args.kwargs
        assert kwargs["options"][CONF_LOW_PRICE_THRESHOLD] == 12.5
        assert kwargs["options"][CONF_LITE_MODE] is False


class TestNumberSetup:

    @pytest.mark.asyncio
    async def test_setup_adds_threshold_numbers(self, mock_hass, mock_coordinator):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = _config_entry()
        added_entities = []

        await async_setup_entry(mock_hass, mock_entry, added_entities.extend)

        unique_ids = {entity._attr_unique_id for entity in added_entities}
        assert unique_ids == {
            "rce_pse_low_price_threshold",
            "rce_pse_high_price_threshold",
        }

    @pytest.mark.asyncio
    async def test_setup_in_lite_mode_adds_no_entities(self, mock_hass, mock_coordinator):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = _config_entry(**{CONF_LITE_MODE: True})
        added_entities = []

        await async_setup_entry(mock_hass, mock_entry, added_entities.extend)

        assert added_entities == []

    @pytest.mark.asyncio
    async def test_setup_skips_disabled_thresholds(self, mock_hass, mock_coordinator):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = _config_entry(
            **{
                CONF_ENABLE_LOW_PRICE_THRESHOLD: False,
                CONF_ENABLE_HIGH_PRICE_THRESHOLD: True,
            }
        )
        added_entities = []

        await async_setup_entry(mock_hass, mock_entry, added_entities.extend)

        unique_ids = {entity._attr_unique_id for entity in added_entities}
        assert unique_ids == {"rce_pse_high_price_threshold"}
