from __future__ import annotations

from datetime import timedelta
from typing import Final

DOMAIN: Final[str] = "rce_pse"
SENSOR_PREFIX: Final[str] = "RCE PSE"
MANUFACTURER: Final[str] = "Lewa-Reka"
PSE_API_URL: Final[str] = "https://v2.api.raporty.pse.pl/api/rce-pln"
API_UPDATE_INTERVAL: Final[timedelta] = timedelta(minutes=30)
API_SELECT: Final[str] = "dtime,period,rce_pln,business_date,publication_ts"
API_FIRST: Final[int] = 200

TAX_RATE: Final[float] = 0.23

CONF_CHEAPEST_TIME_WINDOW_START: Final[str] = "cheapest_time_window_start"
CONF_CHEAPEST_TIME_WINDOW_END: Final[str] = "cheapest_time_window_end"
CONF_CHEAPEST_WINDOW_DURATION_HOURS: Final[str] = "cheapest_window_duration_hours"

CONF_EXPENSIVE_TIME_WINDOW_START: Final[str] = "expensive_time_window_start"
CONF_EXPENSIVE_TIME_WINDOW_END: Final[str] = "expensive_time_window_end"
CONF_EXPENSIVE_WINDOW_DURATION_HOURS: Final[str] = "expensive_window_duration_hours"

CONF_WINDOW_DURATION_HOURS: Final[str] = "window_duration_hours"

DEFAULT_TIME_WINDOW_START: Final[int] = 0  
DEFAULT_TIME_WINDOW_END: Final[int] = 24   
DEFAULT_WINDOW_DURATION_HOURS: Final[int] = 2 