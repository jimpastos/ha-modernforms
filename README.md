# ha-modernforms
Modern Forms Smart Fan Integration for Home Assistant

Modern Forms Fans contain a WiFi module that can be controlled with basic json http posts.
The API was derived from the Moden Forms Android application.

The component creates a Light and FanEntity (if enabled)

# Installation
Create a directory in .homeassistant/custom_components/modernforms/ and place the files from this repo there.

# Configuration
Add the following in your configuration.yaml. The light: value is optional and should be set to true if the fan has a light
```
modernforms:
  - host: <ip of fan>
    name: <name>
    light: true
