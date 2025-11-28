import logging
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_API_KEY): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    url = data[CONF_URL].rstrip("/")
    api_key = data[CONF_API_KEY]
    
    session = async_get_clientsession(hass)
    
    try:
        async with async_timeout.timeout(10):
            async with session.get(f"{url}/api/health") as response:
                if response.status != 200:
                    raise Exception("Cannot connect to Jotty")
    except Exception as err:
        _LOGGER.error("Error connecting to Jotty: %s", err)
        raise Exception("Cannot connect to Jotty") from err
    
    try:
        headers = {"x-api-key": api_key}
        async with async_timeout.timeout(10):
            async with session.get(f"{url}/api/summary", headers=headers) as response:
                if response.status == 401:
                    raise Exception("Invalid API key")
                elif response.status != 200:
                    raise Exception(f"API returned status {response.status}")
    except aiohttp.ClientError as err:
        _LOGGER.error("Error validating API key: %s", err)
        raise Exception("Cannot validate API key") from err
    
    return {"title": "Jotty Notes & Lists"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )