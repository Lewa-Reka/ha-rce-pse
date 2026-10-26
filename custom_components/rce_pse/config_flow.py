from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult, section
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_ENABLE_CHEAPEST_WINDOW,
    CONF_ENABLE_EXPENSIVE_WINDOW,
    CONF_ENABLE_HIGH_PRICE_THRESHOLD,
    CONF_ENABLE_LOW_PRICE_THRESHOLD,
    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_USE_HOURLY_PRICES,
    CONF_LITE_MODE,
    CONF_LOW_PRICE_THRESHOLD,
    CONF_HIGH_PRICE_THRESHOLD,
    CONF_USE_GROSS_PRICES,
    CONF_PRICE_DISPLAY_PRECISION,
    CONF_PRICE_UNIT,
    DEFAULT_ENABLE_CHEAPEST_WINDOW,
    DEFAULT_ENABLE_EXPENSIVE_WINDOW,
    DEFAULT_ENABLE_HIGH_PRICE_THRESHOLD,
    DEFAULT_ENABLE_LOW_PRICE_THRESHOLD,
    DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW,
    DEFAULT_LITE_MODE,
    DEFAULT_PRICE_DISPLAY_PRECISION,
    DEFAULT_PRICE_UNIT,
    UNIT_PLN_KWH,
    UNIT_PLN_MWH,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_USE_HOURLY_PRICES,
    DEFAULT_USE_GROSS_PRICES,
    DEFAULT_LOW_PRICE_THRESHOLD,
    DEFAULT_HIGH_PRICE_THRESHOLD,
    PRICE_DISPLAY_PRECISION_MAX,
    PRICE_DISPLAY_PRECISION_MIN,
    THRESHOLD_MAX,
    THRESHOLD_MIN,
    threshold_selector_step_for_unit,
)
from .options import get_effective_options, with_option_defaults
from .time_window import (
    duration_options,
    end_time_options,
    normalize_hhmm,
    start_time_options,
    time_window_error,
)

_LOGGER = logging.getLogger(__name__)

SECTION_PRICING = "pricing"
SECTION_CHEAPEST_WINDOW = "cheapest_window"
SECTION_EXPENSIVE_WINDOW = "expensive_window"
SECTION_SECOND_EXPENSIVE_WINDOW = "second_expensive_window"
SECTION_THRESHOLDS = "thresholds"

SECTION_KEYS = frozenset(
    {
        SECTION_PRICING,
        SECTION_CHEAPEST_WINDOW,
        SECTION_EXPENSIVE_WINDOW,
        SECTION_SECOND_EXPENSIVE_WINDOW,
        SECTION_THRESHOLDS,
    }
)

TIME_KEYS = (
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
)

WINDOW_END_KEYS = frozenset(
    {
        CONF_CHEAPEST_TIME_WINDOW_END,
        CONF_EXPENSIVE_TIME_WINDOW_END,
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    }
)

WINDOW_VALIDATION_CONFIG = (
    (
        CONF_ENABLE_CHEAPEST_WINDOW,
        DEFAULT_ENABLE_CHEAPEST_WINDOW,
        CONF_CHEAPEST_TIME_WINDOW_START,
        DEFAULT_TIME_WINDOW_START,
        CONF_CHEAPEST_TIME_WINDOW_END,
        DEFAULT_TIME_WINDOW_END,
        CONF_CHEAPEST_WINDOW_DURATION_HOURS,
        DEFAULT_WINDOW_DURATION_HOURS,
    ),
    (
        CONF_ENABLE_EXPENSIVE_WINDOW,
        DEFAULT_ENABLE_EXPENSIVE_WINDOW,
        CONF_EXPENSIVE_TIME_WINDOW_START,
        DEFAULT_TIME_WINDOW_START,
        CONF_EXPENSIVE_TIME_WINDOW_END,
        DEFAULT_TIME_WINDOW_END,
        CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
        DEFAULT_WINDOW_DURATION_HOURS,
    ),
    (
        CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
        DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW,
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
        DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
        DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
        CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
        DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    ),
)


def migrate_price_unit_in_mapping(data: dict[str, Any]) -> dict[str, Any]:
    out = dict(data)
    if CONF_PRICE_UNIT not in out:
        return out
    v = out[CONF_PRICE_UNIT]
    if v == "pln_kwh":
        out[CONF_PRICE_UNIT] = UNIT_PLN_KWH
    elif v == "pln_mwh":
        out[CONF_PRICE_UNIT] = UNIT_PLN_MWH
    return out


def migrate_legacy_time_values(data: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(data)
    for key in TIME_KEYS:
        if key not in out:
            continue
        v = out[key]
        if isinstance(v, int):
            if key in WINDOW_END_KEYS and v == 24:
                out[key] = "00:00"
            else:
                out[key] = f"{int(v):02d}:00"
        elif isinstance(v, str) and v.isdigit():
            iv = int(v)
            if key in WINDOW_END_KEYS and iv == 24:
                out[key] = "00:00"
            else:
                out[key] = f"{iv:02d}:00"
    return out


def migrate_option_defaults(data: Mapping[str, Any]) -> dict[str, Any]:
    return with_option_defaults(data)


def _select_options(values: list[str]) -> list[dict[str, str]]:
    return [{"value": value, "label": value} for value in values]


def _start_time_select_options() -> list[dict[str, str]]:
    return _select_options(start_time_options())


def _end_time_select_options() -> list[dict[str, str]]:
    return _select_options(end_time_options())


def _duration_select_options() -> list[dict[str, str]]:
    return _select_options(duration_options())


def _flatten_rce_user_input(user_input: dict[str, Any]) -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in user_input.items():
        if key in SECTION_KEYS and isinstance(value, dict):
            flat.update(value)
        else:
            flat[key] = value
    return flat


def _coerce_time_values(flat: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(flat)
    for key in TIME_KEYS:
        if key not in out:
            continue
        v = out[key]
        if isinstance(v, int):
            if key in WINDOW_END_KEYS and v == 24:
                out[key] = "00:00"
            else:
                out[key] = f"{int(v):02d}:00"
        elif hasattr(v, "hour") and hasattr(v, "minute"):
            h = int(v.hour)
            m = int(v.minute)
            if h == 24:
                out[key] = "24:00"
            else:
                out[key] = f"{h:02d}:{m:02d}"
        else:
            out[key] = normalize_hhmm(v)
    return out


def _window_row_error(
    flat: Mapping[str, Any],
    enable_key: str,
    enable_default: bool,
    start_key: str,
    start_default: str,
    end_key: str,
    end_default: str,
    duration_key: str,
    duration_default: str,
) -> str | None:
    if not flat.get(enable_key, enable_default):
        return None
    return time_window_error(
        str(flat.get(start_key, start_default)),
        str(flat.get(end_key, end_default)),
        str(flat.get(duration_key, duration_default)),
    )


def window_option_error(flat: Mapping[str, Any], option_key: str, option_value: str) -> str | None:
    proposed = dict(flat)
    proposed[option_key] = option_value
    for row in WINDOW_VALIDATION_CONFIG:
        (
            _enable_key,
            _enable_default,
            start_key,
            _start_default,
            end_key,
            _end_default,
            duration_key,
            _duration_default,
        ) = row
        if option_key not in (start_key, end_key, duration_key):
            continue
        return _window_row_error(proposed, *row)
    return None


def _time_window_errors(flat: Mapping[str, Any]) -> dict[str, str]:
    if flat.get(CONF_LITE_MODE, DEFAULT_LITE_MODE):
        return {}

    for row in WINDOW_VALIDATION_CONFIG:
        error = _window_row_error(flat, *row)
        if error:
            return {"base": error}
    return {}


def _price_unit_select_options() -> list[dict[str, str]]:
    return [
        {"value": UNIT_PLN_MWH, "label": UNIT_PLN_MWH},
        {"value": UNIT_PLN_KWH, "label": UNIT_PLN_KWH},
    ]

def _rce_form_schema(current_data: Mapping[str, Any]) -> vol.Schema:
    current_data = with_option_defaults(current_data)

    def _get(key: str, default: Any) -> Any:
        v = current_data.get(key, default)
        if isinstance(v, int) and key in TIME_KEYS:
            if key.endswith("_end") and v == 24:
                return "00:00"
            return f"{int(v):02d}:00"
        if key in TIME_KEYS and v is not None:
            if isinstance(v, dict):
                return normalize_hhmm(v)
            return normalize_hhmm(str(v))
        return v

    price_unit = _get(CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT)
    threshold_step = threshold_selector_step_for_unit(price_unit)

    pricing_inner = vol.Schema(
        {
            vol.Optional(
                CONF_LITE_MODE, default=_get(CONF_LITE_MODE, DEFAULT_LITE_MODE)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Optional(
                CONF_USE_HOURLY_PRICES, default=_get(CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Optional(
                CONF_USE_GROSS_PRICES, default=_get(CONF_USE_GROSS_PRICES, DEFAULT_USE_GROSS_PRICES)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_PRICE_UNIT, default=_get(CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT)
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_price_unit_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(
                CONF_PRICE_DISPLAY_PRECISION,
                default=_get(
                    CONF_PRICE_DISPLAY_PRECISION, DEFAULT_PRICE_DISPLAY_PRECISION
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=PRICE_DISPLAY_PRECISION_MIN,
                    max=PRICE_DISPLAY_PRECISION_MAX,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )

    cheapest_inner = vol.Schema(
        {
            vol.Optional(
                CONF_ENABLE_CHEAPEST_WINDOW,
                default=_get(CONF_ENABLE_CHEAPEST_WINDOW, DEFAULT_ENABLE_CHEAPEST_WINDOW),
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_START,
                default=_get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_start_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_END,
                default=_get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_end_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_CHEAPEST_WINDOW_DURATION_HOURS,
                default=_get(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_duration_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )

    expensive_inner = vol.Schema(
        {
            vol.Optional(
                CONF_ENABLE_EXPENSIVE_WINDOW,
                default=_get(CONF_ENABLE_EXPENSIVE_WINDOW, DEFAULT_ENABLE_EXPENSIVE_WINDOW),
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_START,
                default=_get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_start_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_END,
                default=_get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_end_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
                default=_get(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_duration_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )

    second_expensive_inner = vol.Schema(
        {
            vol.Optional(
                CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
                default=_get(
                    CONF_ENABLE_SECOND_EXPENSIVE_WINDOW,
                    DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW,
                ),
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                default=_get(
                    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_start_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                default=_get(
                    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_end_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                default=_get(
                    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_duration_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )

    thresholds_inner = vol.Schema(
        {
            vol.Optional(
                CONF_ENABLE_LOW_PRICE_THRESHOLD,
                default=_get(
                    CONF_ENABLE_LOW_PRICE_THRESHOLD, DEFAULT_ENABLE_LOW_PRICE_THRESHOLD
                ),
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_LOW_PRICE_THRESHOLD,
                default=_get(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=THRESHOLD_MIN,
                    max=THRESHOLD_MAX,
                    step=threshold_step,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement=price_unit,
                )
            ),
            vol.Optional(
                CONF_ENABLE_HIGH_PRICE_THRESHOLD,
                default=_get(
                    CONF_ENABLE_HIGH_PRICE_THRESHOLD, DEFAULT_ENABLE_HIGH_PRICE_THRESHOLD
                ),
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_HIGH_PRICE_THRESHOLD,
                default=_get(CONF_HIGH_PRICE_THRESHOLD, DEFAULT_HIGH_PRICE_THRESHOLD),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=THRESHOLD_MIN,
                    max=THRESHOLD_MAX,
                    step=threshold_step,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement=price_unit,
                )
            ),
        }
    )

    return vol.Schema(
        {
            vol.Required(SECTION_PRICING): section(pricing_inner, {"collapsed": False}),
            vol.Required(SECTION_THRESHOLDS): section(thresholds_inner, {"collapsed": True}),
            vol.Required(SECTION_CHEAPEST_WINDOW): section(cheapest_inner, {"collapsed": True}),
            vol.Required(SECTION_EXPENSIVE_WINDOW): section(expensive_inner, {"collapsed": True}),
            vol.Required(SECTION_SECOND_EXPENSIVE_WINDOW): section(
                second_expensive_inner, {"collapsed": True}
            ),
        }
    )


CONFIG_SCHEMA = _rce_form_schema({})


class RCEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]

    VERSION = 3
    MINOR_VERSION = 0
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    def async_get_options_flow(config_entry):
        return RCEOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        _LOGGER.debug("Starting RCE PSE config flow")

        if self._async_current_entries():
            _LOGGER.debug("RCE PSE integration already configured, aborting")
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}

        if user_input is not None:
            flat = _coerce_time_values(_flatten_rce_user_input(user_input))
            errors = _time_window_errors(flat)
            if not errors:
                _LOGGER.debug("Creating RCE PSE config entry with options: %s", flat)
                await self.async_set_unique_id("rce_pse")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="RCE PSE", data=flat)

        _LOGGER.debug("Showing RCE PSE configuration form")
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )


class RCEOptionsFlow(config_entries.OptionsFlow):

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            flat = _coerce_time_values(_flatten_rce_user_input(user_input))
            errors = _time_window_errors(flat)
            if not errors:
                _LOGGER.debug("Updating RCE PSE options: %s", flat)
                return self.async_create_entry(title="", data=flat)

        current_data = get_effective_options(self.config_entry)
        options_schema = _rce_form_schema(current_data)

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
        )
