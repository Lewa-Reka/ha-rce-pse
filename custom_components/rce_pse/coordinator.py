"""Data update coordinator for RCE PSE integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import API_FIRST, API_SELECT, API_UPDATE_INTERVAL, DOMAIN, PSE_API_URL

_LOGGER = logging.getLogger(__name__)


class RCEPSEDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the PSE API."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=API_UPDATE_INTERVAL,
        )
        self.session = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        _LOGGER.debug("Starting data update from PSE API")
        
        # Create session if it doesn't exist
        if self.session is None:
            self.session = aiohttp.ClientSession()
            
        try:
            async with async_timeout.timeout(30):
                data = await self._fetch_data()
                _LOGGER.debug("Successfully fetched data from PSE API, records count: %d", 
                            len(data.get("raw_data", [])))
                return data
        except asyncio.TimeoutError as exception:
            _LOGGER.error("Timeout communicating with PSE API: %s", exception)
            raise UpdateFailed(f"Timeout communicating with API: {exception}") from exception
        except Exception as exception:
            _LOGGER.error("Error communicating with PSE API: %s", exception)
            raise UpdateFailed(f"Error communicating with API: {exception}") from exception

    async def _fetch_data(self) -> dict[str, Any]:
        """Fetch data from PSE API."""
        today = dt_util.now().strftime("%Y-%m-%d")
        _LOGGER.debug("Fetching PSE data for business_date >= %s", today)
        
        params = {
            "$select": API_SELECT,
            "$filter": f"business_date ge '{today}'",
            "$first": API_FIRST,
        }
        
        headers = {
            "Accept": "application/json",
        }

        _LOGGER.debug("PSE API request URL: %s, params: %s", PSE_API_URL, params)

        try:
            async with self.session.get(
                PSE_API_URL, params=params, headers=headers
            ) as response:
                _LOGGER.debug("PSE API response status: %d", response.status)
                
                if response.status != 200:
                    _LOGGER.error("PSE API returned error status: %d", response.status)
                    raise UpdateFailed(f"API returned status {response.status}")
                
                data = await response.json()
                
                if "value" not in data:
                    _LOGGER.error("PSE API response missing 'value' field")
                    raise UpdateFailed("Invalid API response format")
                
                record_count = len(data["value"])
                _LOGGER.debug("PSE API returned %d records", record_count)
                
                if record_count == 0:
                    _LOGGER.warning("PSE API returned no data records")
                
                return {
                    "raw_data": data["value"],
                    "last_update": dt_util.now().isoformat(),
                }
                
        except aiohttp.ClientError as exception:
            _LOGGER.error("HTTP client error fetching PSE data: %s", exception)
            raise UpdateFailed(f"Error fetching data: {exception}") from exception

    async def async_close(self) -> None:
        """Close the session."""
        _LOGGER.debug("Closing PSE API session")
        if self.session:
            await self.session.close() 