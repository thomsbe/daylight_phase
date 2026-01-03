"""Config flow for Daylight Phase Controller integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import (
    DOMAIN, CONF_SUN_SENSOR, CONF_INDOOR_SENSORS, CONF_OUTDOOR_SENSORS,
    CONF_CALCULATION_METHOD, CONF_MAX_LUX_INDOOR, CONF_MAX_LUX_OUTDOOR,
    CONF_THRESHOLD_INDOOR, CONF_THRESHOLD_OUTDOOR,
    METHOD_MEDIAN, METHOD_MEAN, 
    DEFAULT_MAX_LUX_INDOOR, DEFAULT_MAX_LUX_OUTDOOR,
    DEFAULT_THRESHOLD_INDOOR, DEFAULT_THRESHOLD_OUTDOOR
)

class DaylightPhaseConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Daylight Phase Controller."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Daylight Phase Controller", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SUN_SENSOR, default="sun.sun"): selector.EntitySelector(
                    {"domain": "sun"}
                ),
                vol.Required(CONF_INDOOR_SENSORS): selector.EntitySelector(
                    {"multiple": True, "domain": "sensor", "device_class": "illuminance"}
                ),
                vol.Required(CONF_OUTDOOR_SENSORS): selector.EntitySelector(
                    {"multiple": True, "domain": "sensor", "device_class": "illuminance"}
                ),
                vol.Required(CONF_CALCULATION_METHOD, default=METHOD_MEDIAN): vol.In(
                    {METHOD_MEDIAN: "Median", METHOD_MEAN: "Mittelwert"}
                ),
                vol.Required(CONF_MAX_LUX_INDOOR, default=DEFAULT_MAX_LUX_INDOOR): int,
                vol.Required(CONF_MAX_LUX_OUTDOOR, default=DEFAULT_MAX_LUX_OUTDOOR): int,
                vol.Required(CONF_THRESHOLD_INDOOR, default=DEFAULT_THRESHOLD_INDOOR): int,
                vol.Required(CONF_THRESHOLD_OUTDOOR, default=DEFAULT_THRESHOLD_OUTDOOR): int,
            })
        )
