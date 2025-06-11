# RCE PSE Integration for Home Assistant - API v2 ready

[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub Release](https://img.shields.io/github/v/release/lewa-reka/ha-rce-pse?style=for-the-badge)
[![hacs_downloads](https://img.shields.io/github/downloads/lewa-reka/ha-rce-pse/latest/total?style=for-the-badge)](https://github.com/lewa-reka/ha-rce-pse/releases/latest)
![GitHub License](https://img.shields.io/github/license/lewa-reka/ha-rce-pse?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/lewa-reka/ha-rce-pse?style=for-the-badge)
![Maintenance](https://img.shields.io/maintenance/yes/2025?style=for-the-badge)

## Rynkowa Cena Energii

A Home Assistant integration for monitoring Polish electricity market prices (RCE - Rynkowa Cena Energii) from PSE (Polskie Sieci Elektroenergetyczne).

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Lewa-Reka&repository=ha-rce-pse&category=integration)

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/rce_pse` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

### Initial Setup

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=rce_pse)

1. Go to **Settings** > **Integrations**
2. Click **Add Integration** and search for "RCE PSE"
3. Configure the time window settings (see below)
4. Click **Submit** to complete the setup

## Usage Examples

Here are two ready-to-use dashboard card configurations that showcase different ways to display energy price data:

### 1. Advanced Charts with ApexCharts (Additional Dependencies Required)

This card provides advanced charting capabilities with professional-looking graphs and real-time price analysis. Perfect for users who want detailed visual analytics.

![ApexCharts Analysis Card](examples/images/card2_apexcharts.png)

**Configuration file**: [`examples/card2_apexcharts_analysis.yaml`](examples/card2_apexcharts_analysis.yaml)


**Requirements:**
- `apexcharts-card` - Install via HACS → "ApexCharts Card"

### 2. Basic Overview (No Dependencies Required)

This card provides a comprehensive overview of current energy prices using standard Home Assistant entities. It's perfect for users who want a clean, simple display without additional dependencies.

![Basic Overview Card](examples/images/card1_basic.png)

**Configuration file**: [`examples/card1_basic_overview.yaml`](examples/card1_basic_overview.yaml)


Both cards can be easily customized to match your dashboard theme and specific needs. Simply copy the YAML configuration from the respective files and paste them into your Home Assistant dashboard in edit mode.

## Features

- **Real-time price monitoring** - Current electricity price with 15-minute precision
- **Historical data** - Previous hour pricing information  
- **Future price forecasting** - Prices for next 1-3 hours ahead
- **Daily statistics** - Comprehensive price analysis (average, min, max, median)
- **Tomorrow's data** - Next day pricing available after 14:00 CET
- **Price comparison** - Today vs tomorrow percentage differences
- **Optimal time windows** - Configurable search for cheapest and most expensive periods
- **Smart scheduling** - Find best times for energy-intensive activities
- **Peak avoidance** - Identify and avoid high-cost electricity periods
- **Time range display** - Easy-to-read time ranges (e.g., "23:00 - 01:00")
- **Automatic updates** - Data refreshed every 30 minutes from official PSE API

## Configuration

After installing the integration, you can configure it through the Home Assistant UI. The integration offers several customization options for optimal time windows that help you find the best electricity prices for your needs.

### Configuration Options

The integration provides advanced configuration options to customize how it searches for optimal electricity price windows:

#### Cheapest Hours Search Settings

These settings control how the integration finds the most economical electricity periods:

- **Start Hour** (0-23): Beginning of the time window to search for cheapest hours
  - *Default*: 0 (midnight)
  - *Example*: Set to 22 to search from 10 PM onwards

- **End Hour** (1-24): End of the time window to search for cheapest hours  
  - *Default*: 24 (midnight next day)
  - *Example*: Set to 6 to search until 6 AM

- **Duration (hours)** (1-24): Length of the cheapest continuous time window to find
  - *Default*: 2 hours
  - *Example*: Set to 3 to find 3-hour blocks of cheapest electricity

#### Most Expensive Hours Search Settings

These settings control how the integration finds the most expensive electricity periods (useful for avoiding high-cost times):

- **Start Hour** (0-23): Beginning of the time window to search for most expensive hours
  - *Default*: 0 (midnight)
  - *Example*: Set to 16 to search from 4 PM onwards

- **End Hour** (1-24): End of the time window to search for most expensive hours
  - *Default*: 24 (midnight next day)  
  - *Example*: Set to 20 to search until 8 PM

- **Duration (hours)** (1-24): Length of the most expensive continuous time window to find
  - *Default*: 2 hours
  - *Example*: Set to 1 to find 1-hour blocks of most expensive electricity

### Reconfiguring Settings

You can modify these settings at any time:

1. Go to **Configuration** > **Integrations**
2. Find "RCE PSE" in your integrations list
3. Click **Configure** 
4. Adjust the settings as needed
5. Click **Submit** to apply changes

The integration will automatically reload with your new settings.

### Configuration Examples

**Example 1: Night Charging (Electric Vehicle)**
- Cheapest Hours: Start=22, End=6, Duration=4
- Find 4 cheapest consecutive hours between 10 PM and 6 AM

**Example 2: Business Hours Optimization**  
- Most Expensive Hours: Start=8, End=18, Duration=2
- Avoid the 2 most expensive consecutive hours during business hours

**Example 3: Peak Avoidance**
- Most Expensive Hours: Start=17, End=21, Duration=1  
- Identify the single most expensive hour during evening peak

### Additional Sensors

When you configure custom time windows, the integration provides additional sensors:

**For Today:**
- Cheapest Window Start/End/Range
- Most Expensive Window Start/End/Range

**For Tomorrow:**
- Cheapest Window Start/End/Range  
- Most Expensive Window Start/End/Range

These sensors automatically update based on your configured search parameters and provide precise time ranges in HH:MM format.

## Sensors

### Main Sensors
- **Price** - Current electricity price
- **Price for kWh** - Dedicated for HomeAssistant Energy dashboard
- **Tomorrow Price** - Tomorrow's average price (available after 14:00 CET)

### Future Price Sensors
- **Next Hour Price** - Price for the next hour
- **Price in 2 Hours** - Price in 2 hours
- **Price in 3 Hours** - Price in 3 hours
- **Previous Hour Price** - Price from the previous hour

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

### Price Hours & Time Ranges
- **Today Max Price Hour Start/End** - When the highest price period starts/ends today
- **Today Min Price Hour Start/End** - When the lowest price period starts/ends today
- **Today Max Price Range** - Time range of highest price period (e.g., "17:00 - 18:00")
- **Today Min Price Range** - Time range of lowest price period (e.g., "02:00 - 03:00")
- **Tomorrow Max Price Hour Start/End** - When the highest price period starts/ends tomorrow
- **Tomorrow Min Price Hour Start/End** - When the lowest price period starts/ends tomorrow
- **Tomorrow Max Price Range** - Time range of highest price period tomorrow
- **Tomorrow Min Price Range** - Time range of lowest price period tomorrow

### Custom Time Window Sensors

Based on your configuration settings, the integration provides additional sensors for optimal time windows:

#### Today's Custom Windows
- **Today Cheapest Window Start** - Start time of cheapest configured window
- **Today Cheapest Window End** - End time of cheapest configured window  
- **Today Cheapest Window Range** - Time range of cheapest window (e.g., "23:00 - 01:00")
- **Today Expensive Window Start** - Start time of most expensive configured window
- **Today Expensive Window End** - End time of most expensive configured window
- **Today Expensive Window Range** - Time range of most expensive window

#### Tomorrow's Custom Windows (available after 14:00 CET)
- **Tomorrow Cheapest Window Start** - Start time of cheapest configured window
- **Tomorrow Cheapest Window End** - End time of cheapest configured window
- **Tomorrow Cheapest Window Range** - Time range of cheapest window
- **Tomorrow Expensive Window Start** - Start time of most expensive configured window  
- **Tomorrow Expensive Window End** - End time of most expensive configured window
- **Tomorrow Expensive Window Range** - Time range of most expensive window

All time values are provided in 24-hour format (HH:MM) and automatically update based on current market data and your configuration settings.

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
