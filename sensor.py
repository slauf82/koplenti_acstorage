from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    data = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([

        KoplentiLogSensor(
            data["log_buffer"],
            data["last_octet"]
        )

    ], True)


class KoplentiLogSensor(SensorEntity):

    def __init__(self, log_buffer, last_octet):

        self._log_buffer = log_buffer

        self._attr_name = f"ACStorage Log ({last_octet})"

        self._attr_unique_id = f"{DOMAIN}_log_{last_octet}"

    @property
    def native_value(self):

        return len(self._log_buffer)

    @property
    def extra_state_attributes(self):

        return {

            "logs": list(self._log_buffer)

        }