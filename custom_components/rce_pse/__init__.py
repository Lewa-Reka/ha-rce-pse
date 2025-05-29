"""The RCE PSE integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import RCEPSEDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the RCE PSE component."""
    _LOGGER.debug("Setting up RCE PSE integration")
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.debug("RCE PSE integration setup completed")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RCE PSE from a config entry."""
    _LOGGER.debug("Setting up RCE PSE config entry: %s", entry.entry_id)
    hass.data.setdefault(DOMAIN, {})
    
    coordinator = RCEPSEDataUpdateCoordinator(hass)
    _LOGGER.debug("Created data coordinator for RCE PSE")
    
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug("Completed first data refresh for RCE PSE")
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("RCE PSE config entry setup completed successfully")
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading RCE PSE config entry: %s", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_close()
        _LOGGER.debug("RCE PSE config entry unloaded successfully")
    else:
        _LOGGER.warning("Failed to unload RCE PSE config entry: %s", entry.entry_id)
    
    return unload_ok 