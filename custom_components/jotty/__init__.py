import asyncio
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
        
        _LOGGER.debug("Creating note: title=%s", title)
        try:
            result = await client.create_note(title, content, category)
            _LOGGER.debug("Create note result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to create note: %s", err)
            raise
    
    async def handle_update_note(call):
        note_id = call.data.get("note_id")
        title = call.data.get("title")
        content = call.data.get("content")
        category = "Home Assistant"
        
        _LOGGER.debug("Updating note: note_id=%s, title=%s", note_id, title)
        try:
            result = await client.update_note(note_id, title, content, category)
            _LOGGER.debug("Update note result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to update note: %s", err)
            raise
    
    async def handle_delete_note(call):
        note_id = call.data.get("note_id")
        
        _LOGGER.debug("Deleting note: note_id=%s", note_id)
        try:
            result = await client.delete_note(note_id)
            _LOGGER.debug("Delete note result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete note: %s", err)
            raise
    
    async def handle_create_checklist(call):
        title = call.data.get("title")
        category = "Home Assistant"
        list_type = call.data.get("type", "simple")
        
        _LOGGER.debug("Creating checklist: title=%s, type=%s", title, list_type)
        try:
            result = await client.create_checklist(title, category, list_type)
            _LOGGER.debug("Create checklist result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to create checklist: %s", err)
            raise
    
    async def handle_update_checklist(call):
        checklist_id = call.data.get("checklist_id")
        title = call.data.get("title")
        category = call.data.get("category", "Home Assistant")
        
        _LOGGER.debug("Updating checklist: checklist_id=%s, title=%s", checklist_id, title)
        try:
            result = await client.update_checklist(checklist_id, title, category)
            _LOGGER.debug("Update checklist result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to update checklist: %s", err)
            raise
    
    async def handle_add_checklist_item(call):
        checklist_id = call.data.get("checklist_id")
        text = call.data.get("text")
        status = call.data.get("status")
        parent_index = call.data.get("parent_index")
        
        _LOGGER.debug("Adding checklist item: checklist_id=%s, text=%s, status=%s, parent_index=%s", 
                     checklist_id, text, status, parent_index)
        try:
            result = await client.add_checklist_item(checklist_id, text, status, parent_index)
            _LOGGER.debug("Add checklist item result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to add checklist item: %s", err)
            raise
    
    async def handle_check_item(call):
        checklist_id = call.data.get("checklist_id")
        item_index = call.data.get("item_index")
        
        _LOGGER.debug("Checking item: checklist_id=%s, item_index=%s (type: %s)", 
                     checklist_id, item_index, type(item_index).__name__)
        try:
            result = await client.check_item(checklist_id, item_index)
            _LOGGER.debug("Check item result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to check item: %s", err)
            raise
    
    async def handle_uncheck_item(call):
        checklist_id = call.data.get("checklist_id")
        item_index = call.data.get("item_index")
        
        _LOGGER.debug("Unchecking item: checklist_id=%s, item_index=%s (type: %s)", 
                     checklist_id, item_index, type(item_index).__name__)
        try:
            result = await client.uncheck_item(checklist_id, item_index)
            _LOGGER.debug("Uncheck item result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to uncheck item: %s", err)
            raise
    
    async def handle_delete_checklist_item(call):
        checklist_id = call.data.get("checklist_id")
        item_index = call.data.get("item_index")
        
        _LOGGER.debug("Deleting checklist item: checklist_id=%s, item_index=%s", checklist_id, item_index)
        try:
            result = await client.delete_checklist_item(checklist_id, item_index)
            _LOGGER.debug("Delete checklist item result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete checklist item: %s", err)
            raise
    
    async def handle_delete_checklist(call):
        checklist_id = call.data.get("checklist_id")
        
        _LOGGER.debug("Deleting checklist: checklist_id=%s", checklist_id)
        try:
            result = await client.delete_checklist(checklist_id)
            _LOGGER.debug("Delete checklist result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete checklist: %s", err)
            raise

    async def handle_create_task(call):
        title = call.data.get("title")
        category = "Home Assistant"
        
        _LOGGER.debug("Creating task: title=%s", title)
        try:
            result = await client.create_task(title, category)
            _LOGGER.debug("Create task result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to create task: %s", err)
            raise

    async def handle_update_task(call):
        task_id = call.data.get("task_id")
        title = call.data.get("title")
        category = call.data.get("category", "Home Assistant")
        
        _LOGGER.debug("Updating task: task_id=%s, title=%s", task_id, title)
        try:
            result = await client.update_task(task_id, title, category)
            _LOGGER.debug("Update task result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to update task: %s", err)
            raise

    async def handle_delete_task(call):
        task_id = call.data.get("task_id")
        
        _LOGGER.debug("Deleting task: task_id=%s", task_id)
        try:
            result = await client.delete_task(task_id)
            _LOGGER.debug("Delete task result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete task: %s", err)
            raise

    async def handle_add_task_item(call):
        task_id = call.data.get("task_id")
        text = call.data.get("text")
        status = call.data.get("status", "todo")
        parent_index = call.data.get("parent_index")
        
        _LOGGER.debug("Adding task item: task_id=%s, text=%s, status=%s, parent_index=%s", 
                     task_id, text, status, parent_index)
        try:
            result = await client.add_task_item(task_id, text, status, parent_index)
            _LOGGER.debug("Add task item result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to add task item: %s", err)
            raise

    async def handle_update_task_item_status(call):
        task_id = call.data.get("task_id")
        item_index = call.data.get("item_index")
        status = call.data.get("status")
        
        _LOGGER.debug("Updating task item status: task_id=%s, item_index=%s, status=%s", 
                     task_id, item_index, status)
        try:
            result = await client.update_task_item_status(task_id, item_index, status)
            _LOGGER.debug("Update task item status result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to update task item status: %s", err)
            raise

    async def handle_delete_task_item(call):
        task_id = call.data.get("task_id")
        item_index = call.data.get("item_index")
        
        _LOGGER.debug("Deleting task item: task_id=%s, item_index=%s", task_id, item_index)
        try:
            result = await client.delete_task_item(task_id, item_index)
            _LOGGER.debug("Delete task item result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete task item: %s", err)
            raise

    async def handle_get_task_statuses(call):
        task_id = call.data.get("task_id")
        
        _LOGGER.debug("Getting task statuses: task_id=%s", task_id)
        try:
            result = await client.get_task_statuses(task_id)
            _LOGGER.debug("Get task statuses result: %s", result)
            return result
        except Exception as err:
            _LOGGER.error("Failed to get task statuses: %s", err)
            raise

    async def handle_create_task_status(call):
        task_id = call.data.get("task_id")
        status_id = call.data.get("status_id")
        label = call.data.get("label")
        color = call.data.get("color")
        order = call.data.get("order")
        
        _LOGGER.debug("Creating task status: task_id=%s, status_id=%s, label=%s", 
                     task_id, status_id, label)
        try:
            result = await client.create_task_status(task_id, status_id, label, color, order)
            _LOGGER.debug("Create task status result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to create task status: %s", err)
            raise

    async def handle_update_task_status(call):
        task_id = call.data.get("task_id")
        status_id = call.data.get("status_id")
        label = call.data.get("label")
        color = call.data.get("color")
        order = call.data.get("order")
        
        _LOGGER.debug("Updating task status: task_id=%s, status_id=%s", task_id, status_id)
        try:
            result = await client.update_task_status(task_id, status_id, label, color, order)
            _LOGGER.debug("Update task status result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to update task status: %s", err)
            raise

    async def handle_delete_task_status(call):
        task_id = call.data.get("task_id")
        status_id = call.data.get("status_id")
        
        _LOGGER.debug("Deleting task status: task_id=%s, status_id=%s", task_id, status_id)
        try:
            result = await client.delete_task_status(task_id, status_id)
            _LOGGER.debug("Delete task status result: %s", result)
            schedule_smart_refresh()
        except Exception as err:
            _LOGGER.error("Failed to delete task status: %s", err)
            raise

    hass.services.async_register(DOMAIN, "create_note", handle_create_note)
    hass.services.async_register(DOMAIN, "update_note", handle_update_note)
    hass.services.async_register(DOMAIN, "delete_note", handle_delete_note)
    hass.services.async_register(DOMAIN, "create_checklist", handle_create_checklist)
    hass.services.async_register(DOMAIN, "update_checklist", handle_update_checklist)
    hass.services.async_register(DOMAIN, "add_checklist_item", handle_add_checklist_item)
    hass.services.async_register(DOMAIN, "check_item", handle_check_item)
    hass.services.async_register(DOMAIN, "uncheck_item", handle_uncheck_item)
    hass.services.async_register(DOMAIN, "delete_checklist", handle_delete_checklist)
    hass.services.async_register(DOMAIN, "delete_checklist_item", handle_delete_checklist_item)
    hass.services.async_register(DOMAIN, "create_task", handle_create_task)
    hass.services.async_register(DOMAIN, "update_task", handle_update_task)
    hass.services.async_register(DOMAIN, "delete_task", handle_delete_task)
    hass.services.async_register(DOMAIN, "add_task_item", handle_add_task_item)
    hass.services.async_register(DOMAIN, "update_task_item_status", handle_update_task_item_status)
    hass.services.async_register(DOMAIN, "delete_task_item", handle_delete_task_item)
    hass.services.async_register(DOMAIN, "get_task_statuses", handle_get_task_statuses)
    hass.services.async_register(DOMAIN, "create_task_status", handle_create_task_status)
    hass.services.async_register(DOMAIN, "update_task_status", handle_update_task_status)
    hass.services.async_register(DOMAIN, "delete_task_status", handle_delete_task_status)


class JottyClient:

    def __init__(self, session: aiohttp.ClientSession, url: str, api_key: str):
        self.session = session
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    async def _make_request(self, method: str, endpoint: str, json_data: dict = None, include_content_type: bool = True):
        """Make an HTTP request with proper error handling and logging."""
        url = f"{self.url}{endpoint}"
        
        if include_content_type:
            headers = self.headers.copy()
        else:
            headers = {"x-api-key": self.api_key}
        
        _LOGGER.debug("Making %s request to %s with data: %s", method, url, json_data)
        
        try:
            async with async_timeout.timeout(30):
                if method == "GET":
                    async with self.session.get(url, headers=headers) as response:
                        return await self._handle_response(response, url)
                elif method == "POST":
                    async with self.session.post(url, headers=headers, json=json_data) as response:
                        return await self._handle_response(response, url)
                elif method == "PUT":
                    if json_data is not None:
                        async with self.session.put(url, headers=headers, json=json_data) as response:
                            return await self._handle_response(response, url)
                    else:
                        async with self.session.put(url, headers=headers) as response:
                            return await self._handle_response(response, url)
                elif method == "DELETE":
                    async with self.session.delete(url, headers=headers) as response:
                        return await self._handle_response(response, url)
        except asyncio.TimeoutError:
            _LOGGER.error("Request to %s timed out", url)
            raise
        except Exception as err:
            _LOGGER.error("Request to %s failed: %s", url, err)
            raise

    async def _handle_response(self, response, url):
        """Handle the HTTP response."""
        response_text = await response.text()
        _LOGGER.debug("Response from %s: status=%s, body=%s", url, response.status, response_text[:500])
        
        if response.status >= 400:
            _LOGGER.error("HTTP error %s from %s: %s", response.status, url, response_text)
            response.raise_for_status()
        
        try:
            return await response.json() if response_text else {"success": True}
        except:
            _LOGGER.debug("Response is not JSON, returning raw text")
            return {"success": True, "raw": response_text}

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
            async with async_timeout.timeout(10):
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
            async with async_timeout.timeout(10):
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
            async with async_timeout.timeout(10):
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
        return await self._make_request("POST", "/api/notes", data)

    async def update_note(self, note_id: str, title: str = None, content: str = None, category: str = None):
        data = {}
        if title:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if category:
            data["category"] = category
        return await self._make_request("PUT", f"/api/notes/{note_id}", data)

    async def delete_note(self, note_id: str):
        return await self._make_request("DELETE", f"/api/notes/{note_id}")

    async def create_checklist(self, title: str, category: str = "Uncategorized", list_type: str = "simple"):
        data = {"title": title, "category": category, "type": list_type}
        return await self._make_request("POST", "/api/checklists", data)

    async def update_checklist(self, checklist_id: str, title: str = None, category: str = None):
        data = {}
        if title:
            data["title"] = title
        if category:
            data["category"] = category
        return await self._make_request("PUT", f"/api/checklists/{checklist_id}", data)

    async def add_checklist_item(self, checklist_id: str, text: str, status: str = None, parent_index: str = None):
        data = {"text": text}
        if status:
            data["status"] = status
            data["time"] = 0
        if parent_index is not None:
            data["parentIndex"] = str(parent_index)
        return await self._make_request("POST", f"/api/checklists/{checklist_id}/items", data)

    async def check_item(self, checklist_id: str, item_index):
        # Convert item_index to string and ensure proper formatting
        idx = str(item_index).strip()
        _LOGGER.info("check_item called: checklist_id=%s, item_index=%s", checklist_id, idx)
        endpoint = f"/api/checklists/{checklist_id}/items/{idx}/check"
        return await self._make_request("PUT", endpoint, json_data=None, include_content_type=False)

    async def uncheck_item(self, checklist_id: str, item_index):
        # Convert item_index to string and ensure proper formatting
        idx = str(item_index).strip()
        _LOGGER.info("uncheck_item called: checklist_id=%s, item_index=%s", checklist_id, idx)
        endpoint = f"/api/checklists/{checklist_id}/items/{idx}/uncheck"
        return await self._make_request("PUT", endpoint, json_data=None, include_content_type=False)

    async def delete_checklist_item(self, checklist_id: str, item_index):
        idx = str(item_index).strip()
        _LOGGER.info("delete_checklist_item called: checklist_id=%s, item_index=%s", checklist_id, idx)
        return await self._make_request("DELETE", f"/api/checklists/{checklist_id}/items/{idx}")

    async def delete_checklist(self, checklist_id: str):
        _LOGGER.info("delete_checklist called: checklist_id=%s", checklist_id)
        return await self._make_request("DELETE", f"/api/checklists/{checklist_id}")

    async def get_tasks(self):
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(
                    f"{self.url}/api/tasks",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching tasks: {err}") from err

    async def get_task(self, task_id: str):
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(
                    f"{self.url}/api/tasks/{task_id}",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching task: {err}") from err

    async def create_task(self, title: str, category: str = "Home Assistant"):
        data = {"title": title, "category": category}
        return await self._make_request("POST", "/api/tasks", data)

    async def update_task(self, task_id: str, title: str = None, category: str = None):
        data = {}
        if title:
            data["title"] = title
        if category:
            data["category"] = category
        return await self._make_request("PUT", f"/api/tasks/{task_id}", data)

    async def delete_task(self, task_id: str):
        _LOGGER.info("delete_task called: task_id=%s", task_id)
        return await self._make_request("DELETE", f"/api/tasks/{task_id}")

    async def add_task_item(self, task_id: str, text: str, status: str = "todo", parent_index: str = None):
        data = {"text": text, "status": status}
        if parent_index is not None:
            data["parentIndex"] = str(parent_index)
        return await self._make_request("POST", f"/api/tasks/{task_id}/items", data)

    async def update_task_item_status(self, task_id: str, item_index, status: str):
        idx = str(item_index).strip()
        data = {"status": status}
        _LOGGER.info("update_task_item_status: task_id=%s, item_index=%s, status=%s", task_id, idx, status)
        return await self._make_request("PUT", f"/api/tasks/{task_id}/items/{idx}/status", data)

    async def delete_task_item(self, task_id: str, item_index):
        idx = str(item_index).strip()
        _LOGGER.info("delete_task_item: task_id=%s, item_index=%s", task_id, idx)
        return await self._make_request("DELETE", f"/api/tasks/{task_id}/items/{idx}")

    async def get_task_statuses(self, task_id: str):
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(
                    f"{self.url}/api/tasks/{task_id}/statuses",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("statuses", []) if isinstance(data, dict) else data
        except Exception as err:
            _LOGGER.debug("Error fetching task statuses for %s: %s", task_id, err)
            return []

    async def create_task_status(self, task_id: str, status_id: str, label: str, color: str = None, order: int = None):
        data = {"id": status_id, "label": label}
        if color:
            data["color"] = color
        if order is not None:
            data["order"] = order
        return await self._make_request("POST", f"/api/tasks/{task_id}/statuses", data)

    async def update_task_status(self, task_id: str, status_id: str, label: str = None, color: str = None, order: int = None):
        data = {}
        if label:
            data["label"] = label
        if color:
            data["color"] = color
        if order is not None:
            data["order"] = order
        return await self._make_request("PUT", f"/api/tasks/{task_id}/statuses/{status_id}", data)

    async def delete_task_status(self, task_id: str, status_id: str):
        return await self._make_request("DELETE", f"/api/tasks/{task_id}/statuses/{status_id}")


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
            summary_task = asyncio.create_task(self.client.get_summary())
            checklists_task = asyncio.create_task(self.client.get_checklists())
            notes_task = asyncio.create_task(self.client.get_notes())
            tasks_task = asyncio.create_task(self.client.get_tasks())
            
            summary, checklists, notes, tasks = await asyncio.gather(
                summary_task, checklists_task, notes_task, tasks_task,
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
            if isinstance(tasks, Exception):
                _LOGGER.warning("Tasks fetch failed: %s", tasks)
                tasks = {"tasks": []}
            
            all_checklists = checklists.get("checklists", [])
            all_notes = notes.get("notes", [])
            all_tasks = tasks.get("tasks", [])
            
            ha_checklists = [
                c for c in all_checklists 
                if c.get("category", "").startswith("Home Assistant")
            ]
            ha_notes = [
                n for n in all_notes 
                if n.get("category", "").startswith("Home Assistant")
            ]
            ha_tasks = [
                t for t in all_tasks 
                if t.get("category", "").startswith("Home Assistant")
            ]
            
            return {
                "summary": summary.get("summary", {}),
                "ha_checklists": ha_checklists,
                "ha_notes": ha_notes,
                "ha_tasks": ha_tasks,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err