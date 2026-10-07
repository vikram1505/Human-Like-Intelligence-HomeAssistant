"""Human-Like Intelligence integration setup."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_MIN_CONFIDENCE, DEFAULT_MIN_CONFIDENCE, PLATFORMS
from .coordinator import HLICoordinator
from .discovery import async_discover


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HLI from a Home Assistant config entry."""
    min_confidence = float(
        entry.options.get(CONF_MIN_CONFIDENCE, DEFAULT_MIN_CONFIDENCE)
    )
    model = await async_discover(hass, min_confidence)
    coordinator = HLICoordinator(hass, model)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload an HLI config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
