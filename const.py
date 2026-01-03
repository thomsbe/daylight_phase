"""Constants for the Daylight Phase Controller integration."""

DOMAIN = "daylight_phase"

CONF_SUN_SENSOR = "sun_sensor"
CONF_INDOOR_SENSORS = "indoor_sensors"
CONF_OUTDOOR_SENSORS = "outdoor_sensors"
CONF_CALCULATION_METHOD = "calculation_method"
CONF_MAX_LUX_INDOOR = "max_lux_indoor"
CONF_MAX_LUX_OUTDOOR = "max_lux_outdoor"
CONF_THRESHOLD_INDOOR = "threshold_indoor"
CONF_THRESHOLD_OUTDOOR = "threshold_outdoor"

METHOD_MEDIAN = "median"
METHOD_MEAN = "mean"

DEFAULT_MAX_LUX_INDOOR = 2000
DEFAULT_MAX_LUX_OUTDOOR = 100000
DEFAULT_THRESHOLD_INDOOR = 3
DEFAULT_THRESHOLD_OUTDOOR = 5
