from __future__ import annotations
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, UPDATE_SECONDS
from .engine import evaluate_house
from .models import HouseModel

class HLICoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, model: HouseModel) -> None:
        self.model=model
        super().__init__(hass, logger=__import__('logging').getLogger(__name__), name=DOMAIN, update_interval=timedelta(seconds=UPDATE_SECONDS))
    async def _async_update_data(self) -> dict:
        return evaluate_house(self.hass,self.model)
