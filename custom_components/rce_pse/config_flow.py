from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult, section
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_USE_HOURLY_PRICES,
    CONF_LOW_PRICE_THRESHOLD,
    CONF_USE_GROSS_PRICES,
    CONF_PRICE_UNIT,
    DEFAULT_PRICE_UNIT,
    UNIT_PLN_KWH,
    UNIT_PLN_MWH,
    DEFAULT_TIME_WINDOW_START,
    DEFAULT_TIME_WINDOW_END,
    DEFAULT_WINDOW_DURATION_HOURS,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
    DEFAULT_USE_HOURLY_PRICES,
    DEFAULT_USE_GROSS_PRICES,
    DEFAULT_LOW_PRICE_THRESHOLD,
)
from .time_window import (
    duration_minutes_from_hhmm,
    is_search_end_end_of_day,
    is_valid_duration_hhmm,
    is_valid_quarter_step,
    minutes_from_midnight,
    normalize_hhmm,
)

_LOGGER = logging.getLogger(__name__)

SECTION_PRICING = "pricing"
SECTION_CHEAPEST_WINDOW = "cheapest_window"
SECTION_EXPENSIVE_WINDOW = "expensive_window"
SECTION_SECOND_EXPENSIVE_WINDOW = "second_expensive_window"

SECTION_KEYS = frozenset(
    {
        SECTION_PRICING,
        SECTION_CHEAPEST_WINDOW,
        SECTION_EXPENSIVE_WINDOW,
        SECTION_SECOND_EXPENSIVE_WINDOW,
    }
)

TIME_KEYS = (
    CONF_CHEAPEST_TIME_WINDOW_START,
    CONF_CHEAPEST_TIME_WINDOW_END,
    CONF_CHEAPEST_WINDOW_DURATION_HOURS,
    CONF_EXPENSIVE_TIME_WINDOW_START,
    CONF_EXPENSIVE_TIME_WINDOW_END,
    CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
)

WINDOW_END_KEYS = frozenset(
    {
        CONF_CHEAPEST_TIME_WINDOW_END,
        CONF_EXPENSIVE_TIME_WINDOW_END,
        CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
    }
)


def migrate_price_unit_in_mapping(data: dict[str, Any]) -> dict[str, Any]:
    out = dict(data)
    if CONF_PRICE_UNIT not in out:
        return out
    v = out[CONF_PRICE_UNIT]
    if v == "pln_kwh":
        out[CONF_PRICE_UNIT] = UNIT_PLN_KWH
    elif v == "pln_mwh":
        out[CONF_PRICE_UNIT] = UNIT_PLN_MWH
    return out


def migrate_legacy_time_values(data: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(data)
    for key in TIME_KEYS:
        if key not in out:
            continue
        v = out[key]
        if isinstance(v, int):
            if key in WINDOW_END_KEYS and v == 24:
                out[key] = "00:00"
            else:
                out[key] = f"{int(v):02d}:00"
        elif isinstance(v, str) and v.isdigit():
            iv = int(v)
            if key in WINDOW_END_KEYS and iv == 24:
                out[key] = "00:00"
            else:
                out[key] = f"{iv:02d}:00"
    return out


def _start_time_select_options() -> list[dict[str, str]]:
    return [
        {"value": f"{h:02d}:{m:02d}", "label": f"{h:02d}:{m:02d}"}
        for h in range(24)
        for m in (0, 15, 30, 45)
    ]


def _end_time_select_options() -> list[dict[str, str]]:
    opts: list[dict[str, str]] = [{"value": "00:00", "label": "00:00"}]
    for h in range(24):
        for m in (0, 15, 30, 45):
            if h == 0 and m == 0:
                continue
            v = f"{h:02d}:{m:02d}"
            opts.append({"value": v, "label": v})
    return opts


def _duration_select_options() -> list[dict[str, str]]:
    opts: list[dict[str, str]] = []
    for h in range(24):
        for m in (0, 15, 30, 45):
            if h == 0 and m == 0:
                continue
            v = f"{h:02d}:{m:02d}"
            opts.append({"value": v, "label": v})
    opts.append({"value": "24:00", "label": "24:00"})
    return opts


def _flatten_rce_user_input(user_input: dict[str, Any]) -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in user_input.items():
        if key in SECTION_KEYS and isinstance(value, dict):
            flat.update(value)
        else:
            flat[key] = value
    return flat


def _coerce_time_values(flat: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(flat)
    for key in TIME_KEYS:
        if key not in out:
            continue
        v = out[key]
        if isinstance(v, int):
            if key in WINDOW_END_KEYS and v == 24:
                out[key] = "00:00"
            else:
                out[key] = f"{int(v):02d}:00"
        elif hasattr(v, "hour") and hasattr(v, "minute"):
            h = int(v.hour)
            m = int(v.minute)
            if h == 24:
                out[key] = "24:00"
            else:
                out[key] = f"{h:02d}:{m:02d}"
        else:
            out[key] = normalize_hhmm(v)
    return out


def _search_span_minutes(start_hhmm: str, end_hhmm: str) -> int:
    sm = minutes_from_midnight(normalize_hhmm(start_hhmm))
    ne = normalize_hhmm(end_hhmm)
    if is_search_end_end_of_day(ne):
        return 24 * 60 - sm
    em = minutes_from_midnight(ne)
    return em - sm


def _time_window_errors(flat: Mapping[str, Any]) -> dict[str, str]:
    pairs = (
        (
            flat.get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            flat.get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            flat.get(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
        ),
        (
            flat.get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            flat.get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            flat.get(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
        ),
        (
            flat.get(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
            ),
            flat.get(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
            ),
            flat.get(
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
            ),
        ),
    )
    for start, end, duration in pairs:
        ns = normalize_hhmm(str(start))
        ne = normalize_hhmm(str(end))
        if not is_valid_quarter_step(ns):
            return {"base": "invalid_time_window"}
        if not is_valid_quarter_step(ne):
            return {"base": "invalid_time_window"}
        if not is_valid_duration_hhmm(str(duration)):
            return {"base": "invalid_duration"}
        if not is_search_end_end_of_day(ne) and minutes_from_midnight(ns) >= minutes_from_midnight(ne):
            return {"base": "invalid_time_window"}
        span = _search_span_minutes(ns, ne)
        dm = duration_minutes_from_hhmm(str(duration))
        if dm > span:
            return {"base": "duration_exceeds_search_window"}
    return {}


def _price_unit_select_options() -> list[dict[str, str]]:
    return [
        {"value": UNIT_PLN_MWH, "label": UNIT_PLN_MWH},
        {"value": UNIT_PLN_KWH, "label": UNIT_PLN_KWH},
    ]

def _rce_form_schema(current_data: Mapping[str, Any]) -> vol.Schema:
    def _get(key: str, default: Any) -> Any:
        v = current_data.get(key, default)
        if isinstance(v, int) and key in TIME_KEYS:
            if key.endswith("_end") and v == 24:
                return "00:00"
            return f"{int(v):02d}:00"
        if key in TIME_KEYS and v is not None:
            if isinstance(v, dict):
                return normalize_hhmm(v)
            return normalize_hhmm(str(v))
        return v

    pricing_inner = vol.Schema(
        {
            vol.Optional(
                CONF_USE_HOURLY_PRICES, default=_get(CONF_USE_HOURLY_PRICES, DEFAULT_USE_HOURLY_PRICES)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Optional(
                CONF_USE_GROSS_PRICES, default=_get(CONF_USE_GROSS_PRICES, DEFAULT_USE_GROSS_PRICES)
            ): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            vol.Required(
                CONF_PRICE_UNIT, default=_get(CONF_PRICE_UNIT, DEFAULT_PRICE_UNIT)
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_price_unit_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_LOW_PRICE_THRESHOLD, default=_get(CONF_LOW_PRICE_THRESHOLD, DEFAULT_LOW_PRICE_THRESHOLD)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=-3000,
                    max=3000,
                    step=0.01,
                    mode=selector.NumberSelectorMode.BOX,
                    unit_of_measurement="PLN",
                )
            )
        }
    )

    cheapest_inner = vol.Schema(
        {
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_START,
                default=_get(CONF_CHEAPEST_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_start_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_CHEAPEST_TIME_WINDOW_END,
                default=_get(CONF_CHEAPEST_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_end_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_CHEAPEST_WINDOW_DURATION_HOURS,
                default=_get(CONF_CHEAPEST_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_duration_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )

    expensive_inner = vol.Schema(
        {
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_START,
                default=_get(CONF_EXPENSIVE_TIME_WINDOW_START, DEFAULT_TIME_WINDOW_START),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_start_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_TIME_WINDOW_END,
                default=_get(CONF_EXPENSIVE_TIME_WINDOW_END, DEFAULT_TIME_WINDOW_END),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_end_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_EXPENSIVE_WINDOW_DURATION_HOURS,
                default=_get(CONF_EXPENSIVE_WINDOW_DURATION_HOURS, DEFAULT_WINDOW_DURATION_HOURS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_duration_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )

    second_expensive_inner = vol.Schema(
        {
            vol.Required(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                default=_get(
                    CONF_SECOND_EXPENSIVE_TIME_WINDOW_START,
                    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_START,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_start_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                default=_get(
                    CONF_SECOND_EXPENSIVE_TIME_WINDOW_END,
                    DEFAULT_SECOND_EXPENSIVE_TIME_WINDOW_END,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_end_time_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                default=_get(
                    CONF_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                    DEFAULT_SECOND_EXPENSIVE_WINDOW_DURATION_HOURS,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_duration_select_options(),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
        }
    )

    return vol.Schema(
        {
            vol.Required(SECTION_PRICING): section(pricing_inner, {"collapsed": False}),
            vol.Required(SECTION_CHEAPEST_WINDOW): section(cheapest_inner, {"collapsed": True}),
            vol.Required(SECTION_EXPENSIVE_WINDOW): section(expensive_inner, {"collapsed": True}),
            vol.Required(SECTION_SECOND_EXPENSIVE_WINDOW): section(
                second_expensive_inner, {"collapsed": True}
            ),
        }
    )


CONFIG_SCHEMA = _rce_form_schema({})


class RCEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]

    VERSION = 2
    MINOR_VERSION = 0
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    def async_get_options_flow(config_entry):
        return RCEOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        _LOGGER.debug("Starting RCE PSE config flow")

        if self._async_current_entries():
            _LOGGER.debug("RCE PSE integration already configured, aborting")
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}

        if user_input is not None:
            flat = _coerce_time_values(_flatten_rce_user_input(user_input))
            errors = _time_window_errors(flat)
            if not errors:
                _LOGGER.debug("Creating RCE PSE config entry with options: %s", flat)
                await self.async_set_unique_id("rce_pse")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="RCE PSE", data=flat)

        _LOGGER.debug("Showing RCE PSE configuration form")
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )


class RCEOptionsFlow(config_entries.OptionsFlow):

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            flat = _coerce_time_values(_flatten_rce_user_input(user_input))
            errors = _time_window_errors(flat)
            if not errors:
                _LOGGER.debug("Updating RCE PSE options: %s", flat)
                return self.async_create_entry(title="", data=flat)

        current_data = self.config_entry.options if self.config_entry.options else self.config_entry.data
        options_schema = _rce_form_schema(current_data)

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
        )
