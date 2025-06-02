from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from custom_components.rce_pse.coordinator import RCEPSEDataUpdateCoordinator


@pytest.fixture
def mock_hass():
    hass = Mock(spec=HomeAssistant)
    hass.config = Mock()
    hass.config.time_zone = "Europe/Warsaw"
    hass.data = {}
    return hass


@pytest.fixture
def sample_api_response():
    now = dt_util.now()
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    
    return {
        "value": [
            {
                "dtime": f"{today} 00:00:00",
                "period": "00:00 - 01:00",
                "rce_pln": "350.00",
                "business_date": today,
                "publication_ts": f"{today}T23:00:00Z"
            },
            {
                "dtime": f"{today} 01:00:00",
                "period": "01:00 - 02:00",
                "rce_pln": "320.00",
                "business_date": today,
                "publication_ts": f"{today}T23:00:00Z"
            },
            {
                "dtime": f"{today} 02:00:00",
                "period": "02:00 - 03:00",
                "rce_pln": "300.00",
                "business_date": today,
                "publication_ts": f"{today}T23:00:00Z"
            },
            {
                "dtime": f"{today} 12:00:00",
                "period": "12:00 - 13:00",
                "rce_pln": "450.00",
                "business_date": today,
                "publication_ts": f"{today}T23:00:00Z"
            },
            {
                "dtime": f"{tomorrow} 00:00:00",
                "period": "00:00 - 01:00",
                "rce_pln": "330.00",
                "business_date": tomorrow,
                "publication_ts": f"{today}T23:00:00Z"
            },
            {
                "dtime": f"{tomorrow} 01:00:00",
                "period": "01:00 - 02:00",
                "rce_pln": "310.00",
                "business_date": tomorrow,
                "publication_ts": f"{today}T23:00:00Z"
            },
            {
                "dtime": f"{tomorrow} 12:00:00",
                "period": "12:00 - 13:00",
                "rce_pln": "420.00",
                "business_date": tomorrow,
                "publication_ts": f"{today}T23:00:00Z"
            }
        ]
    }


@pytest.fixture
def coordinator_data(sample_api_response):
    return {
        "raw_data": sample_api_response["value"],
        "last_update": dt_util.now().isoformat(),
    }


@pytest.fixture
def mock_coordinator(mock_hass, coordinator_data):
    coordinator = Mock(spec=RCEPSEDataUpdateCoordinator)
    coordinator.hass = mock_hass
    coordinator.data = coordinator_data
    coordinator.last_update_success = True
    coordinator.last_update_success_time = dt_util.now()
    coordinator.async_add_listener = Mock()
    coordinator.async_remove_listener = Mock()
    return coordinator


@pytest.fixture
def mock_aiohttp_session():
    session = AsyncMock()
    response = AsyncMock()
    response.status = 200
    response.json = AsyncMock()
    
    async def async_context_manager(*args, **kwargs):
        return response
        
    session.get.return_value.__aenter__ = AsyncMock(return_value=response)
    session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    
    session.close = AsyncMock()
    
    return session, response 