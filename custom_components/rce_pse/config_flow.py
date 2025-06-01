"""Config flow for RCE PSE integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
)

_LOGGER = logging.getLogger(__name__)

# Configuration schema
CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_CHEAPEST_TIME_WINDOW_START, default=DEFAULT_TIME_WINDOW_START): vol.All(
        vol.Coerce(int), vol.Range(min=0, max=23)
    ),
    vol.Required(CONF_CHEAPEST_TIME_WINDOW_END, default=DEFAULT_TIME_WINDOW_END): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=24)
    ),
    vol.Required(CONF_CHEAPEST_WINDOW_DURATION_HOURS, default=DEFAULT_WINDOW_DURATION_HOURS): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=24)
    ),
    vol.Required(CONF_EXPENSIVE_TIME_WINDOW_START, default=DEFAULT_TIME_WINDOW_START): vol.All(
        vol.Coerce(int), vol.Range(min=0, max=23)
    ),
    vol.Required(CONF_EXPENSIVE_TIME_WINDOW_END, default=DEFAULT_TIME_WINDOW_END): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=24)
    ),
    vol.Required(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, default=DEFAULT_WINDOW_DURATION_HOURS): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=24)
    ),
})


class RCEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RCE PSE."""

    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return RCEOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        _LOGGER.debug("Starting RCE PSE config flow")
        
        if self._async_current_entries():
            _LOGGER.debug("RCE PSE integration already configured, aborting")
            return self.async_abort(reason="single_instance_allowed")

        errors = {}

        if user_input is not None:
            cheapest_start = user_input.get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
            cheapest_end = user_input.get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
            expensive_start = user_input.get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
            expensive_end = user_input.get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
            
            if cheapest_start >= cheapest_end:
                errors["base"] = "invalid_time_window"
            elif expensive_start >= expensive_end:
                errors["base"] = "invalid_time_window"
            else:
                _LOGGER.debug("Creating RCE PSE config entry with options: %s", user_input)
                await self.async_set_unique_id("rce_pse")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="RCE PSE", data=user_input)

        _LOGGER.debug("Showing RCE PSE configuration form")
        return self.async_show_form(
            step_id="user", 
            data_schema=CONFIG_SCHEMA,
            errors=errors
        )


class RCEOptionsFlow(config_entries.OptionsFlow):
    """Handle RCE PSE options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors = {}

        if user_input is not None:
            cheapest_start = user_input.get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
            cheapest_end = user_input.get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
            expensive_start = user_input.get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
            expensive_end = user_input.get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
            
            if cheapest_start >= cheapest_end:
                errors["base"] = "invalid_time_window"
            elif expensive_start >= expensive_end:
                errors["base"] = "invalid_time_window"
            else:
                _LOGGER.debug("Updating RCE PSE options: %s", user_input)
                return self.async_create_entry(title="", data=user_input)

        # Get current options from config entry or use defaults
        current_data = self.config_entry.data
        options_schema = vol.Schema({
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_START, 
                default=current_data.get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_END, 
                default=current_data.get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
            vol.Required(
                CONF_CHEAPEST_WINDOW_DURATION_HOURS, 
                default=current_data.get(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_START, 
                default=current_data.get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_END, 
                default=current_data.get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
            vol.Required(
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS, 
                default=current_data.get(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors
        ) 