from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_WINDOW_DURATION_HOURS,
    DOMAIN,
)
from .coordinator import RCEPSEDataUpdateCoordinator
from .options import (
    async_set_entry_option,
    get_entry_value,
    is_cheapest_window_enabled,
    is_expensive_window_enabled,
    is_lite_mode,
    is_second_expensive_window_enabled,
)
from .shared_base import RCEBaseCommonEntity
from .time_window import (
    duration_options,
    end_time_options,
    normalize_hhmm,
    start_time_options,
)

_LOGGER = logging.getLogger(__name__)

WINDOW_SELECT_GROUPS = (
    (
        is_cheapest_window_enabled,
        (
            (
                "cheapest_time_window_start",
                CONF_CHEAPEST_TIME_WINDOW_START,
                start_time_options,
                DEFAULT_TIME_WINDOW_START,
                "mdi:clock-start",
            ),
            (
                "cheapest_time_window_end",
                CONF_CHEAPEST_TIME_WINDOW_END,
                end_time_options,
                DEFAULT_TIME_WINDOW_END,
                "mdi:clock-end",
            ),
            (
                "cheapest_window_duration_hours",
                CONF_CHEAPEST_WINDOW_DURATION_HOURS,
                duration_options,
                DEFAULT_WINDOW_DURATION_HOURS,
                "mdi:timer-outline",
            ),
        ),
    ),
    (
        is_expensive_window_enabled,
        (
            (
                "expensive_time_window_start",
                CONF_EXPENSIVE_TIME_WINDOW_START,
                start_time_options,
                DEFAULT_TIME_WINDOW_START,
                "mdi:clock-start",
            ),
            (
                "expensive_time_window_end",
                CONF_EXPENSIVE_TIME_WINDOW_END,
                end_time_options,
                DEFAULT_TIME_WINDOW_END,
                "mdi:clock-end",
            ),
            (
                "expensive_window_duration_hours",
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
                duration_options,
                DEFAULT_WINDOW_DURATION_HOURS,
                "mdi:timer-outline",
            ),
        ),
    ),
    (
        is_second_expensive_window_enabled,
        (
            (
                "second_expensive_time_window_start",
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                start_time_options,
                DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
                "mdi:clock-start",
            ),
            (
                "second_expensive_time_window_end",
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                end_time_options,
                DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
                "mdi:clock-end",
            ),
            (
                "second_expensive_window_duration_hours",
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                duration_options,
                DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                "mdi:timer-outline",
            ),
        ),
    ),
)


class RCEWindowTimeSelectEntity(RCEBaseCommonEntity, SelectEntity):
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
        unique_id: str,
        option_key: str,
        options: list[str],
        default: str,
        icon: str,
    ) -> None:
        super().__init__(coordinator, unique_id)
        self.config_entry = config_entry
        self._option_key = option_key
        self._default = default
        self._attr_options = options
        self._attr_icon = icon

    @property
    def available(self) -> bool:
        return True

    @property
    def current_option(self) -> str | None:
        value = get_entry_value(self.config_entry, self._option_key, self._default)
        return normalize_hhmm(str(value))

    async def async_select_option(self, option: str) -> None:
        await async_set_entry_option(
            self.hass, self.config_entry, self._option_key, option
        )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.debug("Setting up RCE PSE select entities for config entry: %s", config_entry.entry_id)
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[RCEWindowTimeSelectEntity] = []

    if not is_lite_mode(config_entry):
        for is_enabled, entity_defs in WINDOW_SELECT_GROUPS:
            if not is_enabled(config_entry):
                continue
            for unique_id, option_key, options_fn, default, icon in entity_defs:
                entities.append(
                    RCEWindowTimeSelectEntity(
                        coordinator,
                        config_entry,
                        unique_id,
                        option_key,
                        options_fn(),
                        default,
                        icon,
                    )
                )

    _LOGGER.debug("Adding %d RCE PSE select entities to Home Assistant", len(entities))
    async_add_entities(entities)
    _LOGGER.debug("RCE PSE select entities setup completed successfully")
