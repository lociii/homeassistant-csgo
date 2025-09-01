from http import HTTPStatus
import logging

from aiohttp import web
import voluptuous as vol

from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.helpers import config_entry_flow
from homeassistant.components.webhook import async_register, async_unregister  # <— new

from .const import DOMAIN
from .gamestate import GameState
from .schema import WEBHOOK_SCHEMA

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, hass_config):
    """Set up the csgo_gamestate component."""
    return True


async def async_setup_entry(hass, entry):
    """Configure based on config entry."""
    async_register(
        hass,
        DOMAIN,
        "CS:GO game state listener",
        entry.data[CONF_WEBHOOK_ID],
        handle_webhook,
    )
    hass.data.setdefault(DOMAIN, GameState(hass=hass).dump())
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    return True


async def handle_webhook(hass, webhook_id, request):
    """Handle incoming webhook from CSGO."""
    try:
        data = WEBHOOK_SCHEMA(await request.json())
    except vol.MultipleInvalid as error:
        _LOGGER.warning(f"csgo: failed to parse message '{error.error_message}'")
        return web.Response(text="OK", status=HTTPStatus.OK)

    gamestate = GameState(hass=hass)
    gamestate.load(data=hass.data[DOMAIN])
    gamestate.update(data=data)
    hass.data[DOMAIN] = gamestate.dump()

    return web.Response(text="OK", status=HTTPStatus.OK)


# pylint: disable=invalid-name
async_remove_entry = config_entry_flow.webhook_async_remove_entry
