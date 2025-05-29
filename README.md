# RCE PSE Integration for Home Assistant
## Rynkowa Cena Energii

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub Release](https://img.shields.io/github/v/release/lewa-reka/ha-rce-pse?style=for-the-badge)
[![hacs_downloads](https://img.shields.io/github/downloads/lewa-reka/ha-rce-pse/latest/total?style=for-the-badge)](https://github.com/lewa-reka/ha-rce-pse/releases/latest)
![GitHub License](https://img.shields.io/github/license/lewa-reka/ha-rce-pse?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/lewa-reka/ha-rce-pse?style=for-the-badge)
![Maintenance](https://img.shields.io/maintenance/yes/2025?style=for-the-badge)

A Home Assistant integration for monitoring Polish electricity market prices (RCE - Rynkowa Cena Energii) from PSE (Polskie Sieci Elektroenergetyczne).

## Features

- Current electricity price monitoring
- Future prices (1h, 2h, 3h ahead)
- Daily statistics (average, min, max, median)
- Tomorrow's statistics (available after 14:00 CET)
- Today vs tomorrow price comparison
- Hours of highest and lowest prices

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant
4. Add the integration through Configuration > Integrations

### Manual Installation

1. Copy the `custom_components/rce-pse` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration through Configuration > Integrations

## Sensors

The integration provides 23 sensors:

### Main Sensors
- **Price** - Current electricity price
- **Tomorrow Price** - Tomorrow's average price (available after 14:00 CET)

### Future Price Sensors
- **Next Hour Price** - Price for the next hour
- **Price in 2 Hours** - Price in 2 hours
- **Price in 3 Hours** - Price in 3 hours

### Today's Statistics
- **Today Average Price** - Average price for today
- **Today Maximum Price** - Highest price today
- **Today Minimum Price** - Lowest price today
- **Today Median Price** - Median price for today
- **Today Current vs Average** - Percentage difference between current and average price

### Tomorrow's Statistics (available after 14:00 CET)
- **Tomorrow Average Price** - Average price for tomorrow
- **Tomorrow Maximum Price** - Highest price tomorrow
- **Tomorrow Minimum Price** - Lowest price tomorrow
- **Tomorrow Median Price** - Median price for tomorrow
- **Tomorrow vs Today Average** - Percentage difference between tomorrow and today average

### Price Hours
- **Today Max Price Hour Start/End** - When the highest price period starts/ends today
- **Today Min Price Hour Start/End** - When the lowest price period starts/ends today
- **Tomorrow Max Price Hour Start/End** - When the highest price period starts/ends tomorrow
- **Tomorrow Min Price Hour Start/End** - When the lowest price period starts/ends tomorrow

## Debugging

To enable debug logging for the RCE PSE integration, add the following to your Home Assistant `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.rce_pse: debug
```

This will enable detailed logging for:
- Integration setup and configuration
- API requests and responses 
- Data fetching and processing
- Sensor creation and updates
- Error handling and troubleshooting

After adding this configuration, restart Home Assistant and check the logs in:
- **Configuration** > **Logs** in the Home Assistant UI
- Or directly in the `home-assistant.log` file

Debug logs include:
- PSE API request URLs and parameters
- API response status and data counts
- Configuration flow steps
- Sensor setup progress
- Coordinator data updates

## Data Source

This integration fetches data from the official PSE API:
- **API**: `https://v2.api.raporty.pse.pl/api`
- **Update Interval**: 30 minutes
- **Data Availability**: Tomorrow's prices are available after 14:00 CET

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### Apache 2.0 License

Copyright 2025 Lewa-Reka and RCE PSE Integration Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate and ensure your code follows the project's coding standards. 