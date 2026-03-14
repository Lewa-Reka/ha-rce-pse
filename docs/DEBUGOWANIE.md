# Debugowanie

Aby włączyć logowanie debugowe integracji RCE PSE, dodaj do `configuration.yaml` w Home Assistant:

```yaml
logger:
  default: info
  logs:
    custom_components.rce_pse: debug
```

Po zapisaniu konfiguracji zrestartuj Home Assistant.

**Gdzie sprawdzać logi:**  
- **Ustawienia** → **Logi** w interfejsie Home Assistant  
- lub bezpośrednio w pliku `home-assistant.log`

W logach debugowych pojawią się m.in.:  
- adresy i parametry żądań do API PSE  
- status odpowiedzi i liczba pobranych danych  
- kroki konfiguracji (config flow)  
- informacje o tworzeniu i aktualizacji sensorów  
- błędy i ostrzeżenia
