from __future__ import annotations

from datetime import timedelta
from typing import Any, TYPE_CHECKING

from .base import RCEPriceSensor
from ..const import CONF_USE_GROSS_PRICES, DEFAULT_USE_GROSS_PRICES, TAX_RATE

if TYPE_CHECKING:
    from ..coordinator import RCEPSEDataUpdateCoordinator


class RCETodayMainSensor(RCEPriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_price")
        self._attr_native_unit_of_measurement = self.native_price_unit()
        self._attr_icon = "mdi:cash"

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def scan_interval(self) -> timedelta:
        return timedelta(minutes=1)

    @property
    def native_value(self) -> float | None:
        current_data = self.get_current_price_data()
        if current_data:
            return self.round_display_price(float(current_data["rce_pln"]))
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        today_data = self.get_today_data()
        excluded_keys = {"rce_pln_neg_to_zero", "publication_ts"}
        sanitized_today_data = self.round_price_records_for_attributes(
            [{k: v for k, v in record.items() if k not in excluded_keys} for record in today_data]
        )
        
        attributes = {
            "last_update": self.coordinator.data.get("last_update") if self.coordinator.data else None,
            "data_points": len(today_data),
            "prices": sanitized_today_data,
        }
        
        return attributes


class RCETodayProsumerSellingPriceSensor(RCEPriceSensor):

    def __init__(self, coordinator: RCEPSEDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "today_prosumer_selling_price")
        self._attr_native_unit_of_measurement = self.native_price_unit()
        self._attr_icon = "mdi:cash"

    @property
    def native_value(self) -> float | None:
        current_data = self.get_current_price_data()
        if current_data:
            price = float(current_data["rce_pln_neg_to_zero"])
            if price <= 0:
                return 0

            use_gross_prices = self.coordinator._get_config_value(
                CONF_USE_GROSS_PRICES, DEFAULT_USE_GROSS_PRICES
            )

            if use_gross_prices:
                return self.round_display_price(price)

            return self.round_display_price(price * (1 + TAX_RATE))
        return None