from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .binary_sensors import (
    RCETodayMinPriceWindowBinarySensor,
    RCETodayMaxPriceWindowBinarySensor,
    RCETodayCheapestWindowBinarySensor,
    RCETodayExpensiveWindowBinarySensor,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.debug("Setting up RCE PSE binary sensors for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    binary_sensors = [
        RCETodayMinPriceWindowBinarySensor(coordinator),
        RCETodayMaxPriceWindowBinarySensor(coordinator),
        RCETodayCheapestWindowBinarySensor(coordinator, config_entry),
        RCETodayExpensiveWindowBinarySensor(coordinator, config_entry),
    ]
    
    _LOGGER.debug("Adding %d RCE PSE binary sensors to Home Assistant", len(binary_sensors))
    async_add_entities(binary_sensors)
    _LOGGER.debug("RCE PSE binary sensors setup completed successfully") 