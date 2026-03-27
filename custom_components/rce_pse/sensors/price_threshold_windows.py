from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as dt_util

from ..const import (
    CONF_HIGH_PRICE_THRESHOLD,
    CONF_LOW_PRICE_THRESHOLD,
    DEFAULT_HIGH_PRICE_THRESHOLD,
    DEFAULT_LOW_PRICE_THRESHOLD,
)
from ..coordinator import RCEPSEDataUpdateCoordinator
from ..time_window import parse_pse_dtime
from .base import RCEBaseSensor


class RCEPriceThresholdWindowTimestampSensor(RCEBaseSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
        unique_id: str,
        is_below: bool,
        is_start: bool,
    ) -> None:
        super().__init__(coordinator, unique_id)
        self.config_entry = config_entry
        self._is_below = is_below
        self._is_start = is_start
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-start" if is_start else "mdi:clock-end"

    def _threshold(self) -> float:
        ce = self.config_entry
        key = CONF_LOW_PRICE_THRESHOLD if self._is_below else CONF_HIGH_PRICE_THRESHOLD
        default = (
            DEFAULT_LOW_PRICE_THRESHOLD if self._is_below else DEFAULT_HIGH_PRICE_THRESHOLD
        )
        if ce.options and key in ce.options:
            return float(ce.options[key])
        if key in ce.data:
            return float(ce.data[key])
        return float(self.coordinator._get_config_value(key, default))

    def nearest_window(self) -> list[dict] | None:
        today = self.get_today_data()
        tomorrow = self.get_tomorrow_data()
        return self.calculator.pick_nearest_threshold_window(
            today,
            tomorrow,
            self._threshold(),
            self._is_below,
            dt_util.now(),
        )

    def _window_start_local(self, window: list[dict]) -> datetime | None:
        if not window:
            return None
        try:
            pe = parse_pse_dtime(window[0]["dtime"])
            return dt_util.as_local(pe - timedelta(minutes=15))
        except (ValueError, KeyError, IndexError):
            return None

    def _window_end_local(self, window: list[dict]) -> datetime | None:
        if not window:
            return None
        try:
            pe = parse_pse_dtime(window[-1]["dtime"])
            return dt_util.as_local(pe)
        except (ValueError, KeyError, IndexError):
            return None

    @property
    def native_value(self) -> datetime | None:
        if not self.available:
            return None
        w = self.nearest_window()
        if not w:
            return None
        if self._is_start:
            return self._window_start_local(w)
        return self._window_end_local(w)


class RCELowPriceThresholdWindowStartSensor(RCEPriceThresholdWindowTimestampSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        super().__init__(
            coordinator,
            config_entry,
            "low_price_threshold_window_start",
            True,
            True,
        )


class RCELowPriceThresholdWindowEndSensor(RCEPriceThresholdWindowTimestampSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        super().__init__(
            coordinator,
            config_entry,
            "low_price_threshold_window_end",
            True,
            False,
        )


class RCEHighPriceThresholdWindowStartSensor(RCEPriceThresholdWindowTimestampSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        super().__init__(
            coordinator,
            config_entry,
            "high_price_threshold_window_start",
            False,
            True,
        )


class RCEHighPriceThresholdWindowEndSensor(RCEPriceThresholdWindowTimestampSensor):

    def __init__(
        self,
        coordinator: RCEPSEDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        super().__init__(
            coordinator,
            config_entry,
            "high_price_threshold_window_end",
            False,
            False,
        )
