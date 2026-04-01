# Sensory

Jednostka cen (PLN/MWh lub PLN/kWh) wynika z [konfiguracji](KONFIGURACJA.md) integracji; sensory cenowe używają tej samej jednostki. Wyświetlane kwoty są zaokrąglane do dwóch miejsc po przecinku.

Po włączeniu trybu Lite dostępne pozostają wyłącznie sensory **Cena** i **Cena jutro**. Wszystkie sekcje poniżej są wtedy wyłączone i nie publikują encji.

## Sensory główne

- **Cena** – aktualna cena energii (atrybut: wszystkie ceny na dziś)
- **Cena sprzedaży prosument** – rzeczywista cena sprzedaży w wybranej jednostce (ceny ujemne → 0, VAT 23%; przy PLN/kWh wartości odpowiadają podziałowi z PLN/MWh przez 1000)
- **Cena jutro** – cena z rekordów API na następny dzień (bez ukrywania danych przed ustaloną godziną)

## Sensory cen okresu

- **Cena następnego okresu** – cena za następny przedział (domyślnie 1 h przy średnich cenach godzinowych; 15 min po wyłączeniu tej opcji)
- **Cena poprzedniego okresu** – cena z poprzedniego przedziału (jak wyżej)

## Statystyki dzisiaj

- **Średnia cena dzisiaj**
- **Maksymalna cena dzisiaj**
- **Minimalna cena dzisiaj**
- **Mediana ceny dzisiaj**
- **Aktualna vs średnia dzisiaj** – procentowa różnica między aktualną a średnią ceną

## Statystyki jutro (dane na następny dzień z API)

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
- **Kompas Energetyczny Jutro** – to samo dla następnego dnia, gdy w API są rekordy PDGSZ z `business_date` jutra; stan jak przy „Cena Jutro”.

Możliwe stany (wyświetlane jako tekst w języku interfejsu):

- **Zalecane użytkowanie** – korzystny czas na używanie energii.
- **Normalne użytkowanie** – użytkowanie bez szczególnych zaleceń.
- **Zalecane oszczędzanie** – godziny szczytu, zalecane ograniczenie poboru.
- **Wymagane ograniczanie** – sytuacja trudna, wymagane ograniczenie.

Źródło: [raport PDGSZ na stronie PSE](https://raporty.pse.pl/), API `pdgsz`. Zobacz [Źródło danych](ZRODLO-DANYCH.md).

## Sensory konfigurowalnych okien czasowych

Zależą od ustawień w [Konfiguracja](KONFIGURACJA.md). Zakres przeszukiwania jest w formacie **HH:MM** (skok 15 minut); **00:00** jako **koniec** zakresu oznacza koniec tego samego dnia kalendarzowego w danych PSE, a nie północ na początku dnia. Timestamp **końca** okna odpowiada końcowi ostatniego kwadransu w wybranym bloku (nie „00:00” jako godzina tego samego dnia w błędnym sensie).

Jeśli przełącznik danego okna albo progu jest wyłączony, odpowiadające mu sensory i binary sensory nie są tworzone.

### Dzisiaj

- **Tanie Okno Dzisiaj Początek/Koniec** (timestamp)
- **Tanie Okno Dzisiaj Średnia** (jednostka jak w konfiguracji)
- **Drogie Okno Dzisiaj Początek/Koniec**, **Drogie Okno Dzisiaj Średnia**
- **Drugie Drogie Okno Dzisiaj Początek/Koniec**, **Drugie Drogie Okno Dzisiaj Średnia**

### Jutro (dane następnego dnia z API)

- Odpowiednie sensory: tanie okno, drogie okno, drugie drogie okno (początek, koniec, średnia) z **Jutro** w nazwie (np. **Tanie Okno Jutro Początek**)

### Okna poniżej i powyżej progu ceny

Przy ustawionym **progu niskiej ceny sprzedaży** (ciągłe okresy z ceną ≤ progu, kwadrans po kwadransie):

- **Cena poniżej progu Początek** – początek wybranego okna (patrz niżej)
- **Cena poniżej progu Koniec** – koniec tego samego okna

Wybór okna: jeśli aktualnie trwa któreś takie okno (w danych dzisiaj lub jutro), pokazywane jest ono; w przeciwnym razie — okno z **najwcześniejszym początkiem** spośród okien, które jeszcze się nie zaczęły, uwzględniając zarówno dzisiejsze, jak i jutrzejsze rekordy w koordynatorze. Gdy jutro nie ma jeszcze danych w API, brane są tylko okna z dzisiaj.

Przy ustawionym **progu wysokiej ceny sprzedaży** (odwrotna logika: ciągłe okresy z ceną ≥ progu):

- **Cena powyżej progu Początek/Koniec** – ta sama zasada wyboru co dla progu niskiego.

**Binary „Cena poniżej progu aktywna” / „Cena powyżej progu aktywna”** — stan `on`, gdy aktualna cena (jak w sensorze **Cena**) jest odpowiednio ≤ progowi niskiemu lub ≥ progowi wysokiemu; nie zależy od logiki okien timestampów.

Gdy nie ma trwającego ani przyszłego pasującego okna w dostępnych danych, stan odpowiednich sensorów timestamp to "unknown"; integracja pozostaje dostępna.

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
- **Cena poniżej progu aktywna** – `on`, gdy w danej chwili trwa okres z ceną ≤ progu niskiego (kwadrans po kwadransie w danych)
- **Cena powyżej progu aktywna** – `on`, gdy w danej chwili trwa okres z ceną ≥ progu wysokiego

Dla automatyzacji „na koniec okna” korzystaj ze zmiany stanu binary sensora lub z sensora timestamp końca okna, zamiast sztywnej godziny 00:00.

---

Zmiany w sensorach w wersji 2.0.0 (usunięte/zmienione encje, timestampy): [Migracja do v2.0.0](MIGRACJA-V2.md).
