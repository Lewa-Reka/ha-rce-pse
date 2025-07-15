from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, MANUFACTURER
from .price_calculator import PriceCalculator

if TYPE_CHECKING:
    from .coordinator import RCEPSEDataUpdateCoordinator

class RCEBaseCommonEntity(CoordinatorEntity):
    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator, unique_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"rce_pse_{unique_id}"
        self._attr_has_entity_name = True
        self._attr_translation_key = f"rce_pse_{unique_id}"
        self.calculator = PriceCalculator()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "rce_pse")},
            "name": "RCE PSE",
            "model": "RCE PSE",
            "entry_type": "service",
            "manufacturer": MANUFACTURER,
        }

    def get_today_data(self) -> list[dict]:
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        today = dt_util.now().strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == today
        ]

    def get_tomorrow_data(self) -> list[dict]:
        if not self.is_tomorrow_data_available():
            return []
        if not self.coordinator.data or not self.coordinator.data.get("raw_data"):
            return []
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        return [
            record for record in self.coordinator.data["raw_data"]
            if record.get("business_date") == tomorrow
        ]

    def is_tomorrow_data_available(self) -> bool:
        now = dt_util.now()
        return now.hour >= 14

    @property
    def available(self) -> bool:
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self.coordinator.data.get("raw_data") is not None
        ) 