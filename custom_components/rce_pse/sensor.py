"""Sensor platform for RCE PSE integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import RCEPSEDataUpdateCoordinator
from .sensors import (
    RCETodayMainSensor,
    RCENextHourPriceSensor,
    RCENext2HoursPriceSensor,
    RCENext3HoursPriceSensor,
    RCETodayAvgPriceSensor,
    RCETodayMaxPriceSensor,
    RCETodayMinPriceSensor,
    RCETodayMaxPriceHourStartSensor,
    RCETodayMaxPriceHourEndSensor,
    RCETodayMinPriceHourStartSensor,
    RCETodayMinPriceHourEndSensor,
    RCETodayMedianPriceSensor,
    RCETodayCurrentVsAverageSensor,
    RCETomorrowMainSensor,
    RCETomorrowAvgPriceSensor,
    RCETomorrowMaxPriceSensor,
    RCETomorrowMinPriceSensor,
    RCETomorrowMaxPriceHourStartSensor,
    RCETomorrowMaxPriceHourEndSensor,
    RCETomorrowMinPriceHourStartSensor,
    RCETomorrowMinPriceHourEndSensor,
    RCETomorrowMedianPriceSensor,
    RCETomorrowTodayAvgComparisonSensor,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.debug("Setting up RCE PSE sensors for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    sensors = [
        RCETodayMainSensor(coordinator),
        RCENextHourPriceSensor(coordinator),
        RCENext2HoursPriceSensor(coordinator),
        RCENext3HoursPriceSensor(coordinator),
        RCETodayAvgPriceSensor(coordinator),
        RCETodayMaxPriceSensor(coordinator),
        RCETodayMinPriceSensor(coordinator),
        RCETodayMaxPriceHourStartSensor(coordinator),
        RCETodayMaxPriceHourEndSensor(coordinator),
        RCETodayMinPriceHourStartSensor(coordinator),
        RCETodayMinPriceHourEndSensor(coordinator),
        RCETodayMedianPriceSensor(coordinator),
        RCETodayCurrentVsAverageSensor(coordinator),
        # Tomorrow sensors (available after 14:00 CET)
        RCETomorrowMainSensor(coordinator),
        RCETomorrowAvgPriceSensor(coordinator),
        RCETomorrowMaxPriceSensor(coordinator),
        RCETomorrowMinPriceSensor(coordinator),
        RCETomorrowMaxPriceHourStartSensor(coordinator),
        RCETomorrowMaxPriceHourEndSensor(coordinator),
        RCETomorrowMinPriceHourStartSensor(coordinator),
        RCETomorrowMinPriceHourEndSensor(coordinator),
        RCETomorrowMedianPriceSensor(coordinator),
        RCETomorrowTodayAvgComparisonSensor(coordinator),
    ]
    
    _LOGGER.debug("Adding %d RCE PSE sensors to Home Assistant", len(sensors))
    async_add_entities(sensors)
    _LOGGER.debug("RCE PSE sensors setup completed successfully") 