from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensors import (
    RCETodayMainSensor,
    RCETodayKwhPriceSensor,
    RCENextHourPriceSensor,
    RCENext2HoursPriceSensor,
    RCENext3HoursPriceSensor,
    RCEPreviousHourPriceSensor,
    RCETodayAvgPriceSensor,
    RCETodayMaxPriceSensor,
    RCETodayMinPriceSensor,
    RCETodayMaxPriceHourStartSensor,
    RCETodayMaxPriceHourEndSensor,
    RCETodayMinPriceHourStartSensor,
    RCETodayMinPriceHourEndSensor,
    RCETodayMinPriceRangeSensor,
    RCETodayMaxPriceRangeSensor,
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
    RCETomorrowMinPriceRangeSensor,
    RCETomorrowMaxPriceRangeSensor,
    RCETomorrowMedianPriceSensor,
    RCETomorrowTodayAvgComparisonSensor,
)
from .sensors.custom_windows import (
    RCETodayCheapestWindowStartSensor,
    RCETodayCheapestWindowEndSensor,
    RCETodayCheapestWindowRangeSensor,
    RCETodayExpensiveWindowStartSensor,
    RCETodayExpensiveWindowEndSensor,
    RCETodayExpensiveWindowRangeSensor,
    RCETomorrowCheapestWindowStartSensor,
    RCETomorrowCheapestWindowEndSensor,
    RCETomorrowCheapestWindowRangeSensor,
    RCETomorrowExpensiveWindowStartSensor,
    RCETomorrowExpensiveWindowEndSensor,
    RCETomorrowExpensiveWindowRangeSensor,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.debug("Setting up RCE PSE sensors for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    sensors = [
        RCETodayMainSensor(coordinator),
        RCETodayKwhPriceSensor(coordinator),
        RCENextHourPriceSensor(coordinator),
        RCENext2HoursPriceSensor(coordinator),
        RCENext3HoursPriceSensor(coordinator),
        RCEPreviousHourPriceSensor(coordinator),
        RCETodayAvgPriceSensor(coordinator),
        RCETodayMaxPriceSensor(coordinator),
        RCETodayMinPriceSensor(coordinator),
        RCETodayMaxPriceHourStartSensor(coordinator),
        RCETodayMaxPriceHourEndSensor(coordinator),
        RCETodayMinPriceHourStartSensor(coordinator),
        RCETodayMinPriceHourEndSensor(coordinator),
        RCETodayMinPriceRangeSensor(coordinator),
        RCETodayMaxPriceRangeSensor(coordinator),
        RCETodayMedianPriceSensor(coordinator),
        RCETodayCurrentVsAverageSensor(coordinator),
        RCETomorrowMainSensor(coordinator),
        RCETomorrowAvgPriceSensor(coordinator),
        RCETomorrowMaxPriceSensor(coordinator),
        RCETomorrowMinPriceSensor(coordinator),
        RCETomorrowMaxPriceHourStartSensor(coordinator),
        RCETomorrowMaxPriceHourEndSensor(coordinator),
        RCETomorrowMinPriceHourStartSensor(coordinator),
        RCETomorrowMinPriceHourEndSensor(coordinator),
        RCETomorrowMinPriceRangeSensor(coordinator),
        RCETomorrowMaxPriceRangeSensor(coordinator),
        RCETomorrowMedianPriceSensor(coordinator),
        RCETomorrowTodayAvgComparisonSensor(coordinator),
        RCETodayCheapestWindowStartSensor(coordinator, config_entry),
        RCETodayCheapestWindowEndSensor(coordinator, config_entry),
        RCETodayCheapestWindowRangeSensor(coordinator, config_entry),
        RCETodayExpensiveWindowStartSensor(coordinator, config_entry),
        RCETodayExpensiveWindowEndSensor(coordinator, config_entry),
        RCETodayExpensiveWindowRangeSensor(coordinator, config_entry),
        RCETomorrowCheapestWindowStartSensor(coordinator, config_entry),
        RCETomorrowCheapestWindowEndSensor(coordinator, config_entry),
        RCETomorrowCheapestWindowRangeSensor(coordinator, config_entry),
        RCETomorrowExpensiveWindowStartSensor(coordinator, config_entry),
        RCETomorrowExpensiveWindowEndSensor(coordinator, config_entry),
        RCETomorrowExpensiveWindowRangeSensor(coordinator, config_entry),
    ]
    
    _LOGGER.debug("Adding %d RCE PSE sensors to Home Assistant", len(sensors))
    async_add_entities(sensors)
    _LOGGER.debug("RCE PSE sensors setup completed successfully") 