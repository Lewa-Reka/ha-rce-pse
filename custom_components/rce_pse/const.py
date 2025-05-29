"""Constants for the RCE PSE integration."""
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