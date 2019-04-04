import json
import requests

from datetime import timedelta
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_SCAN_INTERVAL)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (async_call_later, async_track_time_interval)
from homeassistant.helpers import discovery
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "modernforms"
DEVICES = "devices"
CONF_LIGHT = "light"
SCAN_INTERVAL = timedelta(seconds=10)

def setup(hass, config):
  hass.data[DOMAIN] = {}
  hass.data[DOMAIN][DEVICES] = []
  fans = config[DOMAIN]

  for fan in fans:
    scan_interval = fan.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    name = fan.get(CONF_NAME)
    host = fan.get(CONF_HOST)
    has_light = fan.get(CONF_LIGHT, False)
    hass.data[DOMAIN][DEVICES].append(ModernFormsDevice(hass, name, host, has_light, scan_interval))

  discovery.load_platform(hass, 'fan', DOMAIN, None, config)
  discovery.load_platform(hass, 'light', DOMAIN, None, config)
  return True


class ModernFormsBaseEntity(Entity):
  def __init__(self, hass, device):
    self.hass = hass
    self.device = device
    self.device._attach(self)
  
  def _device_updated(self):
    self.schedule_update_ha_state()

  @property
  def should_poll(self):
    return False

  @property
  def device_state_attributes(self):
    return self.device.data

class ModernFormsDevice:
  def __init__(self, hass, name, host, has_light, interval):
    self.url = "http://{}/mf".format(host)
    self.name = name
    self.data = {}
    self.has_light = has_light
    self.subscribers = []

    def update_action(time):
      self.update_status()

    async_call_later(hass, 0, update_action)
    self.poll = async_track_time_interval(hass, update_action, interval)

  def _attach(self, sub):
    self.subscribers.append(sub)

  def _notify(self):
    for sub in self.subscribers:
      sub._device_updated()

  def clientId(self):
    return self.data.get("clientId", None)

  def fanOn(self):
    return self.data.get("fanOn", False)

  def fanSpeed(self):
    return self.data.get("fanSpeed", None)

  def fanDirection(self):
    return self.data.get("fanDirection", None)

  def lightOn(self):
    return self.data.get("lightOn", False)

  def lightBrightness(self):
    return self.data.get("lightBrightness", 0);

  def set_fan_on(self):
    self._send_request({"fanOn": 1})
  
  def set_fan_off(self):
    self._send_request({"fanOn": 0})

  def set_fan_speed(self, speed):
    if speed < 1:
      speed = 1
    elif speed > 6:
      speed = 6
    self._send_request({"fanOn": 1, "fanSpeed": speed})

  def set_fan_direction(self, direction):
    self._send_request({"fanDirection": direction})

  def set_light_on(self):
    self._send_request({"lightOn": 1})
  
  def set_light_off(self):
    self._send_request({"lightOn": 0})

  def set_light_brightness(self, level):
    if level < 1:
      level = 1
    elif level > 100:
      level = 100
    self._send_request({"lightOn": 1, "lightBrightness": level})

  def update_status(self):
    self._send_request({"queryDynamicShadowData":1})

  def _send_request(self, data):
    r = requests.post(self.url, json=data)
    r.raise_for_status()
    self.data = r.json();
    self._notify()
