from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from ..const import CONF_HIGH_PRICE_THRESHOLD, DEFAULT_HIGH_PRICE_THRESHOLD
from ..coordinator import RCEPSEDataUpdateCoordinator
from .base import RCEBaseBinarySensor


class RCEHighPriceThresholdWindowActiveBinarySensor(RCEBaseBinarySensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator, "high_price_threshold_window_active")
        self.config_entry = config_entry
        self._attr_icon = "mdi:clock-check"

    def _threshold(self) -> float:
        ce = self.config_entry
        if ce.options and CONF_HIGH_PRICE_THRESHOLD in ce.options:
            return float(ce.options[CONF_HIGH_PRICE_THRESHOLD])
        if CONF_HIGH_PRICE_THRESHOLD in ce.data:
            return float(ce.data[CONF_HIGH_PRICE_THRESHOLD])
        return float(
            self.coordinator._get_config_value(
                CONF_HIGH_PRICE_THRESHOLD, DEFAULT_HIGH_PRICE_THRESHOLD
            )
        )

    @property
    def is_on(self) -> bool:
        if not self.available:
            return False
        rec = self.get_current_price_data()
        if not rec:
            return False
        try:
            price = self.round_display_price(float(rec["rce_pln"]))
        except (ValueError, KeyError, TypeError):
            return False
        return price >= self._threshold()
