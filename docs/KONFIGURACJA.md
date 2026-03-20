# Konfiguracja

Po zainstalowaniu integracji możesz ją skonfigurować w interfejsie Home Assistant. W formularzu najpierw wybierasz opcje cenowe (średnie godzinowe, brutto, próg niskiej ceny), potem okna czasowe (tanie / drogie godziny), aby ułatwić znalezienie najlepszych cen prądu.

## Opcje konfiguracji

### Ustawienia najtańszych godzin

Określają, w jakim przedziale szukać najbardziej ekonomicznych okresów:

- **Godzina początkowa** (0–23): początek okna do wyszukiwania najtańszych godzin  
  - *Domyślnie:* 0 (północ)  
  - *Przykład:* 22 – wyszukiwanie od 22:00

- **Godzina końcowa** (1–24): koniec okna do wyszukiwania najtańszych godzin  
  - *Domyślnie:* 24 (północ następnego dnia)  
  - *Przykład:* 6 – wyszukiwanie do 6:00

- **Czas trwania (godziny)** (1–24): długość jednego ciągłego okna najtańszych godzin  
  - *Domyślnie:* 2 godziny  
  - *Przykład:* 3 – blok 3 godzin najtańszego prądu

### Ustawienia najdroższych godzin

Określają wyszukiwanie najdroższych okresów (np. do unikania szczytu):

- **Godzina początkowa** (0–23): początek okna dla najdroższych godzin  
  - *Domyślnie:* 0  
  - *Przykład:* 16 – od 16:00

- **Godzina końcowa** (1–24): koniec okna  
  - *Domyślnie:* 24  
  - *Przykład:* 20 – do 20:00

- **Czas trwania (godziny)** (1–24): długość okna najdroższych godzin  
  - *Domyślnie:* 2 godziny  
  - *Przykład:* 1 – jedna godzina

### Drugie najdroższe godziny

Osobne okno do wyznaczenia drugiego szczytu (np. poranek vs wieczór):

- **Godzina początkowa** (0–23): *domyślnie* 6  
- **Godzina końcowa** (1–24): *domyślnie* 10  
- **Czas trwania (godziny)** (1–24): *domyślnie* 2

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

### Próg niskiej ceny sprzedaży

Próg (PLN/MWh) używany do wyznaczania "okna niskiej ceny" w dedykowanych sensorach. Pierwszy ciągły okres w danym dniu z ceną ≤ progu pokazują sensory "Cena Poniżej Progu Dzisiaj/Jutro Początek/Koniec"; binary sensor "Cena poniżej progu aktywna" ma stan `on`, gdy trwa ten okres (dzisiaj). Gdy w danym dniu nie ma takiego okresu, sensory mają stan "unknown" (integracja działa normalnie).

- **Próg niskiej ceny sprzedaży** (PLN/MWh): zakres -2000–2000 (dopuszczalne wartości ujemne)  
  - *Domyślnie:* 0

## Zmiana ustawień

1. **Ustawienia** → **Integracje**
2. Znajdź "RCE PSE" na liście
3. Kliknij **Konfiguruj**
4. Zmień parametry i zatwierdź **Zapisz**

Integracja przeładuje się z nowymi ustawieniami.

## Przykłady konfiguracji

**Ładowanie nocne (EV)**  
- Najtańsze godziny: początek=22, koniec=6, czas trwania=4  
- Szukane są 4 kolejne najtańsze godziny między 22:00 a 6:00

**Unikanie szczytu w ciągu dnia**  
- Najdroższe godziny: początek=8, koniec=18, czas trwania=2  
- Identyfikacja 2 kolejnych najdroższych godzin w godzinach pracy

**Jeden szczyt wieczorny**  
- Najdroższe godziny: początek=17, koniec=21, czas trwania=1  
- Jedna najdroższa godzina w szczycie wieczornym

**Dwa szczyty (rano i wieczór)**  
- Drugie najdroższe: początek=6, koniec=10, czas trwania=2  
- 2-godzinny szczyt poranny oddzielony od wieczornego

## Dodatkowe sensory przy własnych oknach

Po skonfigurowaniu okien integracja udostępnia m.in.:

**Dzisiaj:**  
- Tanie Okno Dzisiaj Początek/Koniec, Tanie Okno Dzisiaj Średnia  
- Drogie Okno Dzisiaj Początek/Koniec, Drogie Okno Dzisiaj Średnia  
- Drugie Drogie Okno Dzisiaj Początek/Koniec, Drugie Drogie Okno Dzisiaj Średnia  

**Jutro:**  
- Odpowiednie sensory dla jutra (dane po 14:00 CET)

Sensory początku i końca okien zwracają **timestampy**; do wyświetlenia samej godziny (np. HH:MM) użyj szablonu z `timestamp_custom('%H:%M')`. Więcej: [Sensory](SENSORY.md), [Migracja do v2.0.0](MIGRACJA-V2.md).
