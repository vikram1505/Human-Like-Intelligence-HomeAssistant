"""Update coordinator for Human-Like Intelligence."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, UPDATE_SECONDS
from .engine import evaluate_house
from .models import HouseModel

_LOGGER = logging.getLogger(__name__)


class HLICoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate periodic evaluation of the discovered HLI model."""

    def __init__(self, hass: HomeAssistant, model: HouseModel) -> None:
        """Initialize the HLI coordinator."""
        self.model = model
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_SECONDS),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Calculate the latest HLI intelligence state."""
        return evaluate_house(self.hass, self.model)
