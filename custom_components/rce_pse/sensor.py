from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensors.peak_hours import preload_peak_hours_translation_cache
from .sensors import (
    RCETodayPeakHoursSensor,
    RCETomorrowPeakHoursSensor,
    RCETodayMainSensor,
    RCETodayProsumerSellingPriceSensor,
    RCENextPeriodPriceSensor,
    RCEPreviousPeriodPriceSensor,
    RCETodayAvgPriceSensor,
    RCETodayMaxPriceSensor,
    RCETodayMinPriceSensor,
    RCETodayMaxPriceHourStartTimestampSensor,
    RCETodayMaxPriceHourEndTimestampSensor,
    RCETodayMinPriceHourStartTimestampSensor,
    RCETodayMinPriceHourEndTimestampSensor,
    RCETodayMedianPriceSensor,
    RCETodayCurrentVsAverageSensor,
    RCETomorrowMainSensor,
    RCETomorrowAvgPriceSensor,
    RCETomorrowMaxPriceSensor,
    RCETomorrowMinPriceSensor,
    RCETomorrowMaxPriceHourStartTimestampSensor,
    RCETomorrowMaxPriceHourEndTimestampSensor,
    RCETomorrowMinPriceHourStartTimestampSensor,
    RCETomorrowMinPriceHourEndTimestampSensor,
    RCETomorrowMedianPriceSensor,
    RCETomorrowTodayAvgComparisonSensor,
)
from .sensors.custom_windows import (
    RCETodayCheapestWindowStartTimestampSensor,
    RCETodayCheapestWindowEndTimestampSensor,
    RCETodayExpensiveWindowStartTimestampSensor,
    RCETodayExpensiveWindowEndTimestampSensor,
    RCETomorrowCheapestWindowStartTimestampSensor,
    RCETomorrowCheapestWindowEndTimestampSensor,
    RCETomorrowExpensiveWindowStartTimestampSensor,
    RCETomorrowExpensiveWindowEndTimestampSensor,
    RCETodaySecondExpensiveWindowStartSensor,
    RCETodaySecondExpensiveWindowEndSensor,
    RCETomorrowSecondExpensiveWindowStartSensor,
    RCETomorrowSecondExpensiveWindowEndSensor,
)
from .sensors.window_avg_price import (
    RCETodayCheapestWindowAvgPriceSensor,
    RCETodayExpensiveWindowAvgPriceSensor,
    RCETodaySecondExpensiveWindowAvgPriceSensor,
    RCETomorrowCheapestWindowAvgPriceSensor,
    RCETomorrowExpensiveWindowAvgPriceSensor,
    RCETomorrowSecondExpensiveWindowAvgPriceSensor,
)
from .sensors.price_threshold_windows import (
    RCEHighPriceThresholdWindowEndSensor,
    RCEHighPriceThresholdWindowStartSensor,
    RCELowPriceThresholdWindowEndSensor,
    RCELowPriceThresholdWindowStartSensor,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.debug("Setting up RCE PSE sensors for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    await hass.async_add_executor_job(preload_peak_hours_translation_cache)

    sensors = [
        RCETodayMainSensor(coordinator),
        RCETodayProsumerSellingPriceSensor(coordinator),
        RCENextPeriodPriceSensor(coordinator),
        RCEPreviousPeriodPriceSensor(coordinator),
        RCETodayAvgPriceSensor(coordinator),
        RCETodayMaxPriceSensor(coordinator),
        RCETodayMinPriceSensor(coordinator),
        RCETodayMaxPriceHourStartTimestampSensor(coordinator),
        RCETodayMaxPriceHourEndTimestampSensor(coordinator),
        RCETodayMinPriceHourStartTimestampSensor(coordinator),
        RCETodayMinPriceHourEndTimestampSensor(coordinator),
        RCETodayMedianPriceSensor(coordinator),
        RCETodayCurrentVsAverageSensor(coordinator),
        RCETomorrowMainSensor(coordinator),
        RCETomorrowAvgPriceSensor(coordinator),
        RCETomorrowMaxPriceSensor(coordinator),
        RCETomorrowMinPriceSensor(coordinator),
        RCETomorrowMaxPriceHourStartTimestampSensor(coordinator),
        RCETomorrowMaxPriceHourEndTimestampSensor(coordinator),
        RCETomorrowMinPriceHourStartTimestampSensor(coordinator),
        RCETomorrowMinPriceHourEndTimestampSensor(coordinator),
        RCETomorrowMedianPriceSensor(coordinator),
        RCETomorrowTodayAvgComparisonSensor(coordinator),
        RCETodayCheapestWindowStartTimestampSensor(coordinator, config_entry),
        RCETodayCheapestWindowEndTimestampSensor(coordinator, config_entry),
        RCETodayExpensiveWindowStartTimestampSensor(coordinator, config_entry),
        RCETodayExpensiveWindowEndTimestampSensor(coordinator, config_entry),
        RCETomorrowCheapestWindowStartTimestampSensor(coordinator, config_entry),
        RCETomorrowCheapestWindowEndTimestampSensor(coordinator, config_entry),
        RCETomorrowExpensiveWindowStartTimestampSensor(coordinator, config_entry),
        RCETomorrowExpensiveWindowEndTimestampSensor(coordinator, config_entry),
        RCETodaySecondExpensiveWindowStartSensor(coordinator, config_entry),
        RCETodaySecondExpensiveWindowEndSensor(coordinator, config_entry),
        RCETomorrowSecondExpensiveWindowStartSensor(coordinator, config_entry),
        RCETomorrowSecondExpensiveWindowEndSensor(coordinator, config_entry),
        RCETodayCheapestWindowAvgPriceSensor(coordinator, config_entry),
        RCETodayExpensiveWindowAvgPriceSensor(coordinator, config_entry),
        RCETodaySecondExpensiveWindowAvgPriceSensor(coordinator, config_entry),
        RCETomorrowCheapestWindowAvgPriceSensor(coordinator, config_entry),
        RCETomorrowExpensiveWindowAvgPriceSensor(coordinator, config_entry),
        RCETomorrowSecondExpensiveWindowAvgPriceSensor(coordinator, config_entry),
        RCETodayPeakHoursSensor(coordinator),
        RCETomorrowPeakHoursSensor(coordinator),
        RCELowPriceThresholdWindowStartSensor(coordinator, config_entry),
        RCELowPriceThresholdWindowEndSensor(coordinator, config_entry),
        RCEHighPriceThresholdWindowStartSensor(coordinator, config_entry),
        RCEHighPriceThresholdWindowEndSensor(coordinator, config_entry),
    ]
    
    _LOGGER.debug("Adding %d RCE PSE sensors to Home Assistant", len(sensors))
    async_add_entities(sensors)
    _LOGGER.debug("RCE PSE sensors setup completed successfully") 