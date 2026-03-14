# Sensor migration: timestamp-only time sensors

From this version onward, time-related sensors return only **timestamps** (datetime). Text-only sensors that returned times as strings (e.g. `"11:00"`) and sensors that returned time ranges as text (e.g. `"11:00 - 12:00"`) have been removed. Use the remaining timestamp sensors; in the UI they keep the same display names as the old text sensors (without the "Timestamp" prefix).

## Removed sensors

### Time range sensors (removed; use start + end timestamp sensors instead)

| entity_id                                        | EN name                            | PL name                                |
|--------------------------------------------------|------------------------------------|----------------------------------------|
| `sensor.rce_pse_today_min_price_range`           | Today Cheapest Time Range          | Najtańsze Okno Czasowe Dzisiaj         |
| `sensor.rce_pse_today_max_price_range`           | Today Most Expensive Time Range    | Najdroższe Okno Czasowe Dzisiaj        |
| `sensor.rce_pse_tomorrow_min_price_range`        | Tomorrow Cheapest Time Range       | Najtańsze Okno Czasowe Jutro           |
| `sensor.rce_pse_tomorrow_max_price_range`        | Tomorrow Most Expensive Time Range | Najdroższe Okno Czasowe Jutro          |
| `sensor.rce_pse_today_cheapest_window_range`     | Today Custom Cheapest Window       | Konfigurowalne Najtańsze Okno Dzisiaj  |
| `sensor.rce_pse_today_expensive_window_range`    | Today Custom Most Expensive Window | Konfigurowalne Najdroższe Okno Dzisiaj |
| `sensor.rce_pse_tomorrow_cheapest_window_range`  | Tomorrow Custom Cheapest Window    | Konfigurowalne Najtańsze Okno Jutro    |
| `sensor.rce_pse_tomorrow_expensive_window_range` | Custom Expensive Window Tomorrow   | Konfigurowalne Najdroższe Okno Jutro   |

### Timestamp-named sensors (removed; use sensors without timestamp in name)

| entity_id                                                  | EN name (in UI)                                       | PL name (in UI)                                               |
|------------------------------------------------------------|-------------------------------------------------------|---------------------------------------------------------------|
| `sensor.rce_pse_today_max_price_hour_start_timestamp`      | Today Max Price Hour Start Timestamp                  | Początek Godziny Maks. Ceny Dzisiaj Timestamp                 |
| `sensor.rce_pse_today_max_price_hour_end_timestamp`        | Today Max Price Hour End Timestamp                    | Koniec Godziny Maks. Ceny Dzisiaj Timestamp                   |
| `sensor.rce_pse_today_min_price_hour_start_timestamp`      | Today Min Price Hour Start Timestamp                  | Początek Godziny Min. Ceny Dzisiaj Timestamp                  |
| `sensor.rce_pse_today_min_price_hour_end_timestamp`        | Today Min Price Hour End Timestamp                    | Koniec Godziny Min. Ceny Dzisiaj Timestamp                    |
| `sensor.rce_pse_tomorrow_max_price_hour_start_timestamp`   | Tomorrow Max Price Hour Start Timestamp               | Początek Godziny Maks. Ceny Jutro Timestamp                   |
| `sensor.rce_pse_tomorrow_max_price_hour_end_timestamp`     | Tomorrow Max Price Hour End Timestamp                 | Koniec Godziny Maks. Ceny Jutro Timestamp                     |
| `sensor.rce_pse_tomorrow_min_price_hour_start_timestamp`   | Tomorrow Min Price Hour Start Timestamp               | Początek Godziny Min. Ceny Jutro Timestamp                    |
| `sensor.rce_pse_tomorrow_min_price_hour_end_timestamp`     | Tomorrow Min Price Hour End Timestamp                 | Koniec Godziny Min. Ceny Jutro Timestamp                      |
| `sensor.rce_pse_today_cheapest_window_start_timestamp`     | Today Custom Cheapest Window Start Timestamp          | Początek Konfigurowalnego Najtańszego Okna Dzisiaj Timestamp  |
| `sensor.rce_pse_today_cheapest_window_end_timestamp`       | Today Custom Cheapest Window End Timestamp            | Koniec Konfigurowalnego Najtańszego Okna Dzisiaj Timestamp    |
| `sensor.rce_pse_today_expensive_window_start_timestamp`    | Today Custom Most Expensive Window Start Timestamp    | Początek Konfigurowalnego Najdroższego Okna Dzisiaj Timestamp |
| `sensor.rce_pse_today_expensive_window_end_timestamp`      | Today Custom Most Expensive Window End Timestamp      | Koniec Konfigurowalnego Najdroższego Okna Dzisiaj Timestamp   |
| `sensor.rce_pse_tomorrow_cheapest_window_start_timestamp`  | Tomorrow Custom Cheapest Window Start Timestamp       | Początek Konfigurowalnego Najtańszego Okna Jutro Timestamp    |
| `sensor.rce_pse_tomorrow_cheapest_window_end_timestamp`    | Tomorrow Custom Cheapest Window End Timestamp         | Koniec Konfigurowalnego Najtańszego Okna Jutro Timestamp      |
| `sensor.rce_pse_tomorrow_expensive_window_start_timestamp` | Tomorrow Custom Most Expensive Window Start Timestamp | Początek Konfigurowalnego Najdroższego Okna Jutro Timestamp   |
| `sensor.rce_pse_tomorrow_expensive_window_end_timestamp`   | Tomorrow Custom Most Expensive Window End Timestamp   | Koniec Konfigurowalnego Najdroższego Okna Jutro Timestamp     |

## Replaced by sensors with timestamp values

| entity_id                                        | EN name                                     | PL name                                             |
|--------------------------------------------------|---------------------------------------------|-----------------------------------------------------|
| `sensor.rce_pse_today_max_price_hour_start`      | Today Max Price Hour Start                  | Początek Godziny Maks. Ceny Dzisiaj                 |
| `sensor.rce_pse_today_max_price_hour_end`        | Today Max Price Hour End                    | Koniec Godziny Maks. Ceny Dzisiaj                   |
| `sensor.rce_pse_today_min_price_hour_start`      | Today Min Price Hour Start                  | Początek Godziny Min. Ceny Dzisiaj                  |
| `sensor.rce_pse_today_min_price_hour_end`        | Today Min Price Hour End                    | Koniec Godziny Min. Ceny Dzisiaj                    |
| `sensor.rce_pse_tomorrow_max_price_hour_start`   | Tomorrow Max Price Hour Start               | Początek Godziny Maks. Ceny Jutro                   |
| `sensor.rce_pse_tomorrow_max_price_hour_end`     | Tomorrow Max Price Hour End                 | Koniec Godziny Maks. Ceny Jutro                     |
| `sensor.rce_pse_tomorrow_min_price_hour_start`   | Tomorrow Min Price Hour Start               | Początek Godziny Min. Ceny Jutro                    |
| `sensor.rce_pse_tomorrow_min_price_hour_end`     | Tomorrow Min Price Hour End                 | Koniec Godziny Min. Ceny Jutro                      |
| `sensor.rce_pse_today_cheapest_window_start`     | Today Custom Cheapest Window Start          | Początek Konfigurowalnego Najtańszego Okna Dzisiaj  |
| `sensor.rce_pse_today_cheapest_window_end`       | Today Custom Cheapest Window End            | Koniec Konfigurowalnego Najtańszego Okna Dzisiaj    |
| `sensor.rce_pse_today_expensive_window_start`    | Today Custom Most Expensive Window Start    | Początek Konfigurowalnego Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_today_expensive_window_end`      | Today Custom Most Expensive Window End      | Koniec Konfigurowalnego Najdroższego Okna Dzisiaj   |
| `sensor.rce_pse_tomorrow_cheapest_window_start`  | Tomorrow Custom Cheapest Window Start       | Początek Konfigurowalnego Najtańszego Okna Jutro    |
| `sensor.rce_pse_tomorrow_cheapest_window_end`    | Tomorrow Custom Cheapest Window End         | Koniec Konfigurowalnego Najtańszego Okna Jutro      |
| `sensor.rce_pse_tomorrow_expensive_window_start` | Tomorrow Custom Most Expensive Window Start | Początek Konfigurowalnego Najdroższego Okna Jutro   |
| `sensor.rce_pse_tomorrow_expensive_window_end`   | Tomorrow Custom Most Expensive Window End   | Koniec Konfigurowalnego Najdroższego Okna Jutro     |

## Migration examples

### Replacing a removed text sensor

If you used `sensor.rce_pse_today_min_price_hour_start` (text like `"11:00"`), switch to:

- **Entity:** `sensor.rce_pse_today_min_price_hour_start_timestamp` (timestamp)
- **Display:** In the UI the sensor name is "Today Min Price Hour Start" / "Początek Godziny Min. Ceny Dzisiaj". To show only the time (e.g. `11:00`) in a template or template sensor, use:

```yaml
{{ as_timestamp(states('sensor.rce_pse_today_min_price_hour_start_timestamp')) | timestamp_custom('%H:%M') }}
```

### Replacing a removed range sensor

If you used `sensor.rce_pse_today_min_price_range` (text like `"11:00 - 12:00"`), use the pair:

- `sensor.rce_pse_today_min_price_hour_start_timestamp`
- `sensor.rce_pse_today_min_price_hour_end_timestamp`

To build a range string in a template sensor:

```yaml
template:
  - sensor:
      - name: "Today Cheapest Time Range"
        state: >
          {% set start = states('sensor.rce_pse_today_min_price_hour_start_timestamp') %}
          {% set end = states('sensor.rce_pse_today_min_price_hour_end_timestamp') %}
          {% if start != 'unknown' and end != 'unknown' %}
            {{ as_timestamp(start) | timestamp_custom('%H:%M') }} - {{ as_timestamp(end) | timestamp_custom('%H:%M') }}
          {% else %}
            unknown
          {% endif %}
```

### Automations and scripts

Update any references from the removed entity IDs to the `*_timestamp` entity IDs above. The state type changes from string to datetime (ISO format in templates). Use `as_timestamp()` and `timestamp_custom()` when you need a string time or date.
