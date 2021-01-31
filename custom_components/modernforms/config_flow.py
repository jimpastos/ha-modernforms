from homeassistant import config_entries
import voluptuous as vol

from .const import \
    DOMAIN, \
    CONF_ENABLE_LIGHT, CONF_FAN_HOST, CONF_FAN_NAME


def get_schema(user_input=None):
    data = {}
    if user_input is not None:
        data = user_input

    def default(key, default_value=None):
        kwargs = {}

        if bool(data.get(key)):
            kwargs['default'] = data[key]
        elif default_value:
            kwargs['default'] = default_value

        return kwargs

    return vol.Schema({
        vol.Required(CONF_FAN_HOST, **default(CONF_FAN_HOST)): str,
        vol.Required(CONF_FAN_NAME, **default(CONF_FAN_NAME)): str,
        vol.Required(CONF_ENABLE_LIGHT, **default(CONF_ENABLE_LIGHT, True)): bool
    })

class ModernFormsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if len(errors) == 0:
                await self.async_set_unique_id(
                    user_input[CONF_FAN_HOST], raise_on_progress=False
                )

                return self.async_create_entry(
                    title=user_input[CONF_FAN_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=get_schema(user_input), errors=errors)
