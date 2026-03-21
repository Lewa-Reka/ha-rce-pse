from __future__ import annotations

from datetime import timedelta
from typing import Final

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
CONF_LOW_PRICE_THRESHOLD: Final[str] = "low_price_threshold"
CONF_USE_GROSS_PRICES: Final[str] = "use_gross_prices"
CONF_PRICE_UNIT: Final[str] = "price_unit"

UNIT_PLN_MWH: Final[str] = "PLN/MWh"
UNIT_PLN_KWH: Final[str] = "PLN/kWh"
MWH_TO_KWH_DIVISOR: Final[float] = 1000.0

PRICE_INTERNAL_DECIMALS: Final[int] = 6
DISPLAY_PRICE_DECIMALS: Final[int] = 2

DEFAULT_TIME_WINDOW_START: Final[str] = "00:00"
DEFAULT_TIME_WINDOW_END: Final[str] = "00:00"
DEFAULT_WINDOW_DURATION_HOURS: Final[str] = "02:00"
DEFAULT_USE_HOURLY_PRICES: Final[bool] = False
DEFAULT_USE_GROSS_PRICES: Final[bool] = False

DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START: Final[str] = "06:00"
DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END: Final[str] = "10:00"
DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS: Final[str] = "02:00"
DEFAULT_LOW_PRICE_THRESHOLD: Final[float] = 0.0
DEFAULT_PRICE_UNIT: Final[str] = UNIT_PLN_MWH