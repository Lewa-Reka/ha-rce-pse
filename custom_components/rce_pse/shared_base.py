from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    CONF_PRICE_UNIT,
    DEFAULT_PRICE_UNIT,
    DISPLAY_PRICE_DECIMALS,
    DOMAIN,
    MANUFACTURER,
)
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

    def native_price_unit(self) -> str:
        return self.coordinator._get_config_value(CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT)

    def round_display_price(self, value: float) -> float:
        return round(value, DISPLAY_PRICE_DECIMALS)

    def round_price_records_for_attributes(self, records: list[dict]) -> list[dict]:
        out: list[dict] = []
        for record in records:
            item = dict(record)
            for key in ("rce_pln", "rce_pln_neg_to_zero"):
                if key in item and item[key] is not None:
                    try:
                        item[key] = round(float(item[key]), DISPLAY_PRICE_DECIMALS)
                    except (ValueError, TypeError):
                        pass
            out.append(item)
        return out

    def round_price_dict_for_attributes(self, record: dict | None) -> dict | None:
        if record is None:
            return None
        item = dict(record)
        for key in ("rce_pln", "rce_pln_neg_to_zero"):
            if key in item and item[key] is not None:
                try:
                    item[key] = round(float(item[key]), DISPLAY_PRICE_DECIMALS)
                except (ValueError, TypeError):
                    pass
        return item

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

    def get_today_pdgsz_data(self) -> list[dict]:
        if not self.coordinator.data:
            return []
        pdgsz = self.coordinator.data.get("pdgsz_data") or []
        today = dt_util.now().strftime("%Y-%m-%d")
        out = [r for r in pdgsz if r.get("business_date") == today]
        return sorted(out, key=lambda r: r.get("dtime", ""))

    def get_tomorrow_pdgsz_data(self) -> list[dict]:
        if not self.is_tomorrow_data_available():
            return []
        if not self.coordinator.data:
            return []
        pdgsz = self.coordinator.data.get("pdgsz_data") or []
        tomorrow = (dt_util.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        out = [r for r in pdgsz if r.get("business_date") == tomorrow]
        return sorted(out, key=lambda r: r.get("dtime", ""))

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