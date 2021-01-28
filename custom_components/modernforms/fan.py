from homeassistant.components.fan import (FanEntity, SPEED_OFF, SUPPORT_SET_SPEED, SUPPORT_DIRECTION)

from . import DOMAIN, DEVICES, ModernFormsBaseEntity, ModernFormsDevice

def setup_platform(hass, config, add_entities, discovery_info=None):
  entities = []

  for device in hass.data[DOMAIN][DEVICES]:
    entities.append(ModernFormsFan(hass, device))

  if len(entities) > 0:
    add_entities(entities)

class ModernFormsFan(FanEntity, ModernFormsBaseEntity):
  def __init__(self, hass, device):
    ModernFormsBaseEntity.__init__(self, hass, device)

  @property
  def name(self):
    return self.device.name

  def set_direction(self, direction: str) -> None:
    self.device.set_fan_direction(direction)
    
  def set_speed(self, speed: str) -> None:
    if speed == SPEED_OFF:
      self.device.set_fan_off()
    else:
      self.device.set_fan_speed(int(speed))

  def turn_on(self, speed: str = None, **kwargs) -> None:
    if speed is None:
      self.device.set_fan_on()
    else:
      self.set_speed(speed)

  def turn_off(self, **kwargs) -> None:
    self.device.set_fan_off()

  @property
  def is_on(self):
    return self.device.fanOn()

  @property
  def speed(self) -> str:
    if not self.device.fanOn():
      return SPEED_OFF
    return str(self.device.fanSpeed())

  @property
  def current_direction(self):
    return self.device.fanDirection()

  @property
  def speed_list(self) -> list:
    return [SPEED_OFF, "1","2","3","4","5","6"]

  @property
  def supported_features(self) -> int:
    return SUPPORT_SET_SPEED|SUPPORT_DIRECTION


