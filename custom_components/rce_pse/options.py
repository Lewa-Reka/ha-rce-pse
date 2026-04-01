from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_ENABLE_CHEAPEST_WINDOW,
    CONF_ENABLE_EXPENSIVE_WINDOW,
    CONF_ENABLE_HIGH_PRICE_THRESHOLD,
    CONF_ENABLE_LOW_PRICE_THRESHOLD,
    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
    CONF_LITE_MODE,
    DEFAULT_ENABLE_CHEAPEST_WINDOW,
    DEFAULT_ENABLE_EXPENSIVE_WINDOW,
    DEFAULT_ENABLE_HIGH_PRICE_THRESHOLD,
    DEFAULT_ENABLE_LOW_PRICE_THRESHOLD,
    DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW,
    DEFAULT_LITE_MODE,
)

OPTION_DEFAULTS: dict[str, Any] = {
    CONF_LITE_MODE: DEFAULT_LITE_MODE,
    CONF_ENABLE_CHEAPEST_WINDOW: DEFAULT_ENABLE_CHEAPEST_WINDOW,
    CONF_ENABLE_EXPENSIVE_WINDOW: DEFAULT_ENABLE_EXPENSIVE_WINDOW,
    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW,
    CONF_ENABLE_LOW_PRICE_THRESHOLD: DEFAULT_ENABLE_LOW_PRICE_THRESHOLD,
    CONF_ENABLE_HIGH_PRICE_THRESHOLD: DEFAULT_ENABLE_HIGH_PRICE_THRESHOLD,
}


def with_option_defaults(data: Mapping[str, Any] | None) -> dict[str, Any]:
    merged = dict(OPTION_DEFAULTS)
    if data:
        merged.update(data)
    return merged


def get_entry_value(config_entry: ConfigEntry, key: str, default: Any) -> Any:
    if config_entry.options and key in config_entry.options:
        return config_entry.options[key]
    if config_entry.data and key in config_entry.data:
        return config_entry.data[key]
    return default


def is_lite_mode(config_entry: ConfigEntry) -> bool:
    return bool(get_entry_value(config_entry, CONF_LITE_MODE, DEFAULT_LITE_MODE))


def is_cheapest_window_enabled(config_entry: ConfigEntry) -> bool:
    return bool(
        get_entry_value(
            config_entry,
            CONF_ENABLE_CHEAPEST_WINDOW,
            DEFAULT_ENABLE_CHEAPEST_WINDOW,
        )
    )


def is_expensive_window_enabled(config_entry: ConfigEntry) -> bool:
    return bool(
        get_entry_value(
            config_entry,
            CONF_ENABLE_EXPENSIVE_WINDOW,
            DEFAULT_ENABLE_EXPENSIVE_WINDOW,
        )
    )


def is_second_expensive_window_enabled(config_entry: ConfigEntry) -> bool:
    return bool(
        get_entry_value(
            config_entry,
            CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
            DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW,
        )
    )


def is_low_price_threshold_enabled(config_entry: ConfigEntry) -> bool:
    return bool(
        get_entry_value(
            config_entry,
            CONF_ENABLE_LOW_PRICE_THRESHOLD,
            DEFAULT_ENABLE_LOW_PRICE_THRESHOLD,
        )
    )


def is_high_price_threshold_enabled(config_entry: ConfigEntry) -> bool:
    return bool(
        get_entry_value(
            config_entry,
            CONF_ENABLE_HIGH_PRICE_THRESHOLD,
            DEFAULT_ENABLE_HIGH_PRICE_THRESHOLD,
        )
    )
