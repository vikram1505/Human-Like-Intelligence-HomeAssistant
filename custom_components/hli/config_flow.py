from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import CONF_MIN_CONFIDENCE, DEFAULT_MIN_CONFIDENCE, DOMAIN
class HLIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION=1
    async def async_step_user(self,user_input:dict[str,Any]|None=None):
        await self.async_set_unique_id(DOMAIN); self._abort_if_unique_id_configured()
        if user_input is not None: return self.async_create_entry(title="Human-Like Intelligence",data={})
        return self.async_show_form(step_id="user")
    @staticmethod
    @callback
    def async_get_options_flow(config_entry): return HLIOptionsFlow()
class HLIOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self,user_input=None):
        if user_input is not None: return self.async_create_entry(title="",data=user_input)
        return self.async_show_form(step_id="init",data_schema=vol.Schema({vol.Optional(CONF_MIN_CONFIDENCE,default=DEFAULT_MIN_CONFIDENCE):vol.All(vol.Coerce(float),vol.Range(min=0.5,max=1.0))}))
