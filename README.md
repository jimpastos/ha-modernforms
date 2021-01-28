[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://hacs.xyz/)

# ha-modernforms
Modern Forms Smart Fan Integration for Home Assistant

Modern Forms Smart Fans contain a WiFi module that can be controlled with basic json http posts.
The API was derived from the Moden Forms Android application.

The component creates a FanEntity and a LightEntity (if enabled)

# Installation

## HACS

To install using [HACS](https://hacs.xyz/), on the `Integrations` page, select the three-dot menu and add a `Custom Repository`. Enter `https://github.com/jimpastos/ha-modernforms`. 

## Manual

Create a directory in .homeassistant/custom_components/modernforms/ and place the files from this repo there.

# Configuration
Add the following in your configuration.yaml. 
The light: value is optional and should be set to true if the fan has a light
An optional scan_interval: value can also be set per device, with the default being 10 seconds

```yaml
modernforms:
  - host: <ip of fan>
    name: <name>
    light: true
```
