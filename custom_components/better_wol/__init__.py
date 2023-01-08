"""Support for sending Wake-On-LAN magic packets."""
from functools import partial
import logging

import voluptuous as vol
import wakeonlan

from homeassistant.const import CONF_BROADCAST_ADDRESS, CONF_BROADCAST_PORT, CONF_MAC
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.discovery import async_load_platform
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_SEND_MAGIC_PACKET = "send_magic_packet"

WAKE_ON_LAN_SEND_MAGIC_PACKET_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_BROADCAST_ADDRESS): cv.string,
        vol.Optional(CONF_BROADCAST_PORT): cv.port,
    }
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup DoHome platform"""
    hass.async_create_task(
        async_load_platform(hass, "switch", DOMAIN, {}, config)
    )
    return True
