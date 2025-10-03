from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

import aiohttp
import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import API_FIRST, API_SELECT, API_UPDATE_INTERVAL, DOMAIN, PSE_API_URL, CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES

_LOGGER = logging.getLogger(__name__)


class RCEPSEDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, config_entry=None) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=API_UPDATE_INTERVAL,
        )
        self.session = None
        self._last_api_fetch = None
        self.config_entry = config_entry

    def _get_config_value(self, key: str, default: any) -> any:
        if not self.config_entry:
            return default
            
        if self.config_entry.options and key in self.config_entry.options:
            return self.config_entry.options[key]
        elif self.config_entry.data and key in self.config_entry.data:
            return self.config_entry.data.get(key, default)
        
        return default

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
                
                raw_data = data["value"]
                
                use_hourly_prices = self._get_config_value(CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES)
                
                if use_hourly_prices:
                    _LOGGER.debug("Hourly prices option enabled, calculating hourly averages")
                    processed_data = self._calculate_hourly_averages(raw_data)
                else:
                    _LOGGER.debug("Hourly prices option disabled, using original 15-minute data")
                    processed_data = self._add_neg_to_zero_key(raw_data)
                
                return {
                    "raw_data": processed_data,
                    "last_update": dt_util.now().isoformat(),
                }
                
        except aiohttp.ClientError as exception:
            _LOGGER.error("HTTP client error fetching PSE data: %s", exception)
            raise UpdateFailed(f"Error fetching data: {exception}") from exception

    def _calculate_hourly_averages(self, raw_data: list[dict]) -> list[dict]:
        if not raw_data:
            return raw_data
        
        hourly_groups = defaultdict(list)
        
        for record in raw_data:
            try:
                dtime = datetime.strptime(record["dtime"], "%Y-%m-%d %H:%M:%S")
                period_start = dtime - timedelta(minutes=15)
                date_hour_key = f"{period_start.strftime('%Y-%m-%d')}_{period_start.hour:02d}"
                hourly_groups[date_hour_key].append(record)
            except (ValueError, KeyError) as e:
                _LOGGER.warning("Failed to parse record dtime: %s, error: %s", record.get("dtime"), e)
                continue
        
        processed_data = []
        
        for date_hour_key, records in hourly_groups.items():
            if not records:
                continue
                
            prices = []
            for record in records:
                try:
                    price = float(record["rce_pln"])
                    prices.append(price)
                except (ValueError, KeyError) as e:
                    _LOGGER.warning("Failed to parse price from record: %s, error: %s", record.get("rce_pln"), e)
                    continue
            
            if not prices:
                continue
                
            average_price = sum(prices) / len(prices)
            
            prices_neg_to_zero = [max(0, price) for price in prices]
            average_price_neg_to_zero = sum(prices_neg_to_zero) / len(prices_neg_to_zero)
            
            _LOGGER.debug("Calculated hourly average for %s: %.2f PLN (from %d records)", 
                         date_hour_key, average_price, len(prices))
            _LOGGER.debug("Calculated hourly average (neg to zero) for %s: %.2f PLN", 
                         date_hour_key, average_price_neg_to_zero)
            
            for record in records:
                try:
                    new_record = record.copy()
                    new_record["rce_pln"] = f"{average_price:.2f}"
                    new_record["rce_pln_neg_to_zero"] = f"{average_price_neg_to_zero:.2f}"
                    processed_data.append(new_record)
                except (ValueError, KeyError) as e:
                    _LOGGER.warning("Failed to process record: %s, error: %s", record, e)
                    continue
        
        _LOGGER.debug("Processed %d records with hourly averages (original: %d)", 
                     len(processed_data), len(raw_data))
        
        return processed_data

    def _add_neg_to_zero_key(self, raw_data: list[dict]) -> list[dict]:
        if not raw_data:
            return raw_data
        
        processed_data = []
        
        for record in raw_data:
            try:
                new_record = record.copy()
                price = float(record["rce_pln"])
                neg_to_zero_price = max(0, price)
                new_record["rce_pln_neg_to_zero"] = f"{neg_to_zero_price:.2f}"
                processed_data.append(new_record)
            except (ValueError, KeyError) as e:
                _LOGGER.warning("Failed to process record for neg_to_zero: %s, error: %s", record, e)
                processed_data.append(record)
        
        _LOGGER.debug("Added rce_pln_neg_to_zero key to %d records", len(processed_data))
        
        return processed_data

    async def async_close(self) -> None:
        _LOGGER.debug("Closing PSE API session")
        if self.session:
            await self.session.close() 