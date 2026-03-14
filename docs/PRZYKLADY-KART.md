# Przykłady kart na dashboardzie

Poniżej dwa gotowe układy kart do wyświetlania cen energii.

## 1. Zaawansowane wykresy (ApexCharts) – wymagana dodatkowa karta

Karta z wykresami i analizą cen w czasie. Wymaga zainstalowanej karty ApexCharts w HACS.

![Karta ApexCharts](../examples/images/card2_apexcharts.png)

**Konfiguracja:**  
- [PL: examples/pl/card2_apexcharts_analysis.yaml](../examples/pl/card2_apexcharts_analysis.yaml)  
- [EN: examples/en/card2_apexcharts_analysis.yaml](../examples/en/card2_apexcharts_analysis.yaml)

**Wymagania:**  
- `apexcharts-card` – instalacja przez HACS → "ApexCharts Card"

## 2. Podstawowy przegląd – bez dodatkowych zależności

Prosty przegląd bieżących cen na podstawie standardowych encji Home Assistant.

![Karta podstawowa](../examples/images/card1_basic.png)

**Konfiguracja:**  
- [PL: examples/pl/card1_basic_overview.yaml](../examples/pl/card1_basic_overview.yaml)  
- [EN: examples/en/card1_basic_overview.yaml](../examples/en/card1_basic_overview.yaml)

Karty można dowolnie dostosować do motywu i potrzeb: skopiuj YAML z pliku i wklej w edytorze dashboardu (tryb edycji karty).
