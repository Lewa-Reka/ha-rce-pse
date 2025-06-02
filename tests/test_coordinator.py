from __future__ import annotations

from unittest.mock import patch, AsyncMock

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.rce_pse.coordinator import RCEPSEDataUpdateCoordinator


class TestRCEPSEDataUpdateCoordinator:

    @pytest.mark.asyncio
    async def test_coordinator_initialization(self, mock_hass):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        
        assert coordinator.hass == mock_hass
        assert coordinator.name == "rce_pse"
        assert coordinator.update_interval.total_seconds() == 1800
        assert coordinator.session is None

    @pytest.mark.asyncio
    async def test_successful_data_fetch(self, mock_hass, sample_api_response):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        
        with patch.object(coordinator, '_fetch_data') as mock_fetch:
            expected_data = {
                "raw_data": sample_api_response["value"],
                "last_update": "2025-05-29T12:00:00+00:00"
            }
            mock_fetch.return_value = expected_data
            
            result = await coordinator._async_update_data()
            
            assert result is not None
            assert "raw_data" in result
            assert "last_update" in result
            assert len(result["raw_data"]) == 7
            assert result["raw_data"][0]["rce_pln"] == "350.00"

    @pytest.mark.asyncio
    async def test_data_fetch_creates_session_if_none(self, mock_hass, sample_api_response):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        assert coordinator.session is None
        
        with patch("custom_components.rce_pse.coordinator.aiohttp.ClientSession") as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value = mock_session
            
            with patch.object(coordinator, '_fetch_data') as mock_fetch:
                expected_data = {
                    "raw_data": sample_api_response["value"],
                    "last_update": "2025-05-29T12:00:00+00:00"
                }
                mock_fetch.return_value = expected_data
                
                result = await coordinator._async_update_data()
                
                mock_session_class.assert_called_once()
                assert coordinator.session == mock_session
                assert result["raw_data"] == sample_api_response["value"]

    @pytest.mark.asyncio
    async def test_api_request_behavior(self, mock_hass, sample_api_response):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        
        with patch.object(coordinator, 'session') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=sample_api_response)
            
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await coordinator._fetch_data()
            
            mock_session.get.assert_called_once()
            call_args = mock_session.get.call_args
            
            assert "https://v2.api.raporty.pse.pl/api/rce-pln" in call_args[0]
            assert "params" in call_args[1]
            assert "headers" in call_args[1]
            
            params = call_args[1]["params"]
            assert "$select" in params
            assert "$filter" in params
            assert "$first" in params
            assert params["$first"] == 200

    @pytest.mark.asyncio
    async def test_fetch_data_method(self, mock_hass, sample_api_response):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        
        with patch.object(coordinator, 'session') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=sample_api_response)
            
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await coordinator._fetch_data()
            
            assert result["raw_data"] == sample_api_response["value"]
            assert "last_update" in result
            assert len(result["raw_data"]) == 7

    @pytest.mark.asyncio
    async def test_successful_close_session(self, mock_hass):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        
        await coordinator.async_close()
        
        mock_session = AsyncMock()
        coordinator.session = mock_session
        
        await coordinator.async_close()
        mock_session.close.assert_called_once()

    @pytest.mark.asyncio 
    async def test_data_processing_with_valid_response(self, mock_hass, sample_api_response):
        coordinator = RCEPSEDataUpdateCoordinator(mock_hass)
        
        with patch.object(coordinator, '_fetch_data') as mock_fetch:
            expected_data = {
                "raw_data": sample_api_response["value"],
                "last_update": "2025-05-29T12:00:00+00:00"
            }
            mock_fetch.return_value = expected_data
            
            result = await coordinator._async_update_data()
            
            assert isinstance(result, dict)
            assert isinstance(result["raw_data"], list)
            assert len(result["raw_data"]) > 0
            
            first_record = result["raw_data"][0]
            assert "dtime" in first_record
            assert "period" in first_record
            assert "rce_pln" in first_record
            assert "business_date" in first_record 