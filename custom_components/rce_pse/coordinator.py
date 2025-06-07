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

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=API_UPDATE_INTERVAL,
        )
        self.session = None
        self._last_api_fetch = None

    async def _async_update_data(self) -> dict[str, Any]:
        now = dt_util.now()
        
        if (self._last_api_fetch and 
            self.data and 
            now - self._last_api_fetch < API_UPDATE_INTERVAL):
            time_since_fetch = now - self._last_api_fetch
            _LOGGER.debug("Using cached data - last API fetch was %s ago (max interval: %s)", 
                         time_since_fetch, API_UPDATE_INTERVAL)
            return self.data
        
        _LOGGER.debug("Fetching fresh data from PSE API - last fetch: %s", self._last_api_fetch)
        
        if self.session is None:
            self.session = aiohttp.ClientSession()
            
        try:
            async with async_timeout.timeout(30):
                data = await self._fetch_data()
                self._last_api_fetch = now
                _LOGGER.debug("Successfully fetched fresh data from PSE API, records count: %d", 
                            len(data.get("raw_data", [])))
                return data
        except asyncio.TimeoutError as exception:
            self._last_api_fetch = now
            _LOGGER.error("Timeout communicating with PSE API: %s", exception)
            if self.data:
                _LOGGER.warning("Using existing data due to API timeout")
                return self.data
            raise UpdateFailed(f"Timeout communicating with API: {exception}") from exception
        except Exception as exception:
            self._last_api_fetch = now
            _LOGGER.error("Error communicating with PSE API: %s", exception)
            if self.data:
                _LOGGER.warning("Using existing data due to API error")
                return self.data
            raise UpdateFailed(f"Error communicating with API: {exception}") from exception

    async def _fetch_data(self) -> dict[str, Any]:
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
        _LOGGER.debug("Closing PSE API session")
        if self.session:
            await self.session.close() 