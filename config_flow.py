import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_PASSWORD, CONF_SERVICE_CODE

class KoplentiACStorageFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"{user_input[CONF_HOST]}",
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Optional(CONF_SERVICE_CODE, default=""): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
