try:
    from homeassistant.components.light import LightEntity
except ImportError:
    from homeassistant.components.light import Light as LightEntity

from homeassistant.components.light import (ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS)

from . import DOMAIN, DEVICES, ModernFormsBaseEntity, ModernFormsDevice

def setup_platform(hass, config, add_entities, discovery_info=None):
  entities = []

  for device in hass.data[DOMAIN][DEVICES]:
    if device.has_light:
      entities.append(ModernFormsLight(hass, device))

  if len(entities) > 0:
    add_entities(entities)

class ModernFormsLight(LightEntity, ModernFormsBaseEntity):
  def __init__(self, hass, device):
    ModernFormsBaseEntity.__init__(self, hass, device)

  @property
  def brightness(self):
    return round(255*self.device.lightBrightness()/100)

  @property
  def name(self):
    return self.device.name

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


