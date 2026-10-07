"""Config flow for Human-Like Intelligence."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import CONF_MIN_CONFIDENCE, DEFAULT_MIN_CONFIDENCE, DOMAIN


class HLIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle initial HLI configuration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Create the single local HLI config entry."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title="Human-Like Intelligence", data={})
        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(_config_entry) -> config_entries.OptionsFlow:
        """Return the options flow for HLI."""
        return HLIOptionsFlow()


class HLIOptionsFlow(config_entries.OptionsFlow):
    """Handle user-adjustable HLI discovery options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Configure the minimum automatic-classification confidence."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_MIN_CONFIDENCE,
                    default=DEFAULT_MIN_CONFIDENCE,
                ): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=1.0))
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
