from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .options import (
    is_cheapest_window_enabled,
    is_expensive_window_enabled,
    is_high_price_threshold_enabled,
    is_lite_mode,
    is_low_price_threshold_enabled,
    is_second_expensive_window_enabled,
)
from .binary_sensors import (
    RCETodayMinPriceWindowBinarySensor,
    RCETodayMaxPriceWindowBinarySensor,
    RCETodayCheapestWindowBinarySensor,
    RCETodayExpensiveWindowBinarySensor,
    RCETodaySecondExpensiveWindowBinarySensor,
    RCELowPriceThresholdWindowActiveBinarySensor,
    RCEHighPriceThresholdWindowActiveBinarySensor,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.debug("Setting up RCE PSE binary sensors for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    binary_sensors = []

    if not is_lite_mode(config_entry):
        binary_sensors.extend(
            [
                RCETodayMinPriceWindowBinarySensor(coordinator),
                RCETodayMaxPriceWindowBinarySensor(coordinator),
            ]
        )

        if is_cheapest_window_enabled(config_entry):
            binary_sensors.append(RCETodayCheapestWindowBinarySensor(coordinator, config_entry))

        if is_expensive_window_enabled(config_entry):
            binary_sensors.append(RCETodayExpensiveWindowBinarySensor(coordinator, config_entry))

        if is_second_expensive_window_enabled(config_entry):
            binary_sensors.append(
                RCETodaySecondExpensiveWindowBinarySensor(coordinator, config_entry)
            )

        if is_low_price_threshold_enabled(config_entry):
            binary_sensors.append(
                RCELowPriceThresholdWindowActiveBinarySensor(coordinator, config_entry)
            )

        if is_high_price_threshold_enabled(config_entry):
            binary_sensors.append(
                RCEHighPriceThresholdWindowActiveBinarySensor(coordinator, config_entry)
            )
    
    _LOGGER.debug("Adding %d RCE PSE binary sensors to Home Assistant", len(binary_sensors))
    async_add_entities(binary_sensors)
    _LOGGER.debug("RCE PSE binary sensors setup completed successfully") 