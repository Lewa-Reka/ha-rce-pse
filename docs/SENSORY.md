# Sensory

## Sensory główne

- **Cena** – aktualna cena energii (atrybut: wszystkie ceny na dziś)
- **Cena sprzedaży prosument** – rzeczywista cena sprzedaży w PLN/MWh (ceny ujemne → 0, VAT 23%; bez przeliczenia MWh→kWh)
- **Cena jutro** – cena na jutro (dostępna po 14:00 CET), z atrybutem wszystkich cen na następny dzień

## Sensory cen okresu

- **Cena następnego okresu** – cena za następny przedział (15 min lub 1 h przy włączonej opcji "Ceny godzinowe")
- **Cena poprzedniego okresu** – cena z poprzedniego przedziału (15 min lub 1 h)

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

- **Początek/Koniec najniższej ceny dzisiaj** – kiedy zaczyna i kończy się okres najniższej ceny
- **Początek/Koniec najwyższej ceny dzisiaj**
- **Początek/Koniec najniższej/najwyższej ceny jutro**

Wszystkie zwracają **timestamp** (datetime). Aby pokazać tylko godzinę (np. HH:MM), użyj szablonu: `as_timestamp(...) | timestamp_custom('%H:%M')`. Szczegóły: [Migracja do v2.0.0](MIGRACJA-V2.md).

## Godziny Szczytu (PDGSZ)

Dane z raportu PSE „Godziny Szczytu” (API PDGSZ) – kiedy zalecane jest użytkowanie energii, a kiedy oszczędzanie.

- **Godziny Szczytu Dzisiaj** – stan: wartość tekstowa dla bieżącej godziny (np. „Zalecane użytkowanie”) lub brak danych jak przy sensorach „Jutro” (np. okna najniższej ceny) – wtedy stan „unknown”. Atrybuty: **records** – surowa odpowiedź API z dnia (tylko wpisy aktywne, is_active); **hourly_states** – lista 24 wpisów `{ "hour": "HH:00", "state": "klucz", "state_display": "tekst np. Zalecane użytkowanie" }` dla każdej godziny dnia.
- **Godziny Szczytu Jutro** – to samo dla następnego dnia (dostępne po 14:00 CET); stan odnosi się do godziny 00:00 jutro.

Możliwe stany (wyświetlane jako tekst w języku interfejsu):

- **Zalecane użytkowanie** – korzystny czas na używanie energii.
- **Normalne użytkowanie** – użytkowanie bez szczególnych zaleceń.
- **Zalecane oszczędzanie** – godziny szczytu, zalecane ograniczenie poboru.
- **Wymagane ograniczanie** – sytuacja trudna, wymagane ograniczenie.

Źródło: [raport PDGSZ na stronie PSE](https://raporty.pse.pl/), API `pdgsz`. Zobacz [Źródło danych](ZRODLO-DANYCH.md).

## Sensory konfigurowalnych okien czasowych

Zależą od ustawień w [Konfiguracja](KONFIGURACJA.md).

### Dzisiaj

- **Początek/Koniec najtańszego okna dzisiaj** (timestamp)
- **Średnia najtańszego okna dzisiaj** (PLN/MWh)
- **Początek/Koniec najdroższego okna dzisiaj**, **Średnia najdroższego okna dzisiaj**
- **Początek/Koniec drugiego najdroższego okna dzisiaj**, **Średnia drugiego najdroższego okna dzisiaj**

### Jutro (po 14:00 CET)

- Odpowiednie sensory: najtańsze okno, najdroższe, drugie najdroższe (początek, koniec, średnia)

### Okna poniżej progu ceny

Przy ustawionym "Progu niskiej ceny sprzedaży":

- **Początek okna poniżej progu dzisiaj** – początek pierwszego ciągłego okresu dzisiaj z ceną ≤ progu
- **Koniec okna poniżej progu dzisiaj**
- **Początek/Koniec okna poniżej progu jutro**

Gdy w danym dniu nie ma takiego okresu, stan sensorów to "unknown"; integracja pozostaje dostępna.

Sensory okien zwracają timestampy; do samej godziny użyj `timestamp_custom('%H:%M')` w szablonie.

---

## Binary sensory

Wskazują, czy **aktualny moment** jest w danym oknie cenowym (przydatne w automatyzacji i na dashboardzie).

### Okna PSE (najniższa/najwyższa cena)

- **Najniższa cena** – `on`, gdy jesteś w okresie najniższej ceny w danym dniu
- **Najwyższa cena** – `on`, gdy jesteś w okresie najwyższej ceny

### Okna konfigurowalne

- **Najtańsze okno** – `on`, gdy jesteś w skonfigurowanym najtańszym oknie
- **Najdroższe okno** – w skonfigurowanym najdroższym
- **Drugie najdroższe okno** – w drugim najdroższym
- **Cena poniżej progu** – `on`, gdy aktualny czas jest w pierwszym okresie dzisiaj z ceną ≤ progu

---

Zmiany w sensorach w wersji 2.0.0 (usunięte/zmienione encje, timestampy): [Migracja do v2.0.0](MIGRACJA-V2.md).
