from datetime import timedelta
from homeassistant.const import (CONF_SCAN_INTERVAL)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.helpers.update_coordinator import (CoordinatorEntity, DataUpdateCoordinator , UpdateFailed)
from types import MethodType
from typing import Any
import logging
import httpx

from .const import DOMAIN, DEVICES, COORDINATORS, CONF_FAN_NAME, CONF_FAN_HOST, CONF_ENABLE_LIGHT

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

def setup(hass, config):
  hass.data[DOMAIN] = {}
  hass.data[DOMAIN][DEVICES] = {}
  hass.data[DOMAIN][COORDINATORS] = {}

  return True

async def async_setup_entry(hass, config_entry):
  fan = config_entry.data
  scan_interval = fan.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
  name = fan.get(CONF_FAN_NAME)
  host = fan.get(CONF_FAN_HOST)
  has_light = fan.get(CONF_ENABLE_LIGHT)

  device = ModernFormsDevice(name, host, scan_interval)
  device.set_session(get_async_client(hass, verify_ssl=False))
  coordinator = DataUpdateCoordinator(hass, _LOGGER, name="modernforms", update_method=device.update_status,update_interval=device.interval)

  # Ensure client id is set
  await coordinator.async_config_entry_first_refresh()

  hass.data[DOMAIN][DEVICES][host] = device
  hass.data[DOMAIN][COORDINATORS][host] = coordinator

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

class ModernFormsBaseEntity(CoordinatorEntity):
  def __init__(self, coordinator, device):
    super().__init__(coordinator)
    self.device = device

  async def perform_action_and_refresh(
      self, action: MethodType, *args: Any, **kwargs: Any
      ) -> bool:
    await action(*args, **kwargs)
    self.coordinator.async_set_updated_data(self.device.data)


  @property
  def device_state_attributes(self):
    return self.device.data

class ModernFormsDevice:
  def __init__(self, name, host, interval=CONF_SCAN_INTERVAL):
    self.url = "http://{}/mf".format(host)
    self.name = name
    self.data = {}
    self.subscribers = []
    self.interval = interval
    self._session = None

  def set_session(self, session):
      self._session = session

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

  async def set_fan_on(self):
    await self._send_request({"fanOn": 1})

  async def set_fan_off(self):
    await self._send_request({"fanOn": 0})

  async def set_fan_speed(self, speed):
    if speed < 1:
      speed = 1
    elif speed > 6:
      speed = 6
    await self._send_request({"fanOn": 1, "fanSpeed": speed})

  async def set_fan_direction(self, direction):
    await self._send_request({"fanDirection": direction})

  async def set_light_on(self):
    await self._send_request({"lightOn": 1})

  async def set_light_off(self):
    await self._send_request({"lightOn": 0})

  async def set_light_brightness(self, level):
    if level < 1:
      level = 1
    elif level > 100:
      level = 100
    await self._send_request({"lightOn": 1, "lightBrightness": level})

  async def update_status(self):
    await self._send_request({"queryDynamicShadowData": 1})

  async def _send_request(self, data):
    if not self._session:
      self._session = httpx.AsyncClient()
    r = await self._session.post(
        self.url,
        json=data
        )
    r.raise_for_status()
    self.data = r.json()
    return self.data
