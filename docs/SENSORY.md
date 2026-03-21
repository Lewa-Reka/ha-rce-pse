# Sensory

## Sensory główne

- **Cena** – aktualna cena energii (atrybut: wszystkie ceny na dziś)
- **Cena sprzedaży prosument** – rzeczywista cena sprzedaży w PLN/MWh (ceny ujemne → 0, VAT 23%; bez przeliczenia MWh→kWh)
- **Cena jutro** – cena na jutro (dostępna po 14:00 CET), z atrybutem wszystkich cen na następny dzień

## Sensory cen okresu

- **Cena następnego okresu** – cena za następny przedział (domyślnie 1 h przy średnich cenach godzinowych; 15 min po wyłączeniu tej opcji)
- **Cena poprzedniego okresu** – cena z poprzedniego przedziału (jak wyżej)

## Statystyki dzisiaj

- **Średnia cena dzisiaj**
- **Maksymalna cena dzisiaj**
- **Minimalna cena dzisiaj**
- **Mediana ceny dzisiaj**
- **Aktualna vs średnia dzisiaj** – procentowa różnica między aktualną a średnią ceną

## Statystyki jutro (po 14:00 CET)

- **Średnia cena jutro**, **Maksymalna/Minimalna/Mediana jutro**
- **Jutro vs dzisiaj (średnia)** – procentowa różnica średnich

## Godziny cen (timestampy, dane PSE)

- **Najniższa Cena Dzisiaj Początek/Koniec** – kiedy zaczyna i kończy się okres najniższej ceny
- **Najwyższa Cena Dzisiaj Początek/Koniec**
- **Najniższa/Najwyższa Cena Jutro Początek/Koniec**

Wszystkie zwracają **timestamp** (datetime). Aby pokazać tylko godzinę (np. HH:MM), użyj szablonu: `as_timestamp(...) | timestamp_custom('%H:%M')`. Szczegóły: [Migracja do v2.0.0](MIGRACJA-V2.md).

## Kompas Energetyczny (PDGSZ)

Dane z raportu PSE „Godziny Szczytu” (API PDGSZ) – kiedy zalecane jest użytkowanie energii, a kiedy oszczędzanie.

- **Kompas Energetyczny Dzisiaj** – stan: wartość tekstowa dla bieżącej godziny (np. „Zalecane użytkowanie”) lub brak danych jak przy sensorach „Jutro” (np. okna najniższej ceny) – wtedy stan „unknown”. Atrybut **values**: lista wpisów z API (tylko `dtime`, `usage_fcst`, `business_date`) z dodanymi `state` i `display_state` (klucz i tekst w języku interfejsu).
- **Kompas Energetyczny Jutro** – to samo dla następnego dnia (dostępne po 14:00 CET); stan dla aktualnej godziny, ale dnia jutrzejszego (jak sensor „Cena Jutro”).

Możliwe stany (wyświetlane jako tekst w języku interfejsu):

- **Zalecane użytkowanie** – korzystny czas na używanie energii.
- **Normalne użytkowanie** – użytkowanie bez szczególnych zaleceń.
- **Zalecane oszczędzanie** – godziny szczytu, zalecane ograniczenie poboru.
- **Wymagane ograniczanie** – sytuacja trudna, wymagane ograniczenie.

Źródło: [raport PDGSZ na stronie PSE](https://raporty.pse.pl/), API `pdgsz`. Zobacz [Źródło danych](ZRODLO-DANYCH.md).

## Sensory konfigurowalnych okien czasowych

Zależą od ustawień w [Konfiguracja](KONFIGURACJA.md). Zakres przeszukiwania jest w formacie **HH:MM** (skok 15 minut); **00:00** jako **koniec** zakresu oznacza koniec tego samego dnia kalendarzowego w danych PSE, a nie północ na początku dnia. Timestamp **końca** okna odpowiada końcowi ostatniego kwadransu w wybranym bloku (nie „00:00” jako godzina tego samego dnia w błędnym sensie).

### Dzisiaj

- **Tanie Okno Dzisiaj Początek/Koniec** (timestamp)
- **Tanie Okno Dzisiaj Średnia** (PLN/MWh)
- **Drogie Okno Dzisiaj Początek/Koniec**, **Drogie Okno Dzisiaj Średnia**
- **Drugie Drogie Okno Dzisiaj Początek/Koniec**, **Drugie Drogie Okno Dzisiaj Średnia**

### Jutro (po 14:00 CET)

- Odpowiednie sensory: tanie okno, drogie okno, drugie drogie okno (początek, koniec, średnia) z **Jutro** w nazwie (np. **Tanie Okno Jutro Początek**)

### Okna poniżej progu ceny

Przy ustawionym "Progu niskiej ceny sprzedaży":

- **Cena Poniżej Progu Dzisiaj Początek** – początek pierwszego ciągłego okresu dzisiaj z ceną ≤ progu
- **Cena Poniżej Progu Dzisiaj Koniec**
- **Cena Poniżej Progu Jutro Początek/Koniec**

Gdy w danym dniu nie ma takiego okresu, stan sensorów to "unknown"; integracja pozostaje dostępna.

Sensory okien zwracają timestampy; do samej godziny użyj `timestamp_custom('%H:%M')` w szablonie.

---

## Binary sensory

Wskazują, czy **aktualny moment** jest w danym oknie cenowym (przydatne w automatyzacji i na dashboardzie).

### Okna PSE (najniższa/najwyższa cena)

- **Najniższa cena aktywna** – `on`, gdy trwa okres najniższej ceny w danym dniu
- **Najwyższa cena aktywna** – `on`, gdy trwa okres najwyższej ceny

### Okna konfigurowalne

- **Tanie okno aktywne** – `on`, gdy trwa skonfigurowane najtańsze okno (w obrębie jednego dnia; koniec zakresu 00:00 = do końca dnia)
- **Drogie okno aktywne** – `on`, gdy trwa skonfigurowane najdroższe okno
- **Drugie drogie okno aktywne** – `on`, gdy trwa drugie najdroższe okno
- **Cena poniżej progu aktywna** – `on`, gdy trwa pierwszy ciągły okres dzisiaj z ceną ≤ progu

Dla automatyzacji „na koniec okna” korzystaj ze zmiany stanu binary sensora lub z sensora timestamp końca okna, zamiast sztywnej godziny 00:00.

---

Zmiany w sensorach w wersji 2.0.0 (usunięte/zmienione encje, timestampy): [Migracja do v2.0.0](MIGRACJA-V2.md).
