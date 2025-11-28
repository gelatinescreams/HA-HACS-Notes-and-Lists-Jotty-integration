import logging
from datetime import timedelta, datetime

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_URL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    url = entry.data[CONF_URL]
    api_key = entry.data[CONF_API_KEY]

    session = async_get_clientsession(hass)
    client = JottyClient(session, url, api_key)

    try:
        await client.test_connection()
    except Exception as err:
        _LOGGER.error("Failed to connect to Jotty: %s", err)
        raise ConfigEntryNotReady from err

    coordinator = JottyDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await async_setup_services(hass, client, coordinator)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_setup_services(hass: HomeAssistant, client, coordinator):
    
    last_refresh = {"time": datetime.min}
    
    def schedule_smart_refresh():
        now = datetime.now()
        if (now - last_refresh["time"]).total_seconds() > 0.5:
            last_refresh["time"] = now
            hass.async_create_task(coordinator.async_request_refresh())
    
    async def handle_create_note(call):
        title = call.data.get("title")
        content = call.data.get("content", "")
        category = "Home Assistant"
        
        try:
            await client.create_note(title, content, category)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to create note: %s", err)
            raise
    
    async def handle_update_note(call):
        note_id = call.data.get("note_id")
        title = call.data.get("title")
        content = call.data.get("content")
        category = "Home Assistant"
        
        try:
            await client.update_note(note_id, title, content, category)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to update note: %s", err)
            raise
    
    async def handle_delete_note(call):
        note_id = call.data.get("note_id")
        
        try:
            await client.delete_note(note_id)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete note: %s", err)
            raise
    
    async def handle_create_checklist(call):
        title = call.data.get("title")
        category = "Home Assistant"
        list_type = call.data.get("type", "simple")
        
        try:
            await client.create_checklist(title, category, list_type)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to create checklist: %s", err)
            raise
    
    async def handle_add_checklist_item(call):
        checklist_id = call.data.get("checklist_id")
        text = call.data.get("text")
        status = call.data.get("status")
        
        try:
            await client.add_checklist_item(checklist_id, text, status)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to add checklist item: %s", err)
            raise
    
    async def handle_check_item(call):
        checklist_id = call.data.get("checklist_id")
        item_index = call.data.get("item_index")
        
        try:
            await client.check_item(checklist_id, item_index)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to check item: %s", err)
            raise
    
    async def handle_uncheck_item(call):
        checklist_id = call.data.get("checklist_id")
        item_index = call.data.get("item_index")
        
        try:
            await client.uncheck_item(checklist_id, item_index)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to uncheck item: %s", err)
            raise
    
    async def handle_delete_checklist(call):
        checklist_id = call.data.get("checklist_id")
        
        try:
            await client.delete_checklist(checklist_id)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete checklist: %s", err)
            raise

    hass.services.async_register(DOMAIN, "create_note", handle_create_note)
    hass.services.async_register(DOMAIN, "update_note", handle_update_note)
    hass.services.async_register(DOMAIN, "delete_note", handle_delete_note)
    hass.services.async_register(DOMAIN, "create_checklist", handle_create_checklist)
    hass.services.async_register(DOMAIN, "add_checklist_item", handle_add_checklist_item)
    hass.services.async_register(DOMAIN, "check_item", handle_check_item)
    hass.services.async_register(DOMAIN, "uncheck_item", handle_uncheck_item)
    hass.services.async_register(DOMAIN, "delete_checklist", handle_delete_checklist)


class JottyClient:

    def __init__(self, session: aiohttp.ClientSession, url: str, api_key: str):
        self.session = session
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    async def test_connection(self):
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(
                    f"{self.url}/api/health"
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Health check failed with status {response.status}")
                    return await response.json()
        except aiohttp.ClientError as err:
            raise Exception(f"Connection error: {err}") from err

    async def get_summary(self):
        try:
            async with async_timeout.timeout(5):
                async with self.session.get(
                    f"{self.url}/api/summary",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching summary: {err}") from err

    async def get_checklists(self):
        try:
            async with async_timeout.timeout(5):
                async with self.session.get(
                    f"{self.url}/api/checklists",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching checklists: {err}") from err

    async def get_notes(self):
        try:
            async with async_timeout.timeout(5):
                async with self.session.get(
                    f"{self.url}/api/notes",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching notes: {err}") from err

    async def create_note(self, title: str, content: str = "", category: str = "Uncategorized"):
        data = {"title": title, "content": content, "category": category}
        async with async_timeout.timeout(5):
            async with self.session.post(
                f"{self.url}/api/notes",
                headers=self.headers,
                json=data
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def update_note(self, note_id: str, title: str = None, content: str = None, category: str = None):
        data = {}
        if title:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if category:
            data["category"] = category
            
        async with async_timeout.timeout(5):
            async with self.session.put(
                f"{self.url}/api/notes/{note_id}",
                headers=self.headers,
                json=data
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def delete_note(self, note_id: str):
        async with async_timeout.timeout(5):
            async with self.session.delete(
                f"{self.url}/api/notes/{note_id}",
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def create_checklist(self, title: str, category: str = "Uncategorized", list_type: str = "simple"):
        data = {"title": title, "category": category, "type": list_type}
        async with async_timeout.timeout(5):
            async with self.session.post(
                f"{self.url}/api/checklists",
                headers=self.headers,
                json=data
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def add_checklist_item(self, checklist_id: str, text: str, status: str = None):
        data = {"text": text}
        if status:
            data["status"] = status
            data["time"] = 0
            
        async with async_timeout.timeout(5):
            async with self.session.post(
                f"{self.url}/api/checklists/{checklist_id}/items",
                headers=self.headers,
                json=data
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def check_item(self, checklist_id: str, item_index: int):
        async with async_timeout.timeout(2):
            async with self.session.put(
                f"{self.url}/api/checklists/{checklist_id}/items/{item_index}/check",
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def uncheck_item(self, checklist_id: str, item_index: int):
        async with async_timeout.timeout(2):
            async with self.session.put(
                f"{self.url}/api/checklists/{checklist_id}/items/{item_index}/uncheck",
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def delete_checklist(self, checklist_id: str):
        async with async_timeout.timeout(5):
            async with self.session.delete(
                f"{self.url}/api/checklists/{checklist_id}",
                headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()


class JottyDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, client: JottyClient):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self):
        try:
            import asyncio
            summary_task = asyncio.create_task(self.client.get_summary())
            checklists_task = asyncio.create_task(self.client.get_checklists())
            notes_task = asyncio.create_task(self.client.get_notes())
            
            summary, checklists, notes = await asyncio.gather(
                summary_task, checklists_task, notes_task,
                return_exceptions=True
            )
            
            if isinstance(summary, Exception):
                _LOGGER.warning("Summary fetch failed: %s", summary)
                summary = {"summary": {}}
            if isinstance(checklists, Exception):
                _LOGGER.warning("Checklists fetch failed: %s", checklists)
                checklists = {"checklists": []}
            if isinstance(notes, Exception):
                _LOGGER.warning("Notes fetch failed: %s", notes)
                notes = {"notes": []}
            
            all_checklists = checklists.get("checklists", [])
            all_notes = notes.get("notes", [])
            
            ha_checklists = [
                c for c in all_checklists 
                if c.get("category", "").startswith("Home Assistant")
            ]
            ha_notes = [
                n for n in all_notes 
                if n.get("category", "").startswith("Home Assistant")
            ]
            
            return {
                "summary": summary.get("summary", {}),
                "ha_checklists": ha_checklists,
                "ha_notes": ha_notes,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err