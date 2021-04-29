try:
    from homeassistant.components.light import LightEntity
except ImportError:
    from homeassistant.components.light import Light as LightEntity

from homeassistant.components.light import (ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS)
from homeassistant.helpers import entity_platform

from . import ModernFormsBaseEntity
from .const import DOMAIN, DEVICES, COORDINATORS, CONF_FAN_HOST, SERVICE_REBOOT

async def async_setup_entry(hass, config_entry, async_add_devices):
  host = config_entry.data.get(CONF_FAN_HOST)
  coordinator = hass.data[DOMAIN][COORDINATORS][host]
  device = hass.data[DOMAIN][DEVICES][host]

  platform = entity_platform.current_platform.get()
  platform.async_register_entity_service(SERVICE_REBOOT, {}, "async_reboot")

  return async_add_devices([ModernFormsLight(coordinator, device)])

class ModernFormsLight(LightEntity, ModernFormsBaseEntity):
  def __init__(self, coordinator, device):
    ModernFormsBaseEntity.__init__(self, coordinator, device)

  @property
  def brightness(self):
    return round(255*self.device.lightBrightness()/100)

  @property
  def unique_id(self):
    return self.device.clientId()

  @property
  def name(self):
    return self.device.name + " Light"

  async def async_turn_on(self, **kwargs):
    if ATTR_BRIGHTNESS in kwargs:
      br = round(100*kwargs[ATTR_BRIGHTNESS]/255)
      await self.perform_action_and_refresh(self.device.set_light_brightness, br)
    else:
      await self.perform_action_and_refresh(self.device.set_light_on)

  async def async_turn_off(self, **kwargs) -> None:
    await self.perform_action_and_refresh(self.device.set_light_off)

  @property
  def is_on(self):
    return self.device.lightOn()

  @property
  def supported_features(self) -> int:
    return SUPPORT_BRIGHTNESS


