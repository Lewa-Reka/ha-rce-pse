from __future__ import annotations

from datetime import timedelta
from typing import Final

from homeassistant.const import UnitOfEnergy

DOMAIN: Final[str] = "rce_pse"
SENSOR_PREFIX: Final[str] = "RCE PSE"
MANUFACTURER: Final[str] = "Lewa-Reka"
PSE_API_BASE_URL: Final[str] = "https://api.raporty.pse.pl/api"
PSE_ENDPOINT_RCE_PLN: Final[str] = "rce-pln"
PSE_ENDPOINT_PDGSZ: Final[str] = "pdgsz"
RCE_PLN_API_SELECT: Final[str] = "dtime,period,rce_pln,business_date"
PDGSZ_API_SELECT: Final[str] = "business_date,dtime,is_active,usage_fcst"
PSE_API_PAGE_SIZE: Final[int] = 200
API_UPDATE_INTERVAL: Final[timedelta] = timedelta(minutes=30)
PDGSZ_USAGE_FCST_TO_ATTR: Final[dict[int, str]] = {
    0: "recommended_usage",
    1: "normal_usage",
    2: "recommended_saving",
    3: "required_restriction",
}

TAX_RATE: Final[float] = 0.23

CONF_CHEAPEST_TIME_WINDOW_START: Final[str] = "cheapest_time_window_start"
CONF_CHEAPEST_TIME_WINDOW_END: Final[str] = "cheapest_time_window_end"
CONF_CHEAPEST_WINDOW_DURATION_HOURS: Final[str] = "cheapest_window_duration_hours"

CONF_EXPENSIVE_TIME_WINDOW_START: Final[str] = "expensive_time_window_start"
CONF_EXPENSIVE_TIME_WINDOW_END: Final[str] = "expensive_time_window_end"
CONF_EXPENSIVE_WINDOW_DURATION_HOURS: Final[str] = "expensive_window_duration_hours"

CONF_SECOND_EXPENSIVE_TIME_WINDOW_START: Final[str] = "second_expensive_time_window_start"
CONF_SECOND_EXPENSIVE_TIME_WINDOW_END: Final[str] = "second_expensive_time_window_end"
CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS: Final[str] = "second_expensive_window_duration_hours"

CONF_WINDOW_DURATION_HOURS: Final[str] = "window_duration_hours"
CONF_USE_HOURLY_PRICES: Final[str] = "use_hourly_prices"
CONF_LITE_MODE: Final[str] = "lite_mode"
CONF_ENABLE_CHEAPEST_WINDOW: Final[str] = "enable_cheapest_window"
CONF_ENABLE_EXPENSIVE_WINDOW: Final[str] = "enable_expensive_window"
CONF_ENABLE_SECOND_EXPENSIVE_WINDOW: Final[str] = "enable_second_expensive_window"
CONF_ENABLE_LOW_PRICE_THRESHOLD: Final[str] = "enable_low_price_threshold"
CONF_ENABLE_HIGH_PRICE_THRESHOLD: Final[str] = "enable_high_price_threshold"
CONF_LOW_PRICE_THRESHOLD: Final[str] = "low_price_threshold"
CONF_HIGH_PRICE_THRESHOLD: Final[str] = "high_price_threshold"
CONF_USE_GROSS_PRICES: Final[str] = "use_gross_prices"
CONF_PRICE_UNIT: Final[str] = "price_unit"
CONF_PRICE_DISPLAY_PRECISION: Final[str] = "price_display_precision"

CURRENCY_PLN: Final[str] = "PLN"
UNIT_PLN_MWH: Final[str] = f"{CURRENCY_PLN}/{UnitOfEnergy.MEGA_WATT_HOUR}"
UNIT_PLN_KWH: Final[str] = f"{CURRENCY_PLN}/{UnitOfEnergy.KILO_WATT_HOUR}"
MWH_TO_KWH_DIVISOR: Final[float] = 1000.0

PRICE_INTERNAL_DECIMALS: Final[int] = 6
DEFAULT_PRICE_DISPLAY_PRECISION: Final[int] = 2
PRICE_DISPLAY_PRECISION_MIN: Final[int] = 0
PRICE_DISPLAY_PRECISION_MAX: Final[int] = PRICE_INTERNAL_DECIMALS

DEFAULT_TIME_WINDOW_START: Final[str] = "00:00"
DEFAULT_TIME_WINDOW_END: Final[str] = "00:00"
DEFAULT_WINDOW_DURATION_HOURS: Final[str] = "02:00"
DEFAULT_USE_HOURLY_PRICES: Final[bool] = False
DEFAULT_LITE_MODE: Final[bool] = False
DEFAULT_ENABLE_CHEAPEST_WINDOW: Final[bool] = True
DEFAULT_ENABLE_EXPENSIVE_WINDOW: Final[bool] = True
DEFAULT_ENABLE_SECOND_EXPENSIVE_WINDOW: Final[bool] = True
DEFAULT_ENABLE_LOW_PRICE_THRESHOLD: Final[bool] = True
DEFAULT_ENABLE_HIGH_PRICE_THRESHOLD: Final[bool] = True
DEFAULT_USE_GROSS_PRICES: Final[bool] = False

DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START: Final[str] = "06:00"
DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END: Final[str] = "10:00"
DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS: Final[str] = "02:00"
DEFAULT_LOW_PRICE_THRESHOLD: Final[float] = 0.0
DEFAULT_HIGH_PRICE_THRESHOLD: Final[float] = 1000.0
DEFAULT_PRICE_UNIT: Final[str] = UNIT_PLN_MWH

THRESHOLD_MIN: Final[float] = -3000.0
THRESHOLD_MAX: Final[float] = 3000.0
THRESHOLD_STEP: Final[float] = 0.01
THRESHOLD_STEP_KWH: Final[float] = 0.00001


def normalize_price_display_precision(raw: object) -> int:
    if isinstance(raw, bool) or not isinstance(raw, (int, float, str)):
        return DEFAULT_PRICE_DISPLAY_PRECISION
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_PRICE_DISPLAY_PRECISION
    return min(PRICE_DISPLAY_PRECISION_MAX, max(PRICE_DISPLAY_PRECISION_MIN, value))


def threshold_step_for_unit(unit: str) -> float:
    if unit == UNIT_PLN_KWH:
        return THRESHOLD_STEP_KWH
    return THRESHOLD_STEP


def threshold_selector_step_for_unit(unit: str) -> float | str:
    if unit == UNIT_PLN_KWH:
        return "any"
    return THRESHOLD_STEP