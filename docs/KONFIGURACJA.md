# Konfiguracja

Po zainstalowaniu integracji możesz ją skonfigurować w interfejsie Home Assistant. Ustawienia są pogrupowane w sekcje (ceny, okna najtańszych i najdroższych godzin, drugi szczyt cenowy), żeby łatwiej było nawigować po formularzu.

## Opcje konfiguracji

### Ustawienia najtańszych godzin

Określają, w jakim przedziale szukać najbardziej ekonomicznych okresów. Wartości są w formacie **HH:MM** ze skokiem **15 minut** (00, 15, 30, 45). Zakres przeszukiwania dotyczy **jednego dnia kalendarzowego** — nie da się ustawić jednego ciągłego okna „od wieczora do rana następnego dnia” (np. 22:00–06:00); takie scenariusze rozwiązuj dwoma osobnymi zakresami lub inną logiką w automatyzacji.

- **Początek przeszukiwania** (HH:MM): od której chwili szukać najtańszego ciągłego okna  
  - *Domyślnie:* 00:00  
  - *Przykład:* 22:00 – wyszukiwanie od 22:00 tego samego dnia

- **Koniec przeszukiwania** (HH:MM): do której chwili (wyłącznie) obowiązuje zakres  
  - **Wartość 00:00 w polu końca** oznacza **koniec tego samego dnia kalendarzowego** (ostatni kwadrans przypisany do dnia w danych PSE), a nie północ na początku dnia.  
  - *Domyślnie:* 00:00 – cały dzień od początku do końca (para 00:00–00:00 = pełny dzień).  
  - *Przykład:* 16:15–00:00 – od 16:15 do końca dnia (bez przechodzenia przez północ na „następny dzień” w sensie kalendarzowym).

- **Długość poszukiwanego okna** (HH:MM): jak długi ma być jeden ciągły blok (od 00:15 do 24:00)  
  - *Domyślnie:* 02:00  
  - *Przykład:* 03:00 – szukany jest blok trzech godzin; 02:15 – dwa godziny i kwadrans

### Ustawienia najdroższych godzin

Określają wyszukiwanie najdroższych okresów (np. do unikania szczytu). Te same zasady co wyżej: **HH:MM**, skok 15 minut, koniec **00:00** = koniec dnia.

- **Początek przeszukiwania** – *domyślnie* 00:00  
- **Koniec przeszukiwania** – *domyślnie* 00:00 (cały dzień)  
- **Długość poszukiwanego okna** – *domyślnie* 02:00

### Drugie najdroższe godziny

Osobne okno do wyznaczenia drugiego szczytu (np. poranek vs wieczór):

- **Początek przeszukiwania** – *domyślnie* 06:00  
- **Koniec przeszukiwania** – *domyślnie* 10:00  
- **Długość poszukiwanego okna** – *domyślnie* 02:00

### Ceny godzinowe

Opcja przydatna przy rozliczeniach net-billing (prosumenci, liczniki z rozliczeniem co godzinę przy 15-minutowych cenach PSE). Przy włączeniu integracja liczy średnią cenę za każdą godzinę z czterech przedziałów 15-minutowych.

- **Średnie ceny godzinowe** (tak/nie): uśrednianie w obrębie godziny  
  - *Domyślnie:* tak (średnia z czterech kwadransów w godzinie; ta sama wartość we wszystkich przedziałach 15-min w tej godzinie)  
  - *Po wyłączeniu:* surowe ceny 15-minutowe z API PSE  
  - *Zastosowanie:* rozliczenia według art. 4b ust. 11 ustawy o OZE

**Działanie:**  
- Włączone: liczone są średnie godzinowe; ta sama cena jest przypisana do wszystkich czterech przedziałów 15-min w danej godzinie.  
- Wyłączone: używane są surowe ceny 15-min z API PSE.  
- Przykład: godzina 0 z cenami [300, 320, 340, 360] PLN/MWh → przy włączonym uśrednianiu we wszystkich czterech przedziałach wyświetlana jest 330 PLN (średnia).

### Ceny netto/brutto

Integracja pozwala wybrać, czy wszystkie prezentowane ceny mają być traktowane jako netto (tak jak w API PSE), czy brutto (z doliczonym VAT według stawki `TAX_RATE`, obecnie 23%).

- **Użyj cen brutto (z VAT)** (tak/nie): globalne przełączenie netto/brutto  
  - *Domyślnie:* nie – ceny pozostają w formie netto z API PSE.  
  - *Po włączeniu:* wszystkie wartości cenowe w danych koordynatora (`rce_pln` oraz `rce_pln_neg_to_zero`) są przemnażane przez `(1 + TAX_RATE)` i dopiero takie dane są przekazywane do sensorów.  
  - *Efekt:* wszystkie sensory oparte na cenach (dzisiejsze, jutrzejsze, statystyki, okna itp.) automatycznie działają na cenach brutto, bez potrzeby dodatkowych przeliczeń w automatyzacjach.

Sensor ceny sprzedaży prosumenta (`rce_pse_today_prosumer_selling_price`) zawsze bazuje na wartości `rce_pln_neg_to_zero`:

- w trybie **netto** nadal dolicza VAT lokalnie (mnożenie przez `(1 + TAX_RATE)`),  
- w trybie **brutto** nie dolicza VAT ponownie – zwraca już przeliczoną wartość brutto, aby uniknąć podwójnego naliczania podatku.

### Jednostka ceny (PLN/MWh lub PLN/kWh)

- **Jednostka ceny** (domyślnie **PLN/MWh**): ta sama skala co w API PSE.  
- **PLN/kWh**: wszystkie wartości cen w danych koordynatora są dzielone przez 1000 względem surowych danych z API (czyli z MWh na kWh energetycznie). Sensory pokazują kwoty zaokrąglone do dwóch miejsc po przecinku; w `raw_data` stosowana jest wyższa precyzja wewnętrzna (formatowanie liczb w integracji).

### Próg niskiej ceny sprzedaży

Próg w **tej samej jednostce co wybrana jednostka ceny** (PLN/MWh lub PLN/kWh), używany do wyznaczania „okna niskiej ceny” w dedykowanych sensorach. Pierwszy ciągły okres w danym dniu z ceną ≤ progu pokazują sensory „Cena Poniżej Progu Dzisiaj/Jutro Początek/Koniec”; binary sensor „Cena poniżej progu aktywna” ma stan `on`, gdy trwa ten okres (dzisiaj). Gdy w danym dniu nie ma takiego okresu, sensory mają stan „unknown” (integracja działa normalnie).

- **Próg niskiej ceny sprzedaży**: zakres zależy od jednostki — przy PLN/MWh: -2000…2000; przy PLN/kWh: -2…2 (dopuszczalne wartości ujemne).  
  - *Domyślnie:* 0

## Zmiana ustawień

1. **Ustawienia** → **Integracje**
2. Znajdź "RCE PSE" na liście
3. Kliknij **Konfiguruj**
4. Zmień parametry i zatwierdź **Zapisz**

Integracja przeładuje się z nowymi ustawieniami. Po zmianie m.in. jednostki ceny encje mogą chwilowo być niedostępne; historia zapisana w recorderze nadal może zawierać stare próbki w poprzedniej skali przy tym samym `entity_id` — warto uwzględnić to w wykresach i automatyzacjach. Po przełączeniu PLN/MWh ↔ PLN/kWh zaktualizuj próg oraz ewentualne stałe liczby w automatyzacjach.

## Przykłady konfiguracji

**Ładowanie wieczorne (ten sam dzień)**  
- Najtańsze godziny: początek 18:00, koniec 00:00 (koniec dnia), długość 04:00  
- Szukane są 4 kolejne najtańsze kwadranse między 18:00 a końcem dnia

**Unikanie szczytu w ciągu dnia**  
- Najdroższe godziny: początek 08:00, koniec 18:00, długość 02:00  
- Identyfikacja 2 kolejnych najdroższych kwadransów w wybranym przedziale

**Jeden szczyt wieczorny**  
- Najdroższe godziny: początek 17:00, koniec 21:00, długość 01:00  
- Jedna najdroższa godzina w szczycie wieczornym

**Dwa szczyty (rano i wieczór)**  
- Drugie najdroższe: początek 06:00, koniec 10:00, długość 02:00  
- Osobne okno poranne; wieczór można ustawić w sekcji pierwszego „drogiego” okna z innym zakresem godzin

**Noc z przekroczeniem północy (np. EV)**  
- Jednego zakresu „22:00–06:00” nie ma — ustaw np. **osobno** szukanie taniego bloku wieczorem (jak wyżej) i ewentualnie drugi profil na kolejny dzień, albo użyj automatyzacji opartej o sensory timestamp i warunki czasowe.

## Dodatkowe sensory przy własnych oknach

Po skonfigurowaniu okien integracja udostępnia m.in.:

**Dzisiaj:**  
- Tanie Okno Dzisiaj Początek/Koniec, Tanie Okno Dzisiaj Średnia  
- Drogie Okno Dzisiaj Początek/Koniec, Drogie Okno Dzisiaj Średnia  
- Drugie Drogie Okno Dzisiaj Początek/Koniec, Drugie Drogie Okno Dzisiaj Średnia  

**Jutro:**  
- Odpowiednie sensory dla jutra (dane po 14:00 CET)

Sensory początku i końca okien zwracają **timestampy**; do wyświetlenia samej godziny (np. HH:MM) użyj szablonu z `timestamp_custom('%H:%M')`. Więcej: [Sensory](SENSORY.md), [Migracja do v2.0.0](MIGRACJA-V2.md).
