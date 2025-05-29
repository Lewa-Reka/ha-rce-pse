"""Config flow for RCE PSE integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class RCEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RCE PSE."""

    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        _LOGGER.debug("Starting RCE PSE config flow")
        
        if self._async_current_entries():
            _LOGGER.debug("RCE PSE integration already configured, aborting")
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            _LOGGER.debug("Showing RCE PSE configuration form")
            return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

        _LOGGER.debug("Creating RCE PSE config entry")
        await self.async_set_unique_id("rce_pse")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="RCE PSE", data={}) 