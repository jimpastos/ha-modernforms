import requests

from datetime import timedelta
from homeassistant.const import (CONF_SCAN_INTERVAL)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (async_call_later, async_track_time_interval)
import logging

from .const import DOMAIN, DEVICES, CONF_FAN_NAME, CONF_FAN_HOST, CONF_ENABLE_LIGHT

_LOGGER = logging.getLogger(__name__)

CONF_LIGHT = "light"
SCAN_INTERVAL = 60

def setup(hass, config):
  hass.data[DOMAIN] = {}
  hass.data[DOMAIN][DEVICES] = {}

  return True

async def async_setup_entry(hass, config_entry):
  fan = config_entry.data
  scan_interval = timedelta(seconds=fan.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL))
  name = fan.get(CONF_FAN_NAME)
  host = fan.get(CONF_FAN_HOST)
  has_light = fan.get(CONF_ENABLE_LIGHT)

  device = ModernFormsDevice(name, host, has_light, scan_interval)

  # Ensure client id is set
  await hass.async_add_executor_job(device.update_status)
  hass.data[DOMAIN][DEVICES][host] = device

  hass.async_create_task(
    hass.config_entries.async_forward_entry_setup(
      config_entry, "fan"
    )
  )

  if has_light:
    hass.async_create_task(
      hass.config_entries.async_forward_entry_setup(
        config_entry, "light"
      )
    )

  return True

class ModernFormsBaseEntity(Entity):
  def __init__(self, hass, device):
    self.hass = hass
    self.device = device
    self.device._attach(self)

    def update_action(time):
      device.update_status()

    async_call_later(hass, 0, update_action)
    self.poll = async_track_time_interval(hass, update_action, device.interval)

  def _device_updated(self):
    self.schedule_update_ha_state()

  @property
  def should_poll(self):
    return False

  @property
  def device_state_attributes(self):
    return self.device.data

class ModernFormsDevice:
  def __init__(self, name, host, has_light=False, interval=CONF_SCAN_INTERVAL):
    self.url = "http://{}/mf".format(host)
    self.name = name
    self.data = {}
    self.has_light = has_light
    self.subscribers = []
    self.interval = interval

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
    self._send_request({"queryDynamicShadowData": 1})

  def _send_request(self, data):
    r = requests.post(self.url, json=data)
    r.raise_for_status()
    self.data = r.json()
    self._notify()
