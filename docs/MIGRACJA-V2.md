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

### Tekstowe sensory zakresów czasowych (można je zastąpić: pary sensorów początek + koniec)

| entity_id                                         | Nazwa EN                             | Nazwa PL                                 |
| ------------------------------------------------- | ------------------------------------ | ---------------------------------------- |
| `sensor.rce_pse_today_min_price_range`            | Today Cheap Time Range            | Najtańsze Okno Czasowe Dzisiaj           |
| `sensor.rce_pse_today_max_price_range`            | Today Most Expensive Time Range      | Drogie Okno Czasowe Dzisiaj          |
| `sensor.rce_pse_tomorrow_min_price_range`         | Tomorrow Cheap Time Range         | Najtańsze Okno Czasowe Jutro             |
| `sensor.rce_pse_tomorrow_max_price_range`         | Tomorrow Most Expensive Time Range   | Drogie Okno Czasowe Jutro            |
| `sensor.rce_pse_today_cheapest_window_range`      | Today Custom Cheap Window         | Konfigurowalne Najtańsze Okno Dzisiaj    |
| `sensor.rce_pse_today_expensive_window_range`     | Today Custom Most Expensive Window   | Konfigurowalne Drogie Okno Dzisiaj   |
| `sensor.rce_pse_tomorrow_cheapest_window_range`   | Tomorrow Custom Cheap Window      | Konfigurowalne Najtańsze Okno Jutro      |
| `sensor.rce_pse_tomorrow_expensive_window_range`  | Custom Expensive Window Tomorrow     | Konfigurowalne Drogie Okno Jutro     |

### Sensory z "Timestamp" w nazwie (zastąpienie: sensory bez "Timestamp" w nazwie, te same entity_id co wartości timestamp)

Sensory o nazwach zawierających "Timestamp" zostały usunięte; używaj sensorów o tych samych entity_id co w tabeli "Zastąpione przez sensory z wartościami timestamp" – zwracają one teraz timestamp.

---

## Zastąpienie przez sensory z wartościami timestamp

Poniższe entity_id zwracają **timestamp** (datetime). To one zastępują dawne sensory tekstowe i te z "Timestamp" w nazwie:

| entity_id                                         | Nazwa EN                        | Nazwa PL                              |
| ------------------------------------------------- | ------------------------------- | ------------------------------------- |
| `sensor.rce_pse_today_max_price_hour_start`       | Highest Price Today Start       | Najwyższa Cena Dzisiaj Początek       |
| `sensor.rce_pse_today_max_price_hour_end`         | Highest Price Today End         | Najwyższa Cena Dzisiaj Koniec         |
| `sensor.rce_pse_today_min_price_hour_start`       | Lowest Price Today Start        | Najniższa Cena Dzisiaj Początek       |
| `sensor.rce_pse_today_min_price_hour_end`         | Lowest Price Today End          | Najniższa Cena Dzisiaj Koniec         |
| `sensor.rce_pse_tomorrow_max_price_hour_start`    | Highest Price Tomorrow Start    | Najwyższa Cena Jutro Początek         |
| `sensor.rce_pse_tomorrow_max_price_hour_end`      | Highest Price Tomorrow End      | Najwyższa Cena Jutro Koniec           |
| `sensor.rce_pse_tomorrow_min_price_hour_start`    | Lowest Price Tomorrow Start     | Najniższa Cena Jutro Początek         |
| `sensor.rce_pse_tomorrow_min_price_hour_end`      | Lowest Price Tomorrow End       | Najniższa Cena Jutro Koniec           |
| `sensor.rce_pse_today_cheapest_window_start`      | Cheap Window Today Start     | Tanie Okno Dzisiaj Początek           |
| `sensor.rce_pse_today_cheapest_window_end`        | Cheap Window Today End       | Tanie Okno Dzisiaj Koniec             |
| `sensor.rce_pse_today_expensive_window_start`     | Expensive Window Today Start | Drogie Okno Dzisiaj Początek    |
| `sensor.rce_pse_today_expensive_window_end`       | Expensive Window Today End | Drogie Okno Dzisiaj Koniec        |
| `sensor.rce_pse_tomorrow_cheapest_window_start`   | Cheap Window Tomorrow Start  | Tanie Okno Jutro Początek             |
| `sensor.rce_pse_tomorrow_cheapest_window_end`     | Cheap Window Tomorrow End    | Tanie Okno Jutro Koniec               |
| `sensor.rce_pse_tomorrow_expensive_window_start`  | Expensive Window Tomorrow Start | Drogie Okno Jutro Początek     |
| `sensor.rce_pse_tomorrow_expensive_window_end`    | Expensive Window Tomorrow End | Drogie Okno Jutro Koniec        |

---

## Zmienione nazwy wyświetlane (entity_id bez zmian)

Dla poniższych encji zmieniły się tylko **nazwy w UI** (EN/PL). Entity_id pozostają takie same – automatyzacje i skrypty nie wymagają zmian.

| entity_id                       | EN (stara)                          | EN (nowa)                        | PL (stara)                                  | PL (nowa)                                    |
| ------------------------------- | ----------------------------------- | -------------------------------- | ------------------------------------------- | -------------------------------------------- |
| sensory najniższej/najwyższej   | Today Min/Max Price Hour Start/End  | Lowest/Highest Price Today/Tomorrow Start/End   | Początek/Koniec Godziny Min./Maks. Ceny     | Najniższa/Najwyższa Cena Dzisiaj/Jutro Początek/Koniec     |
| binary PSE                      | Today Cheap/Most Expensive       | Lowest Price Active / Highest Price Active     | Aktywne Najtańsze/Najdroższe Okno Dzisiaj   | Najniższa Cena Aktywna / Najwyższa Cena Aktywna              |
| sensory konfigurowalnych okien  | Today Custom Cheap/… Window      | Cheap/Expensive Window Today Start | Początek/Koniec Konfig. Najtańszego/… Okna | Tanie/Drogie Okno Dzisiaj Początek/Koniec        |
| drugie drogie okno              | Today Second Expensive Window       | Second Expensive Window Today Start | …                                        | Drugie Drogie Okno Dzisiaj Początek/Koniec       |
| średnie okien                   | Today Cheap Window Avg Price     | Cheap Window Today Average itd. | Średnia cena najtańszego okna dzisiaj     | Tanie/Drogie Okno Dzisiaj Średnia        |
| okna poniżej progu              | Price Below Threshold Start/End     | Below-Threshold Price Today Start     | Cena Poniżej Progu Początek/Koniec Dzisiaj  | Cena Poniżej Progu Dzisiaj Początek/Koniec   |
| sensory binarne                 | Today Custom Cheap Window itd.   | Cheap Window Active / …    | Aktywne Najtańsze Okno Dzisiaj              | Tanie Okno Aktywne / Drogie Okno Aktywne / Cena Poniżej Progu Aktywna   |

---

## Sensory cen okresu (zmiana nazw i entity_id, usunięcia)

Dawne "cena następnej godziny" / "cena poprzedniej godziny" zastąpiono sensorami **okresu**. Długość okresu zależy od opcji **średnich cen godzinowych**: wyłączone = 15 min, włączone = 1 godzina (uśredniona cena). Przy **nowej** konfiguracji integracji ta opcja jest obecnie domyślnie włączona; starsze wpisy zachowują zapisane wartości (w czasie migracji do v2 domyślnie bywało wyłączenie i okres 15 min).

### Usunięte

| entity_id                           | Nazwa EN          | Nazwa PL           |
| ----------------------------------- | ----------------- | ------------------ |
| `sensor.rce_pse_next_2_hours_price` | Price in 2 Hours  | Cena za 2 Godziny  |
| `sensor.rce_pse_next_3_hours_price` | Price in 3 Hours  | Cena za 3 Godziny  |

W automatyzacjach i dashboardach usuń odwołania do tych entity_id lub zastąp np. sensorem "Cena następnego okresu", jeśli wystarczy następny przedział.

### Zmiana entity_id i nazwy

| Stary entity_id                      | Nowy entity_id                         | EN (stara)           | EN (nowa)             | PL (stara)               | PL (nowa)             |
| ------------------------------------ | -------------------------------------- | -------------------- | --------------------- | ------------------------ | --------------------- |
| `sensor.rce_pse_next_hour_price`     | `sensor.rce_pse_next_period_price`     | Next Hour Price      | Next Period Price     | Cena Następnej Godziny   | Cena Następny Okres   |
| `sensor.rce_pse_previous_hour_price` | `sensor.rce_pse_previous_period_price` | Previous Hour Price  | Previous Period Price | Cena Poprzedniej Godziny | Cena Poprzedni Okres  |

W skryptach, automatyzacjach i kartach zamień stare entity_id na `sensor.rce_pse_next_period_price` i `sensor.rce_pse_previous_period_price`. Jednostka (PLN/MWh) i sens danych bez zmian.

---

## Cena sprzedaży prosument (zmiana entity_id i jednostki)

Dawnej "Cena za kWh" / "Price per kWh" odpowiada teraz sensor **Cena sprzedaży prosument** w PLN/MWh (jak pozostałe ceny).

| Stary entity_id                   | Nowy entity_id                               | EN (stara)       | EN (nowa)              | PL (stara)   | PL (nowa)                 |
| --------------------------------- | -------------------------------------------- | ---------------- | ---------------------- | ------------ | ------------------------- |
| `sensor.rce_pse_today_kwh_price`  | `sensor.rce_pse_today_prosumer_selling_price`| Price per kWh    | Prosumer Selling Price | Cena za kWh  | Cena Sprzedaży Prosument  |

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

