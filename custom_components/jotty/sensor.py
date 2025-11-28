from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import re
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    sensors = [
        JottySensor(coordinator, "total_notes", "Total Notes", "mdi:note-text"),
        JottySensor(coordinator, "total_checklists", "Total Checklists", "mdi:format-list-checks"),
        JottySensor(coordinator, "total_items", "Total Items", "mdi:checkbox-marked"),
        JottySensor(coordinator, "completed_items", "Completed Items", "mdi:check-all"),
        JottySensor(coordinator, "pending_items", "Pending Items", "mdi:clock-outline"),
        JottySensor(coordinator, "completion_rate", "Completion Rate", "mdi:percent"),
    ]
    
    async_add_entities(sensors)
    
    if "ha_entity_ids" not in hass.data[DOMAIN][entry.entry_id]:
        hass.data[DOMAIN][entry.entry_id]["ha_entity_ids"] = set()

    await coordinator.async_config_entry_first_refresh()
    await _update_ha_entities(hass, entry, coordinator, async_add_entities)
    
    def handle_update():
        hass.async_create_task(_update_ha_entities(hass, entry, coordinator, async_add_entities))
    
    entry.async_on_unload(coordinator.async_add_listener(handle_update))

async def _update_ha_entities(hass, entry, coordinator, async_add_entities):
    ha_notes = coordinator.data.get("ha_notes", [])
    ha_lists = coordinator.data.get("ha_checklists", [])
    
    _LOGGER.debug(f"Found {len(ha_notes)} HA notes and {len(ha_lists)} HA checklists")
    
    current_ids = {f"note_{n['id']}" for n in ha_notes}
    current_ids.update({f"list_{l['id']}" for l in ha_lists})
    
    tracked_ids = hass.data[DOMAIN][entry.entry_id]["ha_entity_ids"]
    
    new_ids = current_ids - tracked_ids
    if new_ids:
        new_entities = []
        
        for note in ha_notes:
            note_id = f"note_{note['id']}"
            if note_id in new_ids:
                new_entities.append(JottyNoteSensor(coordinator, note['id'], note['title']))
                _LOGGER.debug(f"Adding note sensor: {note['title']}")
        
        for checklist in ha_lists:
            list_id = f"list_{checklist['id']}"
            if list_id in new_ids:
                new_entities.append(JottyChecklistSensor(coordinator, checklist['id'], checklist['title']))
                _LOGGER.debug(f"Adding checklist sensor: {checklist['title']}")
        
        if new_entities:
            async_add_entities(new_entities)
            tracked_ids.update(new_ids)

class JottySensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, sensor_type, name, icon):
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"Jotty {name}"
        self._attr_unique_id = f"jotty_{sensor_type}"
        self._attr_icon = icon

    @property
    def native_value(self):
        ha_notes = self.coordinator.data.get("ha_notes", [])
        ha_lists = self.coordinator.data.get("ha_checklists", [])
        
        if self._sensor_type == "total_notes":
            return len(ha_notes)
        elif self._sensor_type == "total_checklists":
            return len(ha_lists)
        elif self._sensor_type == "total_items":
            total = 0
            for checklist in ha_lists:
                total += len(checklist.get("items", []))
            return total
        elif self._sensor_type == "completed_items":
            completed = 0
            for checklist in ha_lists:
                for item in checklist.get("items", []):
                    if item.get("completed", False):
                        completed += 1
            return completed
        elif self._sensor_type == "pending_items":
            total = 0
            completed = 0
            for checklist in ha_lists:
                items = checklist.get("items", [])
                total += len(items)
                completed += sum(1 for item in items if item.get("completed", False))
            return total - completed
        elif self._sensor_type == "completion_rate":
            total = 0
            completed = 0
            for checklist in ha_lists:
                items = checklist.get("items", [])
                total += len(items)
                completed += sum(1 for item in items if item.get("completed", False))
            return round((completed / total * 100) if total > 0 else 0, 1)
        
        return 0

    @property
    def extra_state_attributes(self):
        if self._sensor_type == "total_notes":
            return {"count": len(self.coordinator.data.get("ha_notes", []))}
        elif self._sensor_type == "total_checklists":
            return {"count": len(self.coordinator.data.get("ha_checklists", []))}
        
        return {}

class JottyNoteSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, note_id, title):
        super().__init__(coordinator)
        self.note_id = note_id
        self._title = title
        self._attr_name = f"Jotty Note: {title}"
        self._attr_unique_id = f"jotty_note_{note_id}"
        self._attr_icon = "mdi:note-text"

    @property
    def native_value(self):
        note = self._get_note()
        if note:
            return note['title']
        return self._title

    @property
    def extra_state_attributes(self):
        note = self._get_note()
        if note:
            return {
                "note_id": self.note_id,
                "content": note.get("content", ""),
                "category": note.get("category", ""),
                "updated": note.get("updatedAt", ""),
                "created": note.get("createdAt", ""),
            }
        return {
            "note_id": self.note_id,
            "content": "",
            "category": "Home Assistant",
        }

    @property
    def available(self):
        return self._get_note() is not None

    def _get_note(self):
        ha_notes = self.coordinator.data.get("ha_notes", [])
        for note in ha_notes:
            if note["id"] == self.note_id:
                return note
        return None

class JottyChecklistSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, checklist_id, title):
        super().__init__(coordinator)
        self.checklist_id = checklist_id
        self._title = title
        self._attr_name = f"Jotty List: {title}"
        self._attr_unique_id = f"jotty_list_{checklist_id}"
        self._attr_icon = "mdi:format-list-checks"

    @property
    def native_value(self):
        checklist = self._get_checklist()
        if checklist:
            completed = sum(1 for item in checklist.get("items", []) if item.get("completed", False))
            total = len(checklist.get("items", []))
            return f"{completed}/{total}"
        return "0/0"

    @property
    def extra_state_attributes(self):
        checklist = self._get_checklist()
        if checklist:
            items = checklist.get("items", [])
            completed = sum(1 for item in items if item.get("completed", False))
            total = len(items)
            
            return {
                "checklist_id": self.checklist_id,
                "title": checklist.get("title", self._title),
                "category": checklist.get("category", ""),
                "type": checklist.get("type", "simple"),
                "items": items,
                "completed": completed,
                "total": total,
                "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
                "updated": checklist.get("updatedAt", ""),
                "created": checklist.get("createdAt", ""),
            }
        return {
            "checklist_id": self.checklist_id,
            "title": self._title,
            "category": "Home Assistant",
            "items": [],
        }

    @property
    def available(self):
        return self._get_checklist() is not None

    def _get_checklist(self):
        ha_lists = self.coordinator.data.get("ha_checklists", [])
        for checklist in ha_lists:
            if checklist["id"] == self.checklist_id:
                return checklist
        return None