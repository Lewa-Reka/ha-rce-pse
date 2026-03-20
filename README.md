# Integracja RCE PSE do Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub Release](https://img.shields.io/github/v/release/lewa-reka/ha-rce-pse?style=for-the-badge)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/lewa-reka/ha-rce-pse/tests.yml?style=for-the-badge)
[![hacs_downloads](https://img.shields.io/github/downloads/lewa-reka/ha-rce-pse/latest/total?style=for-the-badge)](https://github.com/lewa-reka/ha-rce-pse/releases/latest)
![GitHub License](https://img.shields.io/github/license/lewa-reka/ha-rce-pse?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/lewa-reka/ha-rce-pse?style=for-the-badge)
![Maintenance](https://img.shields.io/maintenance/yes/2222?style=for-the-badge)

## Rynkowa Cena Energii

Integracja do Home Assistant do śledzenia polskich cen rynkowych energii (RCE – Rynkowa Cena Energii) z PSE (Polskie Sieci Elektroenergetyczne). Obsługa okresów 15 minutowych i 1 godzinnych. Odświeżanie danych co 30 minut z oficjalnego API PSE.

Prezentacja i instalacja: <https://youtu.be/6N71uXgf9yc>

## Instalacja

[![Otwórz HACS i dodaj repozytorium](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Lewa-Reka&repository=ha-rce-pse&category=integration)

### HACS (zalecane)

1. Otwórz HACS w Home Assistant
2. Wyszukaj **"RCE PSE"**
3. Pobierz integrację
4. Zrestartuj Home Assistant

### Instalacja ręczna

1. Skopiuj folder `custom_components/rce_pse` do katalogu `custom_components` w Home Assistant
2. Zrestartuj Home Assistant

### Pierwsza konfiguracja

[![Dodaj integrację](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=rce_pse)

1. **Ustawienia** → **Integracje**
2. **Dodaj integrację** → wyszukaj "RCE PSE"
3. Ustaw opcje okien czasowych (szczegóły: [Konfiguracja](docs/KONFIGURACJA.md))
4. **Zapisz**

## Funkcje

- Bieżąca cena energii z dokładnością 15 min, dane historyczne i prognoza następnego okresu
- Statystyki dzienne (średnia, min, max, mediana), porównanie dziś vs jutro
- Definiowane przez użytkownika okna tanich i drogich godzin, sensory czasowe (timestampy)
- Opcjonalne ceny godzinowe (net-billing), próg niskiej ceny sprzedaży
- Dane "jutro" dostępne po 14:00 CET, odświeżanie co 30 min

Szczegóły: [Konfiguracja](docs/KONFIGURACJA.md), [Sensory](docs/SENSORY.md).

## Dokumentacja

- [Konfiguracja](docs/KONFIGURACJA.md) – opcje, przykłady, rekonfiguracja
- [Sensory](docs/SENSORY.md) – lista sensorów i binary sensorów
- [Przykłady kart](docs/PRZYKLADY-KART.md) – karty dashboardu (ApexCharts, podstawowy przegląd)
- [Debugowanie](docs/DEBUGOWANIE.md) – logowanie debugowe
- [Źródło danych](docs/ZRODLO-DANYCH.md) – API PSE, interwał, dostępność
- [Migracja do v2.0.0](docs/MIGRACJA-V2.md) – zmiany niekompatybilne wstecz i porady migracji

## Licencja

Projekt na licencji Apache License 2.0 – szczegóły w pliku [LICENSE](LICENSE).

## Współpraca

Pull Requesty mile widziane. Przy większych zmianach warto wcześniej otworzyć issue. Prosimy o aktualizację testów i zachowanie standardów projektu (CI: pytest, HACS, hassfest, MegaLinter; Dependabot aktualizuje zależności).
