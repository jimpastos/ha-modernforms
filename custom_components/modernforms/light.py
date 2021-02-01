try:
    from homeassistant.components.light import LightEntity
except ImportError:
    from homeassistant.components.light import Light as LightEntity

from homeassistant.components.light import (ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS)

from . import ModernFormsBaseEntity
from .const import DOMAIN, DEVICES, CONF_FAN_HOST

async def async_setup_entry(hass, config_entry, async_add_devices):
  device = hass.data[DOMAIN][DEVICES][config_entry.data.get(CONF_FAN_HOST)]
  return async_add_devices([ModernFormsLight(hass, device)])

class ModernFormsLight(LightEntity, ModernFormsBaseEntity):
  def __init__(self, hass, device):
    ModernFormsBaseEntity.__init__(self, hass, device)

  @property
  def brightness(self):
    return round(255*self.device.lightBrightness()/100)

  @property
  def unique_id(self):
    return self.device.clientId()

  @property
  def name(self):
    return self.device.name + " Light"

  def turn_on(self, **kwargs):
    if ATTR_BRIGHTNESS in kwargs:
      br = round(100*kwargs[ATTR_BRIGHTNESS]/255)
      self.device.set_light_brightness(br)
    else:
      self.device.set_light_on()

  def turn_off(self, **kwargs) -> None:
    self.device.set_light_off()

  @property
  def is_on(self):
    return self.device.lightOn()

  @property
  def supported_features(self) -> int:
    return SUPPORT_BRIGHTNESS


