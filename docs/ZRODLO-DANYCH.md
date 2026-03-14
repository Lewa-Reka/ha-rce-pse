# Źródło danych

Integracja pobiera dane z oficjalnego API PSE (Polskie Sieci Elektroenergetyczne):

- **API:** `https://api.raporty.pse.pl/api` (API v2)
- **Interwał odświeżania:** 30 minut
- **Dostępność danych "jutro":** ceny na następny dzień publikowane są po **14:00 CET**

Endpointy:

- **RCE (ceny energii):** `\rce-pln` – ceny rynkowe energii (RCE) w PLN/MWh, rozdzielczość 15 minut.
- **PDGSZ (Godziny Szczytu):** `\pdgsz` – prognoza użytkowania (usage_fcst) na godziny, zalecenia PSE co do użytkowania i oszczędzania energii.
