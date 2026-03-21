# Źródło danych

Integracja pobiera dane z oficjalnego API PSE (Polskie Sieci Elektroenergetyczne):

- **API:** `https://api.raporty.pse.pl/api` (API v2)
- **Interwał odświeżania:** 30 minut
- **Dostępność danych "jutro":** ceny na następny dzień publikowane są po **14:00 CET**

Endpointy:

- **RCE (Ceny Energii):** `\rce-pln` – ceny rynkowe energii (RCE) w PLN/MWh, rozdzielczość 15 minut. Zapytanie OData ogranicza pola do tych używanych w integracji: m.in. `dtime`, `period`, `rce_pln`, `business_date`.

- **PDGSZ (Godziny Szczytu / Energetyczny Kompas):** `\pdgsz` – prognoza użytkowania (`usage_fcst`) na godziny, zalecenia PSE co do użytkowania i oszczędzania energii. Pobierane są m.in. `business_date`, `dtime`, `is_active`, `usage_fcst`.
