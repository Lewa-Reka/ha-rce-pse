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
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_USE_HOURLY_PRICES,
    CONF_LOW_PRICE_THRESHOLD,
    CONF_USE_GROSS_PRICES,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_USE_HOURLY_PRICES,
    DEFAULT_USE_GROSS_PRICES,
    DEFAULT_LOW_PRICE_THRESHOLD,
)

_LOGGER = logging.getLogger(__name__)

SECTION_PRICING = "pricing"
SECTION_CHEAPEST_WINDOW = "cheapest_window"
SECTION_EXPENSIVE_WINDOW = "expensive_window"
SECTION_SECOND_EXPENSIVE_WINDOW = "second_expensive_window"

SECTION_KEYS = frozenset(
    {
        SECTION_PRICING,
        SECTION_CHEAPEST_WINDOW,
        SECTION_EXPENSIVE_WINDOW,
        SECTION_SECOND_EXPENSIVE_WINDOW,
    }
)


def _flatten_rce_user_input(user_input: dict[str, Any]) -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in user_input.items():
        if key in SECTION_KEYS and isinstance(value, dict):
            flat.update(value)
        else:
            flat[key] = value
    return flat


def _rce_form_schema(current_data: Mapping[str, Any]) -> vol.Schema:
    def _get(key: str, default: Any) -> Any:
        return current_data.get(key, default)

    pricing_inner = vol.Schema(
        {
            vol.Optional(
                CONF_USE_HOURLY_PRICES, default=_get(CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Optional(
                CONF_USE_GROSS_PRICES, default=_get(CONF_USE_GROSS_PRICES, DEFAULT_USE_GROSS_PRICES)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Optional(
                CONF_LOW_PRICE_THRESHOLD, default=_get(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=-2000,
                    max=2000,
                    step=0.01,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="PLN/MWh",
                )
            ),
        }
    )

    cheapest_inner = vol.Schema(
        {
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_START,
                default=_get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=23,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_END,
                default=_get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_CHEAPEST_WINDOW_DURATION_HOURS,
                default=_get(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )

    expensive_inner = vol.Schema(
        {
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_START,
                default=_get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=23,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_END,
                default=_get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
                default=_get(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )

    second_expensive_inner = vol.Schema(
        {
            vol.Required(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                default=_get(
                    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=23,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                default=_get(
                    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                default=_get(
                    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                ),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        }
    )

    return vol.Schema(
        {
            vol.Required(SECTION_PRICING): section(pricing_inner, {"collapsed": False}),
            vol.Required(SECTION_CHEAPEST_WINDOW): section(cheapest_inner, {"collapsed": True}),
            vol.Required(SECTION_EXPENSIVE_WINDOW): section(expensive_inner, {"collapsed": True}),
            vol.Required(SECTION_SECOND_EXPENSIVE_WINDOW): section(
                second_expensive_inner, {"collapsed": True}
            ),
        }
    )


CONFIG_SCHEMA = _rce_form_schema({})


def _time_window_errors(flat: Mapping[str, Any]) -> dict[str, str]:
    errors: dict[str, str] = {}
    cheapest_start = flat.get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
    cheapest_end = flat.get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
    expensive_start = flat.get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
    expensive_end = flat.get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
    second_expensive_start = flat.get(
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_START, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START
    )
    second_expensive_end = flat.get(
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_END, DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END
    )

    if cheapest_start >= cheapest_end:
        errors["base"] = "invalid_time_window"
    elif expensive_start >= expensive_end:
        errors["base"] = "invalid_time_window"
    elif second_expensive_start >= second_expensive_end:
        errors["base"] = "invalid_time_window"
    return errors


class RCEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]

    VERSION = 1
    MINOR_VERSION = 1
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
            flat = _flatten_rce_user_input(user_input)
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
            flat = _flatten_rce_user_input(user_input)
            errors = _time_window_errors(flat)
            if not errors:
                _LOGGER.debug("Updating RCE PSE options: %s", flat)
                return self.async_create_entry(title="", data=flat)

        current_data = self.config_entry.options if self.config_entry.options else self.config_entry.data
        options_schema = _rce_form_schema(current_data)

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
        )
