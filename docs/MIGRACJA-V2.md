# Migracja z v1.4.0 do v2.0.0

Wydanie 2.0.0 przebudowuje listę sensorów, zmienia kilka nazw encji, wprowadza Tryb Lite, Kompas Energetyczny, próg wysokiej ceny, jednostkę cen (PLN/MWh lub PLN/kWh), ceny brutto z VAT oraz okna czasowe w formacie `HH:MM` ze skokiem 15 minut. Ustawienia integracji przenoszą się automatycznie po pierwszym uruchomieniu v2 — nie trzeba usuwać ani dodawać integracji na nowo. Ręcznej poprawy wymagają automatyzacje, skrypty i dashboardy odwołujące się do usuniętych lub przemianowanych `entity_id`. Szczegółowe listy poniżej.

## Licencja

Integracja przechodzi z Apache License 2.0 na [GNU AGPL-3.0-or-later](../LICENSE). Zmiana obowiązuje od v2.0.0.

## Automatyczne przeniesienie ustawień

Po aktualizacji integracja sama zamienia stary zapis konfiguracji na nowy format:

- Godziny okien zapisane wcześniej jako pojedyncze liczby (np. `22`) zostają zamienione na `HH:MM` (np. `22:00`). Stara wartość `24` jako koniec okna zostaje ustawiona na `00:00` i w v2 oznacza koniec tego samego dnia kalendarzowego, nie północ poprzedzającej go.
- Wybrana wcześniej jednostka cen zachowuje się — po aktualizacji zobaczysz w ustawieniach etykiety `PLN/MWh` lub `PLN/kWh`.
- Nowe opcje (Tryb Lite, próg wysokiej ceny, ceny brutto, przełączniki poszczególnych okien i progów) dostają wartości domyślne: Tryb Lite wyłączony, wszystkie okna i progi włączone, ceny netto, próg wysokiej ceny `1000`.

Po aktualizacji otwórz ekran konfiguracji integracji i zweryfikuj, że zakresy okien oraz progi odpowiadają tym z v1.

## Nowe funkcje

**Tryb Lite**. Po włączeniu integracja publikuje tylko cztery sensory: „Cena”, „Cena Jutro”, „Kompas Energetyczny Dzisiaj”, „Kompas Energetyczny Jutro”. Pozostałe sensory i wszystkie binary sensory są wyłączone. Tryb przydaje się, gdy wolisz liczyć statystyki i progi samodzielnie w szablonach, korzystając z atrybutów tych czterech sensorów (pełna siatka cen dnia jest dostępna jako atrybut).

**Kompas Energetyczny**. Dwa nowe sensory: „Kompas Energetyczny Dzisiaj” i „Kompas Energetyczny Jutro”. Pokazują bieżącą rekomendację PSE dotyczącą korzystania z energii (Zalecane użytkowanie, Normalne użytkowanie, Zalecane oszczędzanie, Wymagane ograniczenie). Dane pochodzą z raportu PDGSZ publikowanego przez PSE.

**Próg wysokiej ceny**. Lustrzane odbicie progu niskiej ceny: „Cena Powyżej Progu Początek”, „Cena Powyżej Progu Koniec” oraz binary „Cena Powyżej Progu Aktywna”. Domyślna wartość progu to `1000`.

**Ceny brutto (VAT)**. Włączenie tej opcji sprawia, że integracja zwraca wszystkie ceny już z doliczonym podatkiem VAT (obecnie 23%). Jeśli do tej pory doliczałeś VAT w szablonach, po włączeniu usuń te mnożenia.

**Jednostka cen**. Możesz wybrać między `PLN/MWh` (domyślnie) a `PLN/kWh`. Przełączenie dotyczy wszystkich sensorów cenowych i progów jednocześnie. Po zmianie wykresy w recorderze pokażą „schodek” (stare wartości są w starej skali) — zaktualizuj progi niskiej i wysokiej ceny oraz porównania w automatyzacjach.

**Średnie ceny dla okien konfigurowalnych**. Sześć nowych sensorów ze średnią ceną w tanim, drogim i drugim drogim oknie — po jednym dla dziś i jutra. Pełna lista w tabeli „Nowe encje”.

**Okna w formacie `HH:MM`** ze skokiem 15 minut. Wcześniej okna ustawiało się w pełnych godzinach; teraz pokrywają pełną rozdzielczość danych PSE. Wartość `00:00` jako koniec okna oznacza koniec tego samego dnia.

## Usunięte `entity_id`

### Zakresy jako tekst

Sensory typu „11:00 - 12:00” zostały skasowane bez zamiennika w postaci pojedynczego sensora. Zastąp je parą sensorów „Początek / Koniec” (typu timestamp) i złóż tekst w szablonie lub karcie Lovelace.

| Nazwa v1 (PL)                             | entity_id v1 (PL)                                          | entity_id v1 (EN)                                 |
| ----------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- |
| Najtańsze Okno Czasowe Dzisiaj            | `sensor.rce_pse_najtansze_okno_czasowe_dzisiaj`            | `sensor.rce_pse_today_cheapest_time_range`        |
| Najdroższe Okno Czasowe Dzisiaj           | `sensor.rce_pse_najdrozsze_okno_czasowe_dzisiaj`           | `sensor.rce_pse_today_most_expensive_time_range`  |
| Najtańsze Okno Czasowe Jutro              | `sensor.rce_pse_najtansze_okno_czasowe_jutro`              | `sensor.rce_pse_tomorrow_cheapest_time_range`     |
| Najdroższe Okno Czasowe Jutro             | `sensor.rce_pse_najdrozsze_okno_czasowe_jutro`             | `sensor.rce_pse_tomorrow_most_expensive_time_range` |
| Konfigurowalne Najtańsze Okno Dzisiaj     | `sensor.rce_pse_konfigurowalne_najtansze_okno_dzisiaj`     | `sensor.rce_pse_today_custom_cheapest_window`     |
| Konfigurowalne Najdroższe Okno Dzisiaj    | `sensor.rce_pse_konfigurowalne_najdrozsze_okno_dzisiaj`    | `sensor.rce_pse_today_custom_most_expensive_window` |
| Konfigurowalne Najtańsze Okno Jutro       | `sensor.rce_pse_konfigurowalne_najtansze_okno_jutro`       | `sensor.rce_pse_tomorrow_custom_cheapest_window`  |
| Konfigurowalne Najdroższe Okno Jutro      | `sensor.rce_pse_konfigurowalne_najdrozsze_okno_jutro`      | `sensor.rce_pse_custom_expensive_window_tomorrow` |

### Duplikaty „Timestamp”

W v1 obok tekstowych sensorów godziny istniały równoległe sensory datetime z nazwą zaczynającą się od „Timestamp ” (EN: zakończoną na `_timestamp`). W v2 główne sensory okien i godzin publikują od razu pełny znacznik czasu, więc duplikaty „Timestamp” zostały usunięte.

Dotknięte sensory: 12 sztuk — po jednym starcie i końcu dla 4 okien konfigurowalnych i 4 godzin min/max (dziś i jutro). Przykłady skrajne:

| entity_id v1 (PL)                                                              | entity_id v1 (EN)                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `sensor.rce_pse_timestamp_poczatek_konfigurowalnego_najtanszego_okna_dzisiaj`  | `sensor.rce_pse_custom_cheapest_window_start_timestamp_today`            |
| `sensor.rce_pse_timestamp_koniec_konfigurowalnego_najdrozszego_okna_jutro`     | `sensor.rce_pse_custom_expensive_window_end_timestamp_tomorrow`          |
| `sensor.rce_pse_timestamp_poczatek_godziny_maks_ceny_dzisiaj`                  | `sensor.rce_pse_today_max_price_hour_start_timestamp`                    |
| `sensor.rce_pse_timestamp_koniec_godziny_min_ceny_jutro`                       | `sensor.rce_pse_tomorrow_min_price_hour_end_timestamp`                   |

Zamiennikiem jest główny sensor bez prefiksu „Timestamp” / sufiksu `_timestamp` (te same dane, teraz z pełnym znacznikiem czasu). Patrz też sekcja „Zmiana typu stanu”.

### Ceny w przyszłości

Prognozy dwu- i trzygodzinowe zostały usunięte bez zamiennika. Jeśli ich używałeś, złóż wartość samodzielnie z atrybutu `prices` sensora „Cena” lub „Cena Jutro”.

| Nazwa v1         | entity_id v1 (PL)                    | entity_id v1 (EN)                      |
| ---------------- | ------------------------------------ | -------------------------------------- |
| Cena za 2 Godziny | `sensor.rce_pse_cena_za_2_godziny`  | `sensor.rce_pse_price_in_2_hours`      |
| Cena za 3 Godziny | `sensor.rce_pse_cena_za_3_godziny`  | `sensor.rce_pse_price_in_3_hours`      |

### Cena netto prosumenta (kWh)

Sensor „Cena za kWh” został zastąpiony przez „Cena Sprzedaży Prosument”. Szczegóły w sekcji „Zmienione `entity_id`”.

### Osobne progi niskiej ceny dla dziś i jutra

Cztery sensory (start/end × dziś/jutro) zastąpiła jedna para „Cena Poniżej Progu Początek” / „Cena Poniżej Progu Koniec”. Nowa para pokazuje okno trwające albo najbliższe przyszłe, biorąc pod uwagę dane na dziś i jutro łącznie — nie trzeba już osobno pytać o jutro.

| Nazwa v1                            | entity_id v1 (PL)                                       | entity_id v1 (EN)                                       |
| ----------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Cena Poniżej Progu Początek Dzisiaj | `sensor.rce_pse_cena_ponizej_progu_poczatek_dzisiaj`    | `sensor.rce_pse_price_below_threshold_start_today`      |
| Cena Poniżej Progu Koniec Dzisiaj   | `sensor.rce_pse_cena_ponizej_progu_koniec_dzisiaj`      | `sensor.rce_pse_price_below_threshold_end_today`        |
| Cena Poniżej Progu Początek Jutro   | `sensor.rce_pse_cena_ponizej_progu_poczatek_jutro`      | `sensor.rce_pse_price_below_threshold_start_tomorrow`   |
| Cena Poniżej Progu Koniec Jutro     | `sensor.rce_pse_cena_ponizej_progu_koniec_jutro`        | `sensor.rce_pse_price_below_threshold_end_tomorrow`     |

### Binary „Cena Poniżej Progu”

W v1 obserwował tylko dzień bieżący, w v2 zwraca stan dla najbliższego okna z danych dziś+jutro. Zmienił się przy tym `entity_id`.

| Nazwa v1            | entity_id v1 (PL)                                  | entity_id v1 (EN)                                  |
| ------------------- | -------------------------------------------------- | -------------------------------------------------- |
| Cena Poniżej Progu  | `binary_sensor.rce_pse_cena_ponizej_progu`         | `binary_sensor.rce_pse_price_below_threshold`      |

Zamiennik w v2: „Cena Poniżej Progu Aktywna” — `binary_sensor.rce_pse_cena_ponizej_progu_aktywna` (PL) / `binary_sensor.rce_pse_price_below_threshold_active` (EN).

## Zmienione `entity_id`

| entity_id v1 (PL)                            | entity_id v1 (EN)                        | entity_id v2 (PL)                            | entity_id v2 (EN)                        | Uwaga                                                                                                                            |
| -------------------------------------------- | ---------------------------------------- | -------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `sensor.rce_pse_cena_nastepnej_godziny`      | `sensor.rce_pse_next_hour_price`         | `sensor.rce_pse_cena_nastepny_okres`         | `sensor.rce_pse_next_period_price`       | Długość okresu zależy od opcji „Średnie ceny godzinowe”: wyłączona = 15 min, włączona = 1 h.                                     |
| `sensor.rce_pse_cena_poprzedniej_godziny`    | `sensor.rce_pse_previous_hour_price`     | `sensor.rce_pse_cena_poprzedni_okres`        | `sensor.rce_pse_previous_period_price`   | Analogicznie do następnego okresu.                                                                                               |
| `sensor.rce_pse_cena_za_kwh`                 | `sensor.rce_pse_price_per_kwh`           | `sensor.rce_pse_cena_sprzedazy_prosument`    | `sensor.rce_pse_prosumer_selling_price`  | Ceny ujemne sprowadzane do 0, VAT 23% doliczany. W v1 zawsze w `PLN/kWh`; w v2 w globalnie wybranej jednostce (`PLN/MWh` domyślnie). Gdy włączysz „Ceny brutto” dla całej integracji, ten sensor nie dolicza VAT drugi raz. |
| `sensor.rce_pse_cena_ponizej_progu_poczatek_dzisiaj` / `_jutro` | `sensor.rce_pse_price_below_threshold_start_today` / `_tomorrow` | `sensor.rce_pse_cena_ponizej_progu_poczatek` | `sensor.rce_pse_price_below_threshold_start` | Jeden sensor dla najbliższego okna z danych dziś+jutro.                                                                          |
| `sensor.rce_pse_cena_ponizej_progu_koniec_dzisiaj` / `_jutro`   | `sensor.rce_pse_price_below_threshold_end_today` / `_tomorrow`   | `sensor.rce_pse_cena_ponizej_progu_koniec`   | `sensor.rce_pse_price_below_threshold_end`   | Jw.                                                                                                                               |
| `binary_sensor.rce_pse_cena_ponizej_progu`   | `binary_sensor.rce_pse_price_below_threshold` | `binary_sensor.rce_pse_cena_ponizej_progu_aktywna` | `binary_sensor.rce_pse_price_below_threshold_active` | Reaguje na bieżącą cenę (niezależnie od okien timestampów).                                                                      |

Niezależnie od tego kilka sensorów zachowało swoje `entity_id` z v1, ale dostało nową, krótszą nazwę wyświetlaną — na przykład „Początek Godziny Maks. Ceny Dzisiaj” zmieniło się w „Najwyższa Cena Dzisiaj Początek”, a „Początek Konfigurowalnego Najtańszego Okna Dzisiaj” w „Tanie Okno Dzisiaj Początek”. Automatyzacje odwołujące się do `entity_id` nie wymagają tu zmian; jeśli masz gdzieś zapisaną pełną polską nazwę sensora (np. w zakładce wyświetlanej na dashboardzie), zaktualizuj ją.

## Zmiana typu stanu sensorów czasowych

Sensory „Najniższa Cena Dzisiaj Początek / Koniec”, „Najwyższa Cena Dzisiaj Początek / Koniec”, „Tanie Okno Dzisiaj Początek / Koniec”, „Drogie Okno Dzisiaj Początek / Koniec” i ich odpowiedniki dla jutra oraz drugiego drogiego okna zwracały w v1 tekst w formacie `"11:00"`. W v2 są pełnymi znacznikami czasu (np. `2026-04-18T11:00:00+02:00`).

Formatowanie do „HH:MM” w szablonie:

```yaml
{{ as_timestamp(states('sensor.rce_pse_najnizsza_cena_dzisiaj_poczatek')) | timestamp_custom('%H:%M') }}
```

Składanie zakresu z pary sensorów (zamiennik usuniętych sensorów tekstowych):

```yaml
template:
  - sensor:
      - name: "Najtańsze okno dzisiaj"
        state: >
          {% set s = states('sensor.rce_pse_najnizsza_cena_dzisiaj_poczatek') %}
          {% set e = states('sensor.rce_pse_najnizsza_cena_dzisiaj_koniec') %}
          {% if s not in ['unknown','unavailable'] and e not in ['unknown','unavailable'] %}
            {{ as_timestamp(s) | timestamp_custom('%H:%M') }} - {{ as_timestamp(e) | timestamp_custom('%H:%M') }}
          {% else %}
            unknown
          {% endif %}
```

W kartach Lovelace dla tych sensorów ustaw `format: time`, żeby UI pokazał samą godzinę zamiast pełnego znacznika czasu.

## Zmiany w formularzu konfiguracji

- Wszystkie pola godzinowe (okien tanich, drogich, drugich drogich) są teraz listami wyboru `HH:MM` ze skokiem 15 minut. Koniec okna można ustawić na `00:00`, co oznacza koniec tego samego dnia kalendarzowego.
- Długość okna wybierasz w `HH:MM` od `00:15` do `24:00` (co 15 minut).
- Formularz podzielony jest na sekcje: „Podstawowe ustawienia”, „Okno tanich godzin”, „Okno drogich godzin”, „Drugie okno drogich godzin”, „Progi cenowe”.
- Każde okno i każdy próg ma własny przełącznik włączenia. Po wyłączeniu integracja nie publikuje sensorów powiązanych z tym oknem lub progiem.
- W sekcji „Podstawowe ustawienia” znajdziesz „Tryb Lite”, „Jednostka” (`PLN/MWh` / `PLN/kWh`), „Średnie ceny godzinowe”, „Ceny brutto (z VAT)”.

## Nowe `entity_id`

| Nazwa PL                                 | entity_id (PL)                                                     | entity_id (EN)                                                     | Opis                                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Kompas Energetyczny Dzisiaj              | `sensor.rce_pse_kompas_energetyczny_dzisiaj`                       | `sensor.rce_pse_energy_compass_today`                              | Rekomendacja PSE dla bieżącego kwadransa (Zalecane użytkowanie / Normalne użytkowanie / Zalecane oszczędzanie / Wymagane ograniczenie). |
| Kompas Energetyczny Jutro                | `sensor.rce_pse_kompas_energetyczny_jutro`                         | `sensor.rce_pse_energy_compass_tomorrow`                           | Jw. dla jutra (dostępne od publikacji prognozy przez PSE).                               |
| Tanie Okno Średnia Cena Dzisiaj          | `sensor.rce_pse_tanie_okno_srednia_cena_dzisiaj`                   | `sensor.rce_pse_cheap_window_avg_price_today`                      | Średnia cena w dziennym oknie tanich godzin.                                             |
| Drogie Okno Średnia Cena Dzisiaj         | `sensor.rce_pse_drogie_okno_srednia_cena_dzisiaj`                  | `sensor.rce_pse_expensive_window_avg_price_today`                  | Średnia cena w dziennym oknie drogich godzin.                                            |
| Drugie Drogie Okno Średnia Cena Dzisiaj  | `sensor.rce_pse_drugie_drogie_okno_srednia_cena_dzisiaj`           | `sensor.rce_pse_second_expensive_window_avg_price_today`           | Średnia cena w dziennym drugim oknie drogich godzin.                                     |
| Tanie Okno Średnia Cena Jutro            | `sensor.rce_pse_tanie_okno_srednia_cena_jutro`                     | `sensor.rce_pse_cheap_window_avg_price_tomorrow`                   | Jw. dla jutra.                                                                            |
| Drogie Okno Średnia Cena Jutro           | `sensor.rce_pse_drogie_okno_srednia_cena_jutro`                    | `sensor.rce_pse_expensive_window_avg_price_tomorrow`               | Jw. dla jutra.                                                                            |
| Drugie Drogie Okno Średnia Cena Jutro    | `sensor.rce_pse_drugie_drogie_okno_srednia_cena_jutro`             | `sensor.rce_pse_second_expensive_window_avg_price_tomorrow`        | Jw. dla jutra.                                                                            |
| Cena Powyżej Progu Początek              | `sensor.rce_pse_cena_powyzej_progu_poczatek`                       | `sensor.rce_pse_price_above_threshold_start`                       | Początek najbliższego okna z ceną ≥ próg wysokiej ceny (domyślnie `1000`).               |
| Cena Powyżej Progu Koniec                | `sensor.rce_pse_cena_powyzej_progu_koniec`                         | `sensor.rce_pse_price_above_threshold_end`                         | Koniec tego samego okna.                                                                  |
| Cena Powyżej Progu Aktywna (binary)      | `binary_sensor.rce_pse_cena_powyzej_progu_aktywna`                 | `binary_sensor.rce_pse_price_above_threshold_active`               | `on`, gdy bieżąca cena jest ≥ progu wysokiego.                                           |

Dla porządku — binary „Cena Poniżej Progu Aktywna” też jest nowy w sensie `entity_id`: `binary_sensor.rce_pse_cena_ponizej_progu_aktywna` (PL) / `binary_sensor.rce_pse_price_below_threshold_active` (EN). Szczegóły w sekcji „Zmienione `entity_id`”.

## Checklista po aktualizacji

- [ ] Otwórz ustawienia integracji. Przejrzyj zakresy okien (przeniesione z pełnych godzin na `HH:MM`) i długości okien.
- [ ] Zweryfikuj próg niskiej ceny i rozważ włączenie progu wysokiego (domyślnie `1000`).
- [ ] Wybierz jednostkę cen: `PLN/MWh` (domyślnie) albo `PLN/kWh`. Po zmianie zaktualizuj progi i wszystkie porównania liczbowe w automatyzacjach i szablonach.
- [ ] Zdecyduj, czy włączyć ceny brutto. Jeśli włączysz, usuń z szablonów ręczne mnożenie × 1.23.
- [ ] Rozważ Tryb Lite, jeśli wolisz liczyć okna i statystyki samodzielnie na bazie atrybutów sensorów „Cena” i „Cena Jutro”.
- [ ] Przejrzyj automatyzacje i dashboardy. Zastąp odwołania do:
  - „Najtańsze / Najdroższe Okno Czasowe Dzisiaj / Jutro” oraz „Konfigurowalne Najtańsze / Najdroższe Okno Dzisiaj / Jutro” — parami sensorów „Początek / Koniec” (typ timestamp) i szablonem łączącym je w tekst.
  - Sensorów z prefiksem „Timestamp” (PL) lub sufiksem `_timestamp` (EN) — ich głównym odpowiednikiem bez prefiksu / sufiksu (te same dane, teraz bezpośrednio typu timestamp).
  - „Cena za 2 Godziny”, „Cena za 3 Godziny” — brak zamiennika; licz z atrybutu `prices` sensora „Cena” lub „Cena Jutro”.
  - „Cena za kWh” → „Cena Sprzedaży Prosument”. Sprawdź jednostkę i VAT.
  - „Cena Poniżej Progu Początek / Koniec Dzisiaj / Jutro” → pojedyncza para „Cena Poniżej Progu Początek / Koniec”.
  - „Cena Następnej Godziny” → „Cena Następny Okres”, „Cena Poprzedniej Godziny” → „Cena Poprzedni Okres”. Pamiętaj, że długość okresu zależy teraz od opcji „Średnie ceny godzinowe”.
- [ ] Zaktualizuj szablony, które traktowały sensory min/max godzin i okien jako tekst — teraz są pełnymi znacznikami czasu, użyj `as_timestamp(...) | timestamp_custom('%H:%M')`. W Lovelace ustaw `format: time`.
- [ ] Podmień binary „Cena Poniżej Progu” na „Cena Poniżej Progu Aktywna” (nowe `entity_id`).
