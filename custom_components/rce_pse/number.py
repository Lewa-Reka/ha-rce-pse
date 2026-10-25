from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_HIGH_PRICE_THRESHOLD,
    CONF_LOW_PRICE_THRESHOLD,
    DEFAULT_HIGH_PRICE_THRESHOLD,
    DEFAULT_LOW_PRICE_THRESHOLD,
    DOMAIN,
    THRESHOLD_MAX,
    THRESHOLD_MIN,
    THRESHOLD_STEP,
)
from .coordinator import RCEPSEDataUpdateCoordinator
from .options import (
    async_set_entry_option,
    get_entry_value,
    is_high_price_threshold_enabled,
    is_lite_mode,
    is_low_price_threshold_enabled,
)
from .shared_base import RCEBaseCommonEntity

_LOGGER = logging.getLogger(__name__)

THRESHOLD_NUMBER_ENTITIES = (
    (
        is_low_price_threshold_enabled,
        "low_price_threshold",
        CONF_LOW_PRICE_THRESHOLD,
        DEFAULT_LOW_PRICE_THRESHOLD,
    ),
    (
        is_high_price_threshold_enabled,
        "high_price_threshold",
        CONF_HIGH_PRICE_THRESHOLD,
        DEFAULT_HIGH_PRICE_THRESHOLD,
    ),
)


class RCEPriceThresholdNumberEntity(RCEBaseCommonEntity, NumberEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = THRESHOLD_MIN
    _attr_native_max_value = THRESHOLD_MAX
    _attr_native_step = THRESHOLD_STEP
    _attr_icon = "mdi:cash"

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
        unique_id: str,
        option_key: str,
        default: float,
    ) -> None:
        super().__init__(coordinator, unique_id)
        self.config_entry = config_entry
        self._option_key = option_key
        self._default = default
        self._attr_native_unit_of_measurement = self.native_price_unit()

    @property
    def available(self) -> bool:
        return True

    @property
    def native_value(self) -> float:
        return float(get_entry_value(self.config_entry, self._option_key, self._default))

    async def async_set_native_value(self, value: float) -> None:
        await async_set_entry_option(
            self.hass, self.config_entry, self._option_key, float(value)
        )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.debug("Setting up RCE PSE number entities for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[RCEPriceThresholdNumberEntity] = []

    if not is_lite_mode(config_entry):
        for is_enabled, unique_id, option_key, default in THRESHOLD_NUMBER_ENTITIES:
            if not is_enabled(config_entry):
                continue
            entities.append(
                RCEPriceThresholdNumberEntity(
                    coordinator,
                    config_entry,
                    unique_id,
                    option_key,
                    default,
                )
            )

    _LOGGER.debug("Adding %d RCE PSE number entities to Home Assistant", len(entities))
    async_add_entities(entities)
    _LOGGER.debug("RCE PSE number entities setup completed successfully")
