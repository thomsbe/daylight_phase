# Daylight Phase Controller

This Home Assistant integration provides a sophisticated lighting context sensor by combining astronomical sun data with real-time brightness measurements from indoor and outdoor sensors.

## Features
- **Intelligent Phases**: Automatically determines the phase (NIGHT, DAWN, DUSK, DAY, DARKENING, CLOUDY) based on sun elevation and actual light levels.
- **Logarithmic Scaling**: Brightness values (Lux) are converted into a normalized 0-10 score, providing better resolution for human light perception.
- **Multi-Sensor Support**: Use multiple sensors for indoor/outdoor measurements with automatic Median or Mean calculation.
- **Context Awareness**: Detects if your blinds are closed during the day (DARKENING) or if it's an exceptionally dark storm/winter day (CLOUDY).

## Brightness Score Calculation
The integration uses a logarithmic scale to convert raw Lux values (0 to Max) into an integer score between 0 and 10.
- **Score 0**: Absolute darkness.
- **Score 5**: Moderate light (e.g., 50 Lux with a Max of 2000).
- **Score 10**: Maximum brightness (at or above your defined Max Lux).

## Daylight Phases
The sensor state provides the following values:
- **night**: Sun elevation < -6° (Civil dusk ended).
- **dawn**: Sun is rising, elevation between -6° and 0°.
- **dusk**: Sun is setting, elevation between 0° and -6°.
- **day**: Sun is above the horizon and interior light is sufficient.
- **darkening**: Sun is above horizon, but interior is dark while exterior is bright (e.g., blinds closed).
- **cloudy**: Sun is above horizon, but both interior and exterior are dark (e.g., storm or very dark winter day).

---

## Kurzfassung (Deutsch)
Der **Daylight Phase Controller** ermittelt präzise Beleuchtungskontexte für Dein Smart Home. Er kombiniert den Sonnenstand mit echten Lux-Werten Deiner Sensoren.
- **Logarithmische Skala**: Wandelt Lux-Werte in einen Score von 0 bis 10 um.
- **Phasen-Erkennung**: Erkennt automatisch Zustände wie Nacht, Tag, Dämmerung oder ob es drinnen dunkel ist, obwohl draußen die Sonne scheint (Verdunklung).
- **Automatisierung**: Ideal als Basis für Lichtsteuerungen.

---

## Installation via HACS (Recommended)
You can add this repository to HACS to stay up-to-date:
1. Open **HACS** in your Home Assistant instance.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Paste the URL of this repository: `https://github.com/thomsbe/daylight_phase`
4. Select **Integration** as the category and click **Add**.
5. You can now find and install "Daylight Phase Controller" in HACS.
6. Restart Home Assistant.
7. Go to **Settings -> Devices & Services -> Add Integration** and search for "Daylight Phase Controller".

## Manual Installation
1. Copy the `daylight_phase` folder from `custom_components` to your own `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration via **Settings -> Devices & Services -> Add Integration**.
