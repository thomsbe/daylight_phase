"""Sensor platform for Daylight Phase Controller."""
import math
import statistics
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import STATE_UNKNOWN, STATE_UNAVAILABLE

from .const import (
    DOMAIN, CONF_SUN_SENSOR, CONF_INDOOR_SENSORS, CONF_OUTDOOR_SENSORS,
    CONF_CALCULATION_METHOD, CONF_MAX_LUX_INDOOR, CONF_MAX_LUX_OUTDOOR,
    CONF_THRESHOLD_INDOOR, CONF_THRESHOLD_OUTDOOR,
    METHOD_MEDIAN, METHOD_MEAN
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    async_add_entities([DaylightPhaseSensor(hass, entry)])

class DaylightPhaseSensor(SensorEntity):
    """Representation of a Daylight Phase Sensor."""

    def __init__(self, hass, entry):
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_name = "Daylight Phase"
        self._attr_unique_id = f"{entry.entry_id}_daylight_phase"
        self._attr_icon = "mdi:weather-night-兼用"
        
        self._state = STATE_UNKNOWN
        self._score_indoor = 0
        self._score_outdoor = 0
        
        self._sun_sensor = entry.data[CONF_SUN_SENSOR]
        self._indoor_sensors = entry.data[CONF_INDOOR_SENSORS]
        self._outdoor_sensors = entry.data[CONF_OUTDOOR_SENSORS]
        self._method = entry.data[CONF_CALCULATION_METHOD]
        self._max_indoor = entry.data[CONF_MAX_LUX_INDOOR]
        self._max_outdoor = entry.data[CONF_MAX_LUX_OUTDOOR]
        self._threshold_indoor = entry.data[CONF_THRESHOLD_INDOOR]
        self._threshold_outdoor = entry.data[CONF_THRESHOLD_OUTDOOR]

        self._entities_to_track = [self._sun_sensor] + self._indoor_sensors + self._outdoor_sensors

    async def async_added_to_hass(self):
        """Handle added to Hass."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, self._entities_to_track, self._handle_state_change
            )
        )
        self._update_state()

    def _handle_state_change(self, event):
        """Update state when a tracked entity changes."""
        self._update_state()
        self.schedule_update_ha_state()

    def _get_lux_value(self, sensor_list):
        """Calculate aggregate lux value from a list of sensors."""
        values = []
        for entity_id in sensor_list:
            state = self.hass.states.get(entity_id)
            if state and state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
                try:
                    values.append(float(state.state))
                except ValueError:
                    continue
        
        if not values:
            return -1
        
        if self._method == METHOD_MEDIAN:
            return statistics.median(values)
        return statistics.mean(values)

    def _calculate_score(self, lux, max_lux):
        """Calculate 0..10 score using logarithmic scale."""
        if lux <= 0:
            return 0
        raw = (math.log(lux + 1) / math.log(max_lux + 1)) * 10
        return int(max(0, min(10, round(raw))))

    def _update_state(self):
        """Calculate the current phase."""
        sun_state = self.hass.states.get(self._sun_sensor)
        if not sun_state:
            return

        elevation = float(sun_state.attributes.get("elevation", 0))
        rising = sun_state.attributes.get("rising", False)
        
        lux_indoor = self._get_lux_value(self._indoor_sensors)
        lux_outdoor = self._get_lux_value(self._outdoor_sensors)
        
        self._score_indoor = self._calculate_score(lux_indoor, self._max_indoor) if lux_indoor >= 0 else self._score_indoor
        self._score_outdoor = self._calculate_score(lux_outdoor, self._max_outdoor) if lux_outdoor >= 0 else self._score_outdoor

        if elevation < -6:
            new_state = "night"
        elif elevation < 0:
            new_state = "dawn" if rising else "dusk"
        else:
            if self._score_indoor < self._threshold_indoor and self._score_outdoor > self._threshold_outdoor:
                new_state = "darkening"
            elif self._score_indoor < self._threshold_indoor and self._score_outdoor <= self._threshold_outdoor:
                new_state = "cloudy"
            else:
                new_state = "day"
        
        self._state = new_state

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "score_indoor": self._score_indoor,
            "score_outdoor": self._score_outdoor,
            "calculation_method": self._method
        }
