from __future__ import annotations

from unittest.mock import Mock, patch, AsyncMock

import pytest
from homeassistant.config_entries import ConfigEntry

from custom_components.rce_pse import async_migrate_entry, async_setup_entry, async_unload_entry
from custom_components.rce_pse.binary_sensor import async_setup_entry as async_setup_binary_sensors
from custom_components.rce_pse.config_flow import (
    RCEConfigFlow,
    SECTION_CHEAPEST_WINDOW,
    SECTION_EXPENSIVE_WINDOW,
    SECTION_PRICING,
    SECTION_SECOND_EXPENSIVE_WINDOW,
    SECTION_THRESHOLDS,
)
from custom_components.rce_pse.sensor import async_setup_entry as async_setup_sensors
from custom_components.rce_pse.const import (
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_ENABLE_CHEAPEST_WINDOW,
    CONF_ENABLE_EXPENSIVE_WINDOW,
    CONF_ENABLE_HIGH_PRICE_THRESHOLD,
    CONF_ENABLE_LOW_PRICE_THRESHOLD,
    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_HIGH_PRICE_THRESHOLD,
    CONF_LITE_MODE,
    CONF_LOW_PRICE_THRESHOLD,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_USE_HOURLY_PRICES,
    DOMAIN,
)


class TestRCEPSEIntegration:

    @pytest.mark.asyncio
    async def test_async_setup_entry_success(self, mock_hass):
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.runtime_data = None
        mock_entry.entry_id = "test_entry_id"
        
        with patch("custom_components.rce_pse.RCEPSEDataUpdateCoordinator") as mock_coordinator_class:
            mock_coordinator = Mock()
            mock_coordinator_class.return_value = mock_coordinator
            mock_coordinator.async_config_entry_first_refresh = AsyncMock()
            
            mock_hass.config_entries = Mock()
            mock_hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
                
            result = await async_setup_entry(mock_hass, mock_entry)
                
            assert result is True
            mock_coordinator_class.assert_called_once_with(mock_hass, mock_entry)
            mock_coordinator.async_config_entry_first_refresh.assert_called_once()
            assert mock_hass.data[DOMAIN][mock_entry.entry_id] == mock_coordinator

    @pytest.mark.asyncio
    async def test_async_unload_entry_success(self, mock_hass):
        mock_coordinator = Mock()
        mock_coordinator.async_close = AsyncMock()
        
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.runtime_data = mock_coordinator
        mock_entry.entry_id = "test_entry_id"
        
        mock_hass.data[DOMAIN] = {mock_entry.entry_id: mock_coordinator}
        
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)
            
        result = await async_unload_entry(mock_hass, mock_entry)
            
        assert result is True
        mock_coordinator.async_close.assert_called_once()
        mock_hass.config_entries.async_unload_platforms.assert_called_once_with(
            mock_entry, ["sensor", "binary_sensor"]
        )
        assert mock_entry.entry_id not in mock_hass.data[DOMAIN]

    @pytest.mark.asyncio
    async def test_async_migrate_entry_adds_new_option_flags(self, mock_hass):
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.version = 2
        mock_entry.data = {}
        mock_entry.options = {}
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.async_update_entry = Mock()

        result = await async_migrate_entry(mock_hass, mock_entry)

        assert result is True
        kwargs = mock_hass.config_entries.async_update_entry.call_args.kwargs
        assert kwargs["version"] == 3
        assert kwargs["data"][CONF_LITE_MODE] is False
        assert kwargs["options"][CONF_ENABLE_CHEAPEST_WINDOW] is True
        assert kwargs["options"][CONF_ENABLE_HIGH_PRICE_THRESHOLD] is True


class TestEntitySetupOptions:

    @pytest.mark.asyncio
    async def test_sensor_setup_in_lite_mode_adds_only_two_main_sensors(
        self, mock_hass, mock_coordinator
    ):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_hass.async_add_executor_job = AsyncMock()
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.entry_id = "entry"
        mock_entry.data = {CONF_LITE_MODE: True}
        mock_entry.options = {}
        added_entities = []

        await async_setup_sensors(mock_hass, mock_entry, added_entities.extend)

        assert len(added_entities) == 2
        assert {entity._attr_unique_id for entity in added_entities} == {
            "rce_pse_today_price",
            "rce_pse_tomorrow_price",
        }
        mock_hass.async_add_executor_job.assert_not_called()

    @pytest.mark.asyncio
    async def test_sensor_setup_skips_disabled_windows_and_thresholds(
        self, mock_hass, mock_coordinator
    ):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_hass.async_add_executor_job = AsyncMock()
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.entry_id = "entry"
        mock_entry.data = {}
        mock_entry.options = {
            CONF_ENABLE_CHEAPEST_WINDOW: False,
            CONF_ENABLE_EXPENSIVE_WINDOW: False,
            CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: False,
            CONF_ENABLE_LOW_PRICE_THRESHOLD: False,
            CONF_ENABLE_HIGH_PRICE_THRESHOLD: False,
        }
        added_entities = []

        await async_setup_sensors(mock_hass, mock_entry, added_entities.extend)

        unique_ids = {entity._attr_unique_id for entity in added_entities}
        assert "rce_pse_today_cheapest_window_start" not in unique_ids
        assert "rce_pse_today_expensive_window_start" not in unique_ids
        assert "rce_pse_today_second_expensive_window_start" not in unique_ids
        assert "rce_pse_low_price_threshold_window_start" not in unique_ids
        assert "rce_pse_high_price_threshold_window_start" not in unique_ids
        assert "rce_pse_today_avg_price" in unique_ids

    @pytest.mark.asyncio
    async def test_binary_sensor_setup_in_lite_mode_adds_no_entities(
        self, mock_hass, mock_coordinator
    ):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.entry_id = "entry"
        mock_entry.data = {CONF_LITE_MODE: True}
        mock_entry.options = {}
        added_entities = []

        await async_setup_binary_sensors(mock_hass, mock_entry, added_entities.extend)

        assert added_entities == []

    @pytest.mark.asyncio
    async def test_binary_sensor_setup_skips_disabled_optional_features(
        self, mock_hass, mock_coordinator
    ):
        mock_hass.data[DOMAIN] = {"entry": mock_coordinator}
        mock_entry = Mock(spec=ConfigEntry)
        mock_entry.entry_id = "entry"
        mock_entry.data = {}
        mock_entry.options = {
            CONF_ENABLE_CHEAPEST_WINDOW: False,
            CONF_ENABLE_EXPENSIVE_WINDOW: False,
            CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: False,
            CONF_ENABLE_LOW_PRICE_THRESHOLD: False,
            CONF_ENABLE_HIGH_PRICE_THRESHOLD: False,
        }
        added_entities = []

        await async_setup_binary_sensors(mock_hass, mock_entry, added_entities.extend)

        unique_ids = {entity._attr_unique_id for entity in added_entities}
        assert unique_ids == {
            "rce_pse_today_min_price_window_active",
            "rce_pse_today_max_price_window_active",
        }


class TestRCEPSEConfigFlow:

    @pytest.mark.asyncio
    async def test_config_flow_init(self):
        flow = RCEConfigFlow()
        
        assert flow.VERSION == 3
        assert flow.MINOR_VERSION == 0

    @pytest.mark.asyncio
    async def test_config_flow_user_step_success(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        flow.flow_id = "test_flow_id"
        flow.context = {}
        
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.flow = Mock()
        mock_hass.config_entries.flow.async_progress_by_handler = Mock(return_value=[])
        mock_hass.config_entries.async_entry_for_domain_unique_id = Mock(return_value=None)
        
        with patch.object(flow, "_async_current_entries", return_value=[]):
            with patch.object(flow, "async_create_entry") as mock_create_entry:
                mock_create_entry.return_value = {"type": "create_entry"}
                
                result = await flow.async_step_user(user_input={})
                
                assert result.get("type") == "create_entry"
                mock_create_entry.assert_called_once_with(title="RCE PSE", data={})

    @pytest.mark.asyncio
    async def test_config_flow_user_step_with_hourly_prices_option(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        flow.flow_id = "test_flow_id"
        flow.context = {}
        
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.flow = Mock()
        mock_hass.config_entries.flow.async_progress_by_handler = Mock(return_value=[])
        mock_hass.config_entries.async_entry_for_domain_unique_id = Mock(return_value=None)
        
        with patch.object(flow, "_async_current_entries", return_value=[]):
            with patch.object(flow, "async_create_entry") as mock_create_entry:
                mock_create_entry.return_value = {"type": "create_entry"}
                
                user_input = {"use_hourly_prices": True}
                result = await flow.async_step_user(user_input=user_input)
                
                assert result.get("type") == "create_entry"
                mock_create_entry.assert_called_once_with(title="RCE PSE", data=user_input)

    @pytest.mark.asyncio
    async def test_config_flow_user_step_with_price_thresholds(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        flow.flow_id = "test_flow_id"
        flow.context = {}
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.flow = Mock()
        mock_hass.config_entries.flow.async_progress_by_handler = Mock(return_value=[])
        mock_hass.config_entries.async_entry_for_domain_unique_id = Mock(return_value=None)
        with patch.object(flow, "_async_current_entries", return_value=[]):
            with patch.object(flow, "async_set_unique_id"):
                with patch.object(flow, "_abort_if_unique_id_configured"):
                    with patch.object(flow, "async_create_entry") as mock_create_entry:
                        mock_create_entry.return_value = {"type": "create_entry"}
                        user_input = {
                            "cheapest_time_window_start": 0,
                            "cheapest_time_window_end": 24,
                            "cheapest_window_duration_hours": 2,
                            "expensive_time_window_start": 0,
                            "expensive_time_window_end": 24,
                            "expensive_window_duration_hours": 2,
                            "second_expensive_time_window_start": 6,
                            "second_expensive_time_window_end": 10,
                            "second_expensive_window_duration_hours": 2,
                            "low_price_threshold": 50.0,
                            "high_price_threshold": 400.0,
                        }
                        result = await flow.async_step_user(user_input=user_input)
                        assert result.get("type") == "create_entry"
                        mock_create_entry.assert_called_once()
                        call_data = mock_create_entry.call_args[1]["data"]
                        assert call_data.get("low_price_threshold") == 50.0
                        assert call_data.get("high_price_threshold") == 400.0

    @pytest.mark.asyncio
    async def test_config_flow_user_step_nested_sections_stored_flat(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        flow.flow_id = "test_flow_id"
        flow.context = {}
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.flow = Mock()
        mock_hass.config_entries.flow.async_progress_by_handler = Mock(return_value=[])
        mock_hass.config_entries.async_entry_for_domain_unique_id = Mock(return_value=None)
        user_input = {
            SECTION_PRICING: {CONF_USE_HOURLY_PRICES: True, CONF_LITE_MODE: False},
            SECTION_CHEAPEST_WINDOW: {
                CONF_ENABLE_CHEAPEST_WINDOW: True,
                CONF_CHEAPEST_TIME_WINDOW_START: 0,
                CONF_CHEAPEST_TIME_WINDOW_END: 24,
                CONF_CHEAPEST_WINDOW_DURATION_HOURS: 2,
            },
            SECTION_EXPENSIVE_WINDOW: {
                CONF_ENABLE_EXPENSIVE_WINDOW: True,
                CONF_EXPENSIVE_TIME_WINDOW_START: 0,
                CONF_EXPENSIVE_TIME_WINDOW_END: 24,
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS: 2,
            },
            SECTION_SECOND_EXPENSIVE_WINDOW: {
                CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: True,
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START: 6,
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END: 10,
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS: 2,
            },
            SECTION_THRESHOLDS: {
                CONF_ENABLE_LOW_PRICE_THRESHOLD: True,
                CONF_LOW_PRICE_THRESHOLD: 0.0,
                CONF_ENABLE_HIGH_PRICE_THRESHOLD: True,
                CONF_HIGH_PRICE_THRESHOLD: 1000.0,
            },
        }
        with patch.object(flow, "_async_current_entries", return_value=[]):
            with patch.object(flow, "async_set_unique_id"):
                with patch.object(flow, "_abort_if_unique_id_configured"):
                    with patch.object(flow, "async_create_entry") as mock_create_entry:
                        mock_create_entry.return_value = {"type": "create_entry"}
                        result = await flow.async_step_user(user_input=user_input)
                        assert result.get("type") == "create_entry"
                        call_data = mock_create_entry.call_args[1]["data"]
                        assert call_data[CONF_USE_HOURLY_PRICES] is True
                        assert call_data[CONF_LITE_MODE] is False
                        assert SECTION_PRICING not in call_data
                        assert call_data[CONF_CHEAPEST_TIME_WINDOW_START] == "00:00"
                        assert call_data[CONF_CHEAPEST_TIME_WINDOW_END] == "00:00"
                        assert call_data[CONF_CHEAPEST_WINDOW_DURATION_HOURS] == "02:00"
                        assert call_data[CONF_EXPENSIVE_TIME_WINDOW_START] == "00:00"
                        assert call_data[CONF_EXPENSIVE_TIME_WINDOW_END] == "00:00"
                        assert call_data[CONF_SECOND_EXPENSIVE_TIME_WINDOW_START] == "06:00"
                        assert call_data[CONF_SECOND_EXPENSIVE_TIME_WINDOW_END] == "10:00"
                        assert call_data[CONF_ENABLE_LOW_PRICE_THRESHOLD] is True
                        assert call_data[CONF_HIGH_PRICE_THRESHOLD] == 1000.0

    @pytest.mark.asyncio
    async def test_config_flow_allows_invalid_disabled_window(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        flow.flow_id = "test_flow_id"
        flow.context = {}
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.flow = Mock()
        mock_hass.config_entries.flow.async_progress_by_handler = Mock(return_value=[])
        mock_hass.config_entries.async_entry_for_domain_unique_id = Mock(return_value=None)
        user_input = {
            SECTION_PRICING: {CONF_LITE_MODE: False},
            SECTION_CHEAPEST_WINDOW: {
                CONF_ENABLE_CHEAPEST_WINDOW: False,
                CONF_CHEAPEST_TIME_WINDOW_START: "20:00",
                CONF_CHEAPEST_TIME_WINDOW_END: "10:00",
                CONF_CHEAPEST_WINDOW_DURATION_HOURS: "12:00",
            },
            SECTION_EXPENSIVE_WINDOW: {
                CONF_ENABLE_EXPENSIVE_WINDOW: True,
                CONF_EXPENSIVE_TIME_WINDOW_START: "00:00",
                CONF_EXPENSIVE_TIME_WINDOW_END: "23:00",
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS: "02:00",
            },
            SECTION_SECOND_EXPENSIVE_WINDOW: {
                CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: True,
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START: "06:00",
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END: "10:00",
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS: "02:00",
            },
            SECTION_THRESHOLDS: {
                CONF_ENABLE_LOW_PRICE_THRESHOLD: True,
                CONF_LOW_PRICE_THRESHOLD: 0.0,
                CONF_ENABLE_HIGH_PRICE_THRESHOLD: True,
                CONF_HIGH_PRICE_THRESHOLD: 1000.0,
            },
        }
        with patch.object(flow, "_async_current_entries", return_value=[]):
            with patch.object(flow, "async_set_unique_id"):
                with patch.object(flow, "_abort_if_unique_id_configured"):
                    with patch.object(flow, "async_create_entry") as mock_create_entry:
                        mock_create_entry.return_value = {"type": "create_entry"}
                        result = await flow.async_step_user(user_input=user_input)
                        assert result.get("type") == "create_entry"

    @pytest.mark.asyncio
    async def test_config_flow_lite_mode_skips_window_validation(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        flow.flow_id = "test_flow_id"
        flow.context = {}
        mock_hass.config_entries = Mock()
        mock_hass.config_entries.flow = Mock()
        mock_hass.config_entries.flow.async_progress_by_handler = Mock(return_value=[])
        mock_hass.config_entries.async_entry_for_domain_unique_id = Mock(return_value=None)
        user_input = {
            SECTION_PRICING: {CONF_LITE_MODE: True},
            SECTION_CHEAPEST_WINDOW: {
                CONF_ENABLE_CHEAPEST_WINDOW: True,
                CONF_CHEAPEST_TIME_WINDOW_START: "20:00",
                CONF_CHEAPEST_TIME_WINDOW_END: "10:00",
                CONF_CHEAPEST_WINDOW_DURATION_HOURS: "12:00",
            },
            SECTION_EXPENSIVE_WINDOW: {
                CONF_ENABLE_EXPENSIVE_WINDOW: True,
                CONF_EXPENSIVE_TIME_WINDOW_START: "20:00",
                CONF_EXPENSIVE_TIME_WINDOW_END: "10:00",
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS: "12:00",
            },
            SECTION_SECOND_EXPENSIVE_WINDOW: {
                CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: True,
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START: "10:00",
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END: "06:00",
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS: "12:00",
            },
            SECTION_THRESHOLDS: {
                CONF_ENABLE_LOW_PRICE_THRESHOLD: False,
                CONF_LOW_PRICE_THRESHOLD: 0.0,
                CONF_ENABLE_HIGH_PRICE_THRESHOLD: False,
                CONF_HIGH_PRICE_THRESHOLD: 1000.0,
            },
        }
        with patch.object(flow, "_async_current_entries", return_value=[]):
            with patch.object(flow, "async_set_unique_id"):
                with patch.object(flow, "_abort_if_unique_id_configured"):
                    with patch.object(flow, "async_create_entry") as mock_create_entry:
                        mock_create_entry.return_value = {"type": "create_entry"}
                        result = await flow.async_step_user(user_input=user_input)
                        assert result.get("type") == "create_entry"

    @pytest.mark.asyncio
    async def test_config_flow_user_step_no_input(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        
        with patch.object(flow, "_async_current_entries", return_value=[]):
            result = await flow.async_step_user(user_input=None)
            
            assert result.get("type") == "form"
            assert result.get("step_id") == "user"

    @pytest.mark.asyncio
    async def test_config_flow_already_configured(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        
        mock_entry = Mock()
        mock_entry.domain = DOMAIN
        
        with patch.object(flow, "_async_current_entries") as mock_entries:
            mock_entries.return_value = [mock_entry]
            
            result = await flow.async_step_user(user_input=None)
            
            assert result.get("type") == "abort"
            assert result.get("reason") == "single_instance_allowed"


class TestConstants:

    def test_domain_constant(self):
        from custom_components.rce_pse.const import DOMAIN
        assert DOMAIN == "rce_pse"

    def test_sensor_prefix_constant(self):
        from custom_components.rce_pse.const import SENSOR_PREFIX
        assert SENSOR_PREFIX == "RCE PSE"

    def test_manufacturer_constant(self):
        from custom_components.rce_pse.const import MANUFACTURER
        assert MANUFACTURER == "Lewa-Reka"

    def test_api_base_and_endpoints(self):
        from custom_components.rce_pse.const import (
            PSE_API_BASE_URL,
            PSE_ENDPOINT_PDGSZ,
            PSE_ENDPOINT_RCE_PLN,
        )

        assert PSE_API_BASE_URL == "https://api.raporty.pse.pl/api"
        assert PSE_ENDPOINT_RCE_PLN == "rce-pln"
        assert PSE_ENDPOINT_PDGSZ == "pdgsz"
        assert f"{PSE_API_BASE_URL}/{PSE_ENDPOINT_RCE_PLN}" == (
            "https://api.raporty.pse.pl/api/rce-pln"
        )
        assert f"{PSE_API_BASE_URL}/{PSE_ENDPOINT_PDGSZ}" == (
            "https://api.raporty.pse.pl/api/pdgsz"
        )

    def test_update_interval_constant(self):
        from custom_components.rce_pse.const import API_UPDATE_INTERVAL
        assert API_UPDATE_INTERVAL.total_seconds() == 1800

    def test_api_parameters_constants(self):
        from custom_components.rce_pse.const import (
            PDGSZ_API_SELECT,
            PSE_API_PAGE_SIZE,
            RCE_PLN_API_SELECT,
        )

        assert RCE_PLN_API_SELECT == "dtime,period,rce_pln,business_date"
        assert PDGSZ_API_SELECT == "business_date,dtime,is_active,usage_fcst"
        assert PSE_API_PAGE_SIZE == 200