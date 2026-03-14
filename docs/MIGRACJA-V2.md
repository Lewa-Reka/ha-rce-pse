# Wersja 2.0.0 – zmiany niekompatybilne wstecz i migracja

W wersji 2.0.0 wprowadzono istotne zmiany w sensorach: sensory związane z czasem zwracają wyłącznie **timestampy** (datetime). Usunięto sensory tekstowe (np. godzina jako `"11:00"`) oraz sensory zwracające zakresy jako tekst (np. `"11:00 - 12:00"`). W interfejsie nazwy wyświetlane pozostały zrozumiałe (bez dopisku "Timestamp" w nazwie).

Poniżej: co usunięto, co zastąpić i jak zaktualizować automatyzacje oraz szablony.

---

## Podsumowanie zmian

- **Czas:** tylko timestampy; usunięte sensory z samym tekstem czasu i sensory "zakresów" tekstowych.
- **Nazwy w UI:** zmienione dla części sensorów i binary sensorów (entity_id bez zmian – automatyzacje działają).
- **Cena następnego/poprzedniego okresu:** zmiana nazw i entity_id (`next_hour` → `next_period`, `previous_hour` → `previous_period`); usunięte "cena za 2/3 godziny".
- **Cena sprzedaży prosument:** nowy entity_id, jednostka z PLN/kWh na PLN/MWh.

---

## Usunięte sensory

### Sensory zakresów czasowych (zastąpienie: pary sensorów początek + koniec)

| entity_id                                        | Nazwa EN                            | Nazwa PL                                |
|--------------------------------------------------|-------------------------------------|----------------------------------------|
| `sensor.rce_pse_today_min_price_range`           | Today Cheapest Time Range           | Najtańsze Okno Czasowe Dzisiaj         |
| `sensor.rce_pse_today_max_price_range`           | Today Most Expensive Time Range     | Najdroższe Okno Czasowe Dzisiaj        |
| `sensor.rce_pse_tomorrow_min_price_range`        | Tomorrow Cheapest Time Range        | Najtańsze Okno Czasowe Jutro           |
| `sensor.rce_pse_tomorrow_max_price_range`        | Tomorrow Most Expensive Time Range  | Najdroższe Okno Czasowe Jutro          |
| `sensor.rce_pse_today_cheapest_window_range`     | Today Custom Cheapest Window        | Konfigurowalne Najtańsze Okno Dzisiaj  |
| `sensor.rce_pse_today_expensive_window_range`    | Today Custom Most Expensive Window  | Konfigurowalne Najdroższe Okno Dzisiaj |
| `sensor.rce_pse_tomorrow_cheapest_window_range`  | Tomorrow Custom Cheapest Window     | Konfigurowalne Najtańsze Okno Jutro    |
| `sensor.rce_pse_tomorrow_expensive_window_range` | Custom Expensive Window Tomorrow    | Konfigurowalne Najdroższe Okno Jutro   |

### Sensory z "Timestamp" w nazwie (zastąpienie: sensory bez "Timestamp" w nazwie, te same entity_id co wartości timestamp)

Sensory o nazwach zawierających "Timestamp" zostały usunięte; używaj sensorów o tych samych entity_id co w tabeli "Zastąpione przez sensory z wartościami timestamp" – zwracają one teraz timestamp.

---

## Zastąpienie przez sensory z wartościami timestamp

Poniższe entity_id zwracają **timestamp** (datetime). To one zastępują dawne sensory tekstowe i te z "Timestamp" w nazwie:

| entity_id                                        | Nazwa EN                     | Nazwa PL                             |
|--------------------------------------------------|------------------------------|--------------------------------------|
| `sensor.rce_pse_today_max_price_hour_start`      | Highest Price Start Today    | Początek Najwyższej Ceny Dzisiaj     |
| `sensor.rce_pse_today_max_price_hour_end`       | Highest Price End Today      | Koniec Najwyższej Ceny Dzisiaj       |
| `sensor.rce_pse_today_min_price_hour_start`     | Lowest Price Start Today     | Początek Najniższej Ceny Dzisiaj     |
| `sensor.rce_pse_today_min_price_hour_end`       | Lowest Price End Today       | Koniec Najniższej Ceny Dzisiaj       |
| `sensor.rce_pse_tomorrow_max_price_hour_start`   | Highest Price Start Tomorrow | … jutro                              |
| `sensor.rce_pse_tomorrow_max_price_hour_end`     | Highest Price End Tomorrow   | … jutro                              |
| `sensor.rce_pse_tomorrow_min_price_hour_start`   | Lowest Price Start Tomorrow  | … jutro                              |
| `sensor.rce_pse_tomorrow_min_price_hour_end`     | Lowest Price End Tomorrow    | … jutro                              |
| `sensor.rce_pse_today_cheapest_window_start`     | Cheapest Window Start Today  | Początek Najtańszego Okna Dzisiaj    |
| `sensor.rce_pse_today_cheapest_window_end`       | Cheapest Window End Today    | Koniec Najtańszego Okna Dzisiaj     |
| `sensor.rce_pse_today_expensive_window_start`    | Expensive Window Start Today | …                                    |
| `sensor.rce_pse_today_expensive_window_end`      | Expensive Window End Today   | …                                    |
| `sensor.rce_pse_tomorrow_cheapest_window_start`  | … Tomorrow                   | …                                    |
| `sensor.rce_pse_tomorrow_cheapest_window_end`    | …                            | …                                    |
| `sensor.rce_pse_tomorrow_expensive_window_start` | …                            | …                                    |
| `sensor.rce_pse_tomorrow_expensive_window_end`   | …                            | …                                    |

---

## Zmienione nazwy wyświetlane (entity_id bez zmian)

Dla poniższych encji zmieniły się tylko **nazwy w UI** (EN/PL). Entity_id pozostają takie same – automatyzacje i skrypty nie wymagają zmian.

| entity_id | EN (stara) | EN (nowa) | PL (stara) | PL (nowa) |
| --------- | ---------- | --------- | ---------- | --------- |
| sensory najniższej/najwyższej ceny (PSE) | Today Min/Max Price Hour Start/End | Lowest/Highest Price Start/End Today | Początek/Koniec Godziny Min./Maks. Ceny Dzisiaj | Początek/Koniec Najniższej/Najwyższej Ceny Dzisiaj |
| binary PSE | Today Cheapest/Most Expensive Window Active | Lowest Price / Highest Price | Aktywne Najtańsze/Najdroższe Okno Dzisiaj | Najniższa Cena / Najwyższa Cena |
| sensory konfigurowalnych okien | Today Custom Cheapest/… Window Start/End | Cheapest/Expensive Window Start/End Today | Początek/Koniec Konfig. Najtańszego/… Okna Dzisiaj | Początek/Koniec Najtańszego/Najdroższego Okna Dzisiaj |
| drugie najdroższe okno | Today Second Expensive Window Start/End | Second Expensive Window Start/End Today | … | … |
| średnie okien | Today Cheapest Window Average Price itd. | Cheapest Window Avg Today itd. | Średnia cena najtańszego okna dzisiaj | Średnia Najtańszego Okna Dzisiaj |
| okna poniżej progu | Price Below Threshold Start/End Today | Below-Threshold Window Start/End Today | Cena Poniżej Progu Początek/Koniec Dzisiaj | Początek/Koniec Okna Poniżej Progu Dzisiaj |
| binary konfig. i progu | Today Custom Cheapest Window Active itd. | Cheapest Window / Expensive Window / … | Aktywne Konfig. Najtańsze Okno Dzisiaj | Najtańsze Okno / Najdroższe Okno / Cena Poniżej Progu |

Pełna tabela mapowań nazw (stara → nowa) dla wszystkich encji jest w archiwalnym dokumencie [v2-sensors-changes.md](v2-sensors-changes.md) (wersja angielska).

---

## Sensory cen okresu (zmiana nazw i entity_id, usunięcia)

Dawne "cena następnej godziny" / "cena poprzedniej godziny" zastąpiono sensorami **okresu**. Długość okresu zależy od opcji **Ceny godzinowe**: wyłączone (domyślnie) = 15 min, włączone = 1 godzina (uśredniona cena).

### Usunięte

| entity_id | Nazwa EN | Nazwa PL |
|-----------|----------|----------|
| `sensor.rce_pse_next_2_hours_price` | Price in 2 Hours | Cena za 2 Godziny |
| `sensor.rce_pse_next_3_hours_price` | Price in 3 Hours | Cena za 3 Godziny |

W automatyzacjach i dashboardach usuń odwołania do tych entity_id lub zastąp np. sensorem "Cena następnego okresu", jeśli wystarczy następny przedział.

### Zmiana entity_id i nazwy

| Stary entity_id | Nowy entity_id | EN (stara) | EN (nowa) | PL (stara) | PL (nowa) |
|-----------------|---------------|------------|-----------|------------|-----------|
| `sensor.rce_pse_next_hour_price` | `sensor.rce_pse_next_period_price` | Next Hour Price | Next Period Price | Cena Następnej Godziny | Cena Następny Okres |
| `sensor.rce_pse_previous_hour_price` | `sensor.rce_pse_previous_period_price` | Previous Hour Price | Previous Period Price | Cena Poprzedniej Godziny | Cena Poprzedni Okres |

W skryptach, automatyzacjach i kartach zamień stare entity_id na `sensor.rce_pse_next_period_price` i `sensor.rce_pse_previous_period_price`. Jednostka (PLN/MWh) i sens danych bez zmian.

---

## Cena sprzedaży prosument (zmiana entity_id i jednostki)

Dawnej "Cena za kWh" / "Price per kWh" odpowiada teraz sensor **Cena sprzedaży prosument** w PLN/MWh (jak pozostałe ceny).

| Stary entity_id | Nowy entity_id | EN (stara) | EN (nowa) | PL (stara) | PL (nowa) |
|-----------------|----------------|------------|-----------|------------|-----------|
| `sensor.rce_pse_today_kwh_price` | `sensor.rce_pse_today_prosumer_selling_price` | Price per kWh | Prosumer Selling Price | Cena za kWh | Cena Sprzedaży Prosument |

- **Entity ID:** zamień `sensor.rce_pse_today_kwh_price` na `sensor.rce_pse_today_prosumer_selling_price`.
- **Jednostka:** z PLN/kWh na **PLN/MWh** (brak przeliczenia MWh→kWh).
- **Logika:** bez zmian – ceny ujemne → 0, mnożnik VAT 23%.

---

## Porady migracji

### Zastąpienie usuniętego sensoru tekstowego (np. godzina "11:00")

Kiedy używałeś sensora zwracającego sam czas (np. `sensor.rce_pse_today_min_price_hour_start` z tekstem `"11:00"`), przejdź na sensor zwracający timestamp (ten sam lub odpowiedni entity_id z tabel powyżej) i w szablonie wyciągnij godzinę:

```yaml
{{ as_timestamp(states('sensor.rce_pse_today_min_price_hour_start')) | timestamp_custom('%H:%M') }}
```

(Jeśli w Twojej wersji entity_id sensora czasu to nadal np. `…_timestamp`, użyj tego entity_id – w v2 to ten sam co "start"/"end" bez sufiksów w nazwie wyświetlanej.)

### Zastąpienie usuniętego sensora zakresu (np. "11:00 - 12:00")

Użyj pary sensorów początku i końca (timestamp). Przykład złożenia zakresu w sensorze szablonowym:

```yaml
template:
  - sensor:
      - name: "Najtańsze okno dzisiaj (zakres)"
        state: >
          {% set start = states('sensor.rce_pse_today_min_price_hour_start') %}
          {% set end = states('sensor.rce_pse_today_min_price_hour_end') %}
          {% if start != 'unknown' and end != 'unknown' %}
            {{ as_timestamp(start) | timestamp_custom('%H:%M') }} - {{ as_timestamp(end) | timestamp_custom('%H:%M') }}
          {% else %}
            unknown
          {% endif %}
```

### Automatyzacje i skrypty

- Dla **usuniętych** entity_id (zakresy, "2h/3h", "cena za kWh"): usuń odwołania lub zamień na nowe entity_id / szablony jak wyżej.
- Dla sensorów **tylko z nową nazwą** (bez zmiany entity_id): nic nie zmieniaj w automatyzacjach.
- Stan czasu to teraz datetime (w szablonach często w formacie ISO). Do porównań i formatowania używaj `as_timestamp()` oraz `timestamp_custom()`.

---

Dokument techniczny zmian (wersja angielska, tabele wszystkich encji): [v2-sensors-changes.md](v2-sensors-changes.md).
