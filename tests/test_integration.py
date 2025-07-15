from __future__ import annotations

from unittest.mock import Mock, patch, AsyncMock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.rce_pse import async_setup_entry, async_unload_entry
from custom_components.rce_pse.config_flow import RCEConfigFlow
from custom_components.rce_pse.const import DOMAIN


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
            mock_coordinator_class.assert_called_once_with(mock_hass)
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


class TestRCEPSEConfigFlow:

    @pytest.mark.asyncio
    async def test_config_flow_init(self):
        flow = RCEConfigFlow()
        
        assert flow.VERSION == 1
        assert flow.MINOR_VERSION == 1

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
                
                assert result["type"] == "create_entry"
                mock_create_entry.assert_called_once_with(title="RCE PSE", data={})

    @pytest.mark.asyncio
    async def test_config_flow_user_step_no_input(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        
        with patch.object(flow, "_async_current_entries", return_value=[]):
            result = await flow.async_step_user(user_input=None)
            
            assert result["type"] == "form"
            assert result["step_id"] == "user"

    @pytest.mark.asyncio
    async def test_config_flow_already_configured(self, mock_hass):
        flow = RCEConfigFlow()
        flow.hass = mock_hass
        
        mock_entry = Mock()
        mock_entry.domain = DOMAIN
        
        with patch.object(flow, "_async_current_entries") as mock_entries:
            mock_entries.return_value = [mock_entry]
            
            result = await flow.async_step_user(user_input=None)
            
            assert result["type"] == "abort"
            assert result["reason"] == "single_instance_allowed"


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

    def test_api_url_constant(self):
        from custom_components.rce_pse.const import PSE_API_URL
        assert PSE_API_URL == "https://api.raporty.pse.pl/api/rce-pln"

    def test_update_interval_constant(self):
        from custom_components.rce_pse.const import API_UPDATE_INTERVAL
        assert API_UPDATE_INTERVAL.total_seconds() == 1800

    def test_api_parameters_constants(self):
        from custom_components.rce_pse.const import API_SELECT, API_FIRST
        
        assert API_SELECT == "dtime,period,rce_pln,business_date,publication_ts"
        assert API_FIRST == 200 