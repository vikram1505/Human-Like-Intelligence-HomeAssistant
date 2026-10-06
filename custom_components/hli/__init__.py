from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import CONF_MIN_CONFIDENCE, DEFAULT_MIN_CONFIDENCE, PLATFORMS
from .coordinator import HLICoordinator
from .discovery import async_discover

type HLIConfigEntry = ConfigEntry[HLICoordinator]
async def async_setup_entry(hass: HomeAssistant, entry: HLIConfigEntry) -> bool:
    model=await async_discover(hass,float(entry.options.get(CONF_MIN_CONFIDENCE,DEFAULT_MIN_CONFIDENCE)))
    coordinator=HLICoordinator(hass,model); await coordinator.async_config_entry_first_refresh(); entry.runtime_data=coordinator
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS); return True
async def async_unload_entry(hass: HomeAssistant, entry: HLIConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
