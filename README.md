[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://hacs.xyz/)

# ha-modernforms
Modern Forms Smart Fan Integration for Home Assistant

Modern Forms Smart Fans contain a WiFi module that can be controlled with basic json http posts.
The API was derived from the Moden Forms Android application.

The component creates a FanEntity and a LightEntity (if enabled)

## Installation

### HACS

To install using [HACS](https://hacs.xyz/), on the `Integrations` page, select the three-dot menu and add a `Custom Repository`. Enter `https://github.com/jimpastos/ha-modernforms`. 

### Manual

Create a directory in .homeassistant/custom_components/modernforms/ and place the files from this repo there.

## Configuration
On the integrations page, click "Add Integration" and search for "Modern Forms" and follow the prompts.

## Contributing

To test changes locally you can use [Docker Compose](https://docs.docker.com/compose/)

Start Home Assistant:
```bash
docker-compose up
```

This will create the normal `config` directory in `.config`. Once done, you probably will want to configure your logging:

```yaml
# .config/configuration.yaml
logger:
  default: info
```
