"""Platform for light integration."""
from __future__ import annotations

import logging

from switchbotpy import Bot
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA, SERVICE_TURN_ON)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_MAC, CONF_ID, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

# Validation of the bot configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC): cv.string,
    vol.Optional(CONF_NAME, default='bot'): cv.string,
    vol.Optional(CONF_ID, default='bot'): cv.positive_int,
    vol.Optional(CONF_PASSWORD): cv.string,
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the MySwitchBot platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    mac = config[CONF_MAC]
    name = config.get(CONF_NAME)
    id = config.get(CONF_ID)
    password = config.get(CONF_PASSWORD)

    bot = Bot(id, mac=mac, name=name)

    # Add devices
    add_entities([MySwitchBot(bot)])


class AwesomeLight(SwitchBotEntity):
    """Representation of an Awesome Light."""

    def __init__(self, bot) -> None:
        """Initialize an AwesomeLight."""
        self._bot = bot
        self._name = bot.name
        self._state = None
        self._battery_level = None
        self._firmware = None

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def battery_level(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._battery_level

    @property
    def firmware(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._firmware

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._bot.switch("1")
        self._state = True

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._bot.switch("0")
        self._state = False

    def update(self) -> None:
        """Fetch new state data for this light.

        {'battery': 96, 'firmware': 6.4, 'n_timers': 0, 'dual_state_mode': True, 'inverse_direction': False, 'hold_seconds': 0}
        """
        settings = self._bot.get_settings()
        self._battery_level = settings['battery']
        self._firmware = settings['firmware']
