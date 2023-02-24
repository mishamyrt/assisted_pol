"""Support for Assisted Power-On-LAN."""
# pylint: disable=unused-argument
from __future__ import annotations

import logging
import subprocess as sp
from datetime import datetime
from typing import Any

import voluptuous as vol
import wakeonlan

from homeassistant.components.switch import (
    PLATFORM_SCHEMA as PARENT_PLATFORM_SCHEMA,
    SwitchEntity,
)
from homeassistant.const import (
    CONF_BROADCAST_ADDRESS,
    CONF_BROADCAST_PORT,
    CONF_HOST,
    CONF_MAC,
    CONF_NAME,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Assisted PoL"
DEFAULT_PING_TIMEOUT = 1

PLATFORM_SCHEMA = PARENT_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_BROADCAST_ADDRESS): cv.string,
        vol.Optional(CONF_BROADCAST_PORT): cv.port,
        vol.Optional(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up a wake on lan switch."""
    broadcast_address: str | None = config.get(CONF_BROADCAST_ADDRESS)
    broadcast_port: int | None = config.get(CONF_BROADCAST_PORT)
    host: str | None = config.get(CONF_HOST)
    mac_address: str = config[CONF_MAC]
    name: str = config[CONF_NAME]

    add_entities(
        [
            BetterWolSwitch(
                hass,
                name,
                host,
                mac_address,
                broadcast_address,
                broadcast_port,
            )
        ],
        host is not None,
    )


class BetterWolSwitch(SwitchEntity):
    """Representation of a wake on lan switch."""
    _change_time = None

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        host: str | None,
        mac_address: str,
        broadcast_address: str | None,
        broadcast_port: int | None,
    ) -> None:
        """Initialize the WOL switch."""
        self._hass = hass
        self._attr_name = name
        self._host = host
        self._mac_address = mac_address
        self._broadcast_address = broadcast_address
        self._broadcast_port = broadcast_port
        self._state = False
        self._attr_assumed_state = host is None
        self._attr_should_poll = bool(not self._attr_assumed_state)
        self._attr_unique_id = dr.format_mac(mac_address)

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        service_kwargs: dict[str, Any] = {}
        if self._broadcast_address is not None:
            service_kwargs["ip_address"] = self._broadcast_address
        if self._broadcast_port is not None:
            service_kwargs["port"] = self._broadcast_port

        _LOGGER.info(
            "Send magic packet to mac %s (broadcast: %s, port: %s)",
            self._mac_address,
            self._broadcast_address,
            self._broadcast_port,
        )

        wakeonlan.send_magic_packet(self._mac_address, **service_kwargs)
        self._change_time = datetime.now()
        self._state = True
        self.async_write_ha_state()


    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the device off if an off script is present."""
        session = async_get_clientsession(self._hass)

        await session.post(
            f"http://{self._host}:1312/pol/sleep"
        )

        self._change_time = datetime.now()
        self._state = False

    def update(self) -> None:
        """Check if device is on and update the state.
        Only called if assumed state is false."""
        if self._change_time is not None:
            diff = datetime.now() - self._change_time
            if diff.total_seconds() < 10:
                return
        ping_cmd = [
            "ping",
            "-c",
            "1",
            "-W",
            str(DEFAULT_PING_TIMEOUT),
            str(self._host),
        ]

        status = sp.call(ping_cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        self._state = not bool(status)
