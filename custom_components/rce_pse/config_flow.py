from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

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

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_CHEAPEST_TIME_WINDOW_START, default=DEFAULT_TIME_WINDOW_START): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0,
            max=23,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Required(CONF_CHEAPEST_TIME_WINDOW_END, default=DEFAULT_TIME_WINDOW_END): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=24,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Required(CONF_CHEAPEST_WINDOW_DURATION_HOURS, default=DEFAULT_WINDOW_DURATION_HOURS): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=24,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Required(CONF_EXPENSIVE_TIME_WINDOW_START, default=DEFAULT_TIME_WINDOW_START): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=0,
            max=23,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Required(CONF_EXPENSIVE_TIME_WINDOW_END, default=DEFAULT_TIME_WINDOW_END): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=24,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
    vol.Required(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, default=DEFAULT_WINDOW_DURATION_HOURS): selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=1,
            max=24,
            step=1,
            mode=selector.NumberSelectorMode.BOX,
        )
    ),
})


class RCEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    def async_get_options_flow(config_entry):
        return RCEOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
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

    async def async_step_init(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
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

        current_data = self.config_entry.options if self.config_entry.options else self.config_entry.data
        options_schema = vol.Schema({
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_START, 
                default=current_data.get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
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
                default=current_data.get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
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
                default=current_data.get(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_START, 
                default=current_data.get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START)
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
                default=current_data.get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END)
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
                default=current_data.get(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=24,
                    step=1,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors
        ) 