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

## Renamed sensor display names

From this version, display names of some sensors and binary sensors have been changed (entity IDs are unchanged). PSE-derived periods use "Lowest/Highest Price" (e.g. Początek Najniższej Ceny); user-configured windows use "Cheapest/Expensive Window" (e.g. Początek Najtańszego Okna). For today, names end with "Dzisiaj"/"Today"; for tomorrow, "Jutro"/"Tomorrow".

Automations and scripts can keep using the same entity IDs; only the UI label changes.

| entity_id | EN (old) | EN (new) | PL (old) | PL (new) |
| --------- | -------- | -------- | -------- | -------- |
| `sensor.rce_pse_today_min_price_hour_start_timestamp` | Today Min Price Hour Start | Lowest Price Start Today | Początek Godziny Min. Ceny Dzisiaj | Początek Najniższej Ceny Dzisiaj |
| `sensor.rce_pse_today_min_price_hour_end_timestamp` | Today Min Price Hour End | Lowest Price End Today | Koniec Godziny Min. Ceny Dzisiaj | Koniec Najniższej Ceny Dzisiaj |
| `sensor.rce_pse_today_max_price_hour_start_timestamp` | Today Max Price Hour Start | Highest Price Start Today | Początek Godziny Maks. Ceny Dzisiaj | Początek Najwyższej Ceny Dzisiaj |
| `sensor.rce_pse_today_max_price_hour_end_timestamp` | Today Max Price Hour End | Highest Price End Today | Koniec Godziny Maks. Ceny Dzisiaj | Koniec Najwyższej Ceny Dzisiaj |
| `sensor.rce_pse_tomorrow_min_price_hour_start_timestamp` | Tomorrow Min Price Hour Start | Lowest Price Start Tomorrow | Początek Godziny Min. Ceny Jutro | Początek Najniższej Ceny Jutro |
| `sensor.rce_pse_tomorrow_min_price_hour_end_timestamp` | Tomorrow Min Price Hour End | Lowest Price End Tomorrow | Koniec Godziny Min. Ceny Jutro | Koniec Najniższej Ceny Jutro |
| `sensor.rce_pse_tomorrow_max_price_hour_start_timestamp` | Tomorrow Max Price Hour Start | Highest Price Start Tomorrow | Początek Godziny Maks. Ceny Jutro | Początek Najwyższej Ceny Jutro |
| `sensor.rce_pse_tomorrow_max_price_hour_end_timestamp` | Tomorrow Max Price Hour End | Highest Price End Tomorrow | Koniec Godziny Maks. Ceny Jutro | Koniec Najwyższej Ceny Jutro |
| `binary_sensor.rce_pse_today_min_price_window_active` | Today Cheapest Window Active | Lowest Price | Aktywne Najtańsze Okno Dzisiaj | Najniższa Cena |
| `binary_sensor.rce_pse_today_max_price_window_active` | Today Most Expensive Window Active | Highest Price | Aktywne Najdroższe Okno Dzisiaj | Najwyższa Cena |
| `sensor.rce_pse_today_cheapest_window_start_timestamp` | Today Custom Cheapest Window Start | Cheapest Window Start Today | Początek Konfigurowalnego Najtańszego Okna Dzisiaj | Początek Najtańszego Okna Dzisiaj |
| `sensor.rce_pse_today_cheapest_window_end_timestamp` | Today Custom Cheapest Window End | Cheapest Window End Today | Koniec Konfigurowalnego Najtańszego Okna Dzisiaj | Koniec Najtańszego Okna Dzisiaj |
| `sensor.rce_pse_today_expensive_window_start_timestamp` | Today Custom Most Expensive Window Start | Expensive Window Start Today | Początek Konfigurowalnego Najdroższego Okna Dzisiaj | Początek Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_today_expensive_window_end_timestamp` | Today Custom Most Expensive Window End | Expensive Window End Today | Koniec Konfigurowalnego Najdroższego Okna Dzisiaj | Koniec Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_tomorrow_cheapest_window_start_timestamp` | Tomorrow Custom Cheapest Window Start | Cheapest Window Start Tomorrow | Początek Konfigurowalnego Najtańszego Okna Jutro | Początek Najtańszego Okna Jutro |
| `sensor.rce_pse_tomorrow_cheapest_window_end_timestamp` | Tomorrow Custom Cheapest Window End | Cheapest Window End Tomorrow | Koniec Konfigurowalnego Najtańszego Okna Jutro | Koniec Najtańszego Okna Jutro |
| `sensor.rce_pse_tomorrow_expensive_window_start_timestamp` | Tomorrow Custom Most Expensive Window Start | Expensive Window Start Tomorrow | Początek Konfigurowalnego Najdroższego Okna Jutro | Początek Najdroższego Okna Jutro |
| `sensor.rce_pse_tomorrow_expensive_window_end_timestamp` | Tomorrow Custom Most Expensive Window End | Expensive Window End Tomorrow | Koniec Konfigurowalnego Najdroższego Okna Jutro | Koniec Najdroższego Okna Jutro |
| `sensor.rce_pse_today_second_expensive_window_start` | Today Second Expensive Window Start | Second Expensive Window Start Today | Początek Drugiego Najdroższego Okna Dzisiaj | Początek Drugiego Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_today_second_expensive_window_end` | Today Second Expensive Window End | Second Expensive Window End Today | Koniec Drugiego Najdroższego Okna Dzisiaj | Koniec Drugiego Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_tomorrow_second_expensive_window_start` | Tomorrow Second Expensive Window Start | Second Expensive Window Start Tomorrow | Początek Drugiego Najdroższego Okna Jutro | Początek Drugiego Najdroższego Okna Jutro |
| `sensor.rce_pse_tomorrow_second_expensive_window_end` | Tomorrow Second Expensive Window End | Second Expensive Window End Tomorrow | Koniec Drugiego Najdroższego Okna Jutro | Koniec Drugiego Najdroższego Okna Jutro |
| `sensor.rce_pse_today_cheapest_window_avg_price` | Today Cheapest Window Average Price | Cheapest Window Avg Today | Średnia cena najtańszego okna dzisiaj | Średnia Najtańszego Okna Dzisiaj |
| `sensor.rce_pse_today_expensive_window_avg_price` | Today Most Expensive Window Average Price | Expensive Window Avg Today | Średnia cena najdroższego okna dzisiaj | Średnia Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_today_second_expensive_window_avg_price` | Today Second Expensive Window Average Price | Second Expensive Window Avg Today | Średnia cena drugiego najdroższego okna dzisiaj | Średnia Drugiego Najdroższego Okna Dzisiaj |
| `sensor.rce_pse_tomorrow_cheapest_window_avg_price` | Tomorrow Cheapest Window Average Price | Cheapest Window Avg Tomorrow | Średnia cena najtańszego okna jutro | Średnia Najtańszego Okna Jutro |
| `sensor.rce_pse_tomorrow_expensive_window_avg_price` | Tomorrow Most Expensive Window Average Price | Expensive Window Avg Tomorrow | Średnia cena najdroższego okna jutro | Średnia Najdroższego Okna Jutro |
| `sensor.rce_pse_tomorrow_second_expensive_window_avg_price` | Tomorrow Second Expensive Window Average Price | Second Expensive Window Avg Tomorrow | Średnia cena drugiego najdroższego okna jutro | Średnia Drugiego Najdroższego Okna Jutro |
| `sensor.rce_pse_today_low_price_threshold_window_start` | Price Below Threshold Start Today | Below-Threshold Window Start Today | Cena Poniżej Progu Początek Dzisiaj | Początek Okna Poniżej Progu Dzisiaj |
| `sensor.rce_pse_today_low_price_threshold_window_end` | Price Below Threshold End Today | Below-Threshold Window End Today | Cena Poniżej Progu Koniec Dzisiaj | Koniec Okna Poniżej Progu Dzisiaj |
| `sensor.rce_pse_tomorrow_low_price_threshold_window_start` | Price Below Threshold Start Tomorrow | Below-Threshold Window Start Tomorrow | Cena Poniżej Progu Początek Jutro | Początek Okna Poniżej Progu Jutro |
| `sensor.rce_pse_tomorrow_low_price_threshold_window_end` | Price Below Threshold End Tomorrow | Below-Threshold Window End Tomorrow | Cena Poniżej Progu Koniec Jutro | Koniec Okna Poniżej Progu Jutro |
| `binary_sensor.rce_pse_today_cheapest_window_active` | Today Custom Cheapest Window Active | Cheapest Window | Aktywne Konfigurowalne Najtańsze Okno Dzisiaj | Najtańsze Okno |
| `binary_sensor.rce_pse_today_expensive_window_active` | Today Custom Most Expensive Window Active | Expensive Window | Aktywne Konfigurowalne Najdroższe Okno Dzisiaj | Najdroższe Okno |
| `binary_sensor.rce_pse_today_second_expensive_window_active` | Today Second Expensive Window Active | Second Expensive Window | Aktywne Drugie Najdroższe Okno Dzisiaj | Drugie Najdroższe Okno |
| `binary_sensor.rce_pse_today_low_price_threshold_window_active` | Price Below Threshold | Price Below-Threshold | Cena Poniżej Progu | Cena Poniżej Progu |

## Period price sensors (renamed and removed)

Sensors for "next hour", "previous hour", and "price in 2/3 hours" have been replaced by period-based sensors. A period is one 15-minute PSE slot (not necessarily one hour).

### Removed sensors

| entity_id                       | EN name            | PL name           |
|---------------------------------|--------------------|-------------------|
| `sensor.rce_pse_next_2_hours_price`  | Price in 2 Hours   | Cena za 2 Godziny |
| `sensor.rce_pse_next_3_hours_price`  | Price in 3 Hours   | Cena za 3 Godziny |

Update automations, scripts, and dashboards: remove references to these entity IDs or use the next-period sensor if you only need the immediate next period.

### Renamed sensors (entity_id and display name changed)

| Old entity_id                    | New entity_id                     | EN name (old)         | EN name (new)           | PL name (old)           | PL name (new)        |
|----------------------------------|-----------------------------------|----------------------|-------------------------|-------------------------|----------------------|
| `sensor.rce_pse_next_hour_price`    | `sensor.rce_pse_next_period_price`    | Next Hour Price      | Next Period Price       | Cena Następnej Godziny  | Cena Następny Okres  |
| `sensor.rce_pse_previous_hour_price` | `sensor.rce_pse_previous_period_price` | Previous Hour Price  | Previous Period Price   | Cena Poprzedniej Godziny| Cena Poprzedni Okres |

- **Entity ID:** Update automations, scripts, and dashboards from the old entity IDs to `sensor.rce_pse_next_period_price` and `sensor.rce_pse_previous_period_price`.
- **Semantics:** "Next period" is the next 15-minute slot; "previous period" is the previous 15-minute slot. Values and units (PLN/MWh) are unchanged.

## Prosumer selling price sensor (renamed, entity_id and unit changed)

The former "Cena za kWh" / "Price per kWh" sensor has been renamed and now returns values in PLN/MWh like other price sensors.

| Old entity_id | New entity_id | EN name (old) | EN name (new) | PL name (old) | PL name (new) |
|---------------|---------------|---------------|---------------|---------------|---------------|
| `sensor.rce_pse_today_kwh_price` | `sensor.rce_pse_today_prosumer_selling_price` | Price per kWh | Prosumer Selling Price | Cena za kWh | Cena Sprzedaży Prosument |

- **Entity ID:** Update automations, scripts, and dashboards from `sensor.rce_pse_today_kwh_price` to `sensor.rce_pse_today_prosumer_selling_price`.
- **Unit:** Changed from PLN/kWh to PLN/MWh. The sensor no longer converts MWh to kWh; it returns the price in PLN/MWh like other price sensors.
- **Logic:** Unchanged – negative prices are still converted to zero (`rce_pln_neg_to_zero`) and the 23% VAT multiplier (1.23) is still applied.

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

For the **renamed** sensors and binary sensors above: entity IDs are unchanged, so automations and scripts do not need updates; only the display name in the UI changes.
