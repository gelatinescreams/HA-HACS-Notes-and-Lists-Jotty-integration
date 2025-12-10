# Jotty Home Assistant Integration Installation Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Method A: HACS (Recommended)](#installation-method-a-hacs-recommended)
3. [Installation Method B: Manual Installation](#installation-method-b-manual-installation)
4. [Post Installation Configuration](#post-installation-configuration)
5. [Verifying Installation](#verifying-installation)
6. [Known Issues](#known-issues)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing the Jotty integration, you must have:

1. **A Jotty Server Running**
   - A Jotty server instance accessible from your Home Assistant installation
   - Server URL (example: `http://10.200.80.100:1122` or `https://jotty.yourdomain.com`)
   - Valid API key from your Jotty server (starts with `ck_`)

2. **Home Assistant Community Store (HACS) Installed** (for HACS method)
   - HACS must be installed and configured
   - Visit https://hacs.xyz for HACS installation instructions

3. **File Editor** (recommended)
   - Needed for editing configuration files

4. **"Home Assistant" Category in Jotty**
   - Open your Jotty mobile or desktop app
   - Create a category called "Home Assistant" in BOTH Notes AND Lists
   - This category is **REQUIRED** for the integration to work

5. **Required Lovelace Plugins** (for prebuilt dashboard)
   - [Lovelace HTML card](https://github.com/PiotrMachowski/lovelace-html-card)
   - [Multiline Text Input Card](https://github.com/faeibson/lovelace-multiline-text-input-card)
   - These must be installed via HACS to use the prebuilt dashboard

## Installation Method A: HACS (Recommended)

### Step 1: Add Custom Repository to HACS

1. Open Home Assistant
2. Navigate to HACS in the sidebar
3. Click the three dots menu (top right)
4. Select "Custom repositories"
5. Add the repository:
   - **Repository URL**: `https://github.com/gelatinescreams/ha-jotty`
   - **Category**: Integration
6. Click "Add"

### Step 2: Install Jotty Integration

1. In HACS, click "Integrations"
2. Click the blue "Explore & Download Repositories" button
3. Search for "Jotty Notes & Lists"
4. Click on the integration
5. Click "Download"
6. Select the latest version
7. Click "Download" again
8. Restart Home Assistant:
   - Go to Settings > System > Restart
   - Wait for Home Assistant to fully restart (2-3 minutes)
9. Complete the Post Installation Configuration below for a full prebuilt dashboard

### Step 3: Configure the Integration

1. Go to Settings > Devices & Services
2. Click "Add Integration" (blue button, bottom right)
3. Search for "Jotty"
4. Enter your configuration:
   - **Jotty Server URL**: Your server URL (example: `http://192.168.1.100:1122`)
   - **API Key**: Your Jotty API key (starts with `ck_`)
5. Click "Submit"
6. If successful, the Jotty integration will appear in your integrations list

## Installation Method B: Manual Installation

### Step 1: Download Integration Files

1. Download the latest release from GitHub:
   - Visit: https://github.com/gelatinescreams/ha-jotty/releases
   - Download the latest .zip file
   - Extract the archive

### Step 2: Copy Files to Home Assistant

1. Access your Home Assistant configuration directory
   - This is where your `configuration.yaml` file is located
   - Location varies by installation type:
     - **Home Assistant OS**: Use File Editor or Samba share
     - **Home Assistant Container**: Direct file system access
     - **Home Assistant Core**: `/home/homeassistant/.homeassistant/`

2. Create the custom components directory if it does not exist:
   ```
   custom_components/jotty/
   ```

3. Copy all files from the extracted archive into this directory:
   ```
   custom_components/jotty/__init__.py
   custom_components/jotty/config_flow.py
   custom_components/jotty/const.py
   custom_components/jotty/sensor.py
   custom_components/jotty/manifest.json
   custom_components/jotty/services.yaml
   custom_components/jotty/strings.json
   custom_components/jotty/translations/en.json
   ```

### Step 3: Restart and Configure

1. Restart Home Assistant:
   - Settings > System > Restart
   - Wait 2-3 minutes for full restart

2. Add the integration:
   - Settings > Devices & Services > Add Integration
   - Search for "Jotty"
   - Enter server URL and API key
   - Click Submit

## Post Installation Configuration

After installing the integration, complete these configuration steps for full dashboard functionality.

### Step 1: Create Required Helper Entities

Helper entities are required for the dashboard and scripts to function. You can create them via the UI or configuration file.

#### Method A: Create Helpers via Configuration File (Recommended)

1. Open your `configuration.yaml` file
2. Copy the contents from `demo-dashboard/input_helpers.yaml`
3. Paste at the bottom of your `configuration.yaml` (do not overwrite existing content)
4. Save the file
5. Go to Developer Tools > YAML > Check Configuration
6. If valid, click "Restart"

#### Method B: Create Helpers via UI

Go to Settings > Devices & Services > Helpers and create each helper:

**Text Helpers** (Create 26 text helpers):

| Name | Entity ID | Max Length |
|------|-----------|------------|
| Note ID | `input_text.jotty_note_id` | 255 |
| Note Title | `input_text.jotty_note_title` | 255 |
| Note Content | `input_text.jotty_note_content` | 255 |
| Edit Note Title | `input_text.jotty_edit_note_title` | 255 |
| Edit Note Content | `input_text.jotty_edit_note_content` | 255 |
| Checklist ID | `input_text.jotty_checklist_id` | 255 |
| Checklist Title | `input_text.jotty_checklist_title` | 255 |
| Selected Checklist ID | `input_text.jotty_selected_checklist_id` | 255 |
| Selected Checklist Title | `input_text.jotty_selected_checklist_title` | 255 |
| Selected Checklist Type | `input_text.jotty_selected_checklist_type` | 50 |
| Item Text | `input_text.jotty_item_text` | 255 |
| Loading Item | `input_text.jotty_loading_item` | 100 |
| Task Title | `input_text.jotty_task_title` | 255 |
| Selected Task ID | `input_text.jotty_selected_task_id` | 255 |
| Selected Task Title | `input_text.jotty_selected_task_title` | 255 |
| Task Item Text | `input_text.jotty_task_item_text` | 255 |
| Parent Item Index | `input_text.jotty_parent_item_index` | 50 |
| New Status ID | `input_text.jotty_new_status_id` | 50 |
| New Status Label | `input_text.jotty_new_status_label` | 100 |
| New Status Color | `input_text.jotty_new_status_color` | 20 |
| Edit Status ID | `input_text.jotty_edit_status_id` | 50 |
| Edit Status Label | `input_text.jotty_edit_status_label` | 100 |
| Edit Status Color | `input_text.jotty_edit_status_color` | 20 |
| Editing Reminder ID | `input_text.jotty_editing_reminder_id` | 255 |
| Editing Reminder Type | `input_text.jotty_editing_reminder_type` | 20 |
| Editing Reminder Title | `input_text.jotty_editing_reminder_title` | 255 |

**Hidden Text Helpers** (for dashboard actions : Create 4):

| Name | Entity ID | Max Length |
|------|-----------|------------|
| Quick Action Data | `input_text.jotty_quick_action_data` | 255 |
| Quick Task Action Data | `input_text.jotty_quick_task_action_data` | 255 |
| Quick Delete Item Data | `input_text.jotty_quick_delete_item_data` | 255 |
| Kanban Action Data | `input_text.jotty_kanban_action_data` | 255 |

**Dropdown Helpers** (Create 12 dropdown helpers):

| Name | Entity ID | Options |
|------|-----------|---------|
| Checklist Type | `input_select.jotty_checklist_type` | simple, task |
| Task Status | `input_select.jotty_task_status` | todo, in_progress, paused, completed |
| Note Picker | `input_select.jotty_note_picker` | -- Pick a note -- |
| Checklist Picker | `input_select.jotty_checklist_picker` | -- Pick a checklist -- |
| Item Picker | `input_select.jotty_item_picker` | -- Select item -- |
| Item Status | `input_select.jotty_item_status` | -- Select status --, todo, in_progress, paused, completed |
| Task Picker | `input_select.jotty_task_picker` | -- Pick a task list -- |
| Task Item Picker | `input_select.jotty_task_item_picker` | -- Select task item -- |
| New Task Item Status | `input_select.jotty_new_task_item_status` | todo, in_progress, completed |
| Status Column Picker | `input_select.jotty_status_picker` | -- Select status -- |
| Remind Who | `input_select.jotty_reminder_target` | Nobody |
| Remind Every | `input_select.jotty_reminder_interval` | 30 minutes, 1 hour, 2 hours, 4 hours, 8 hours, 12 hours, Once a day |
| On Days | `input_select.jotty_reminder_days` | Weekdays, Weekends, Every day |

**Number Helpers** (Create 2 number helpers):

| Name | Entity ID | Min | Max | Step |
|------|-----------|-----|-----|------|
| Selected Item Index | `input_number.jotty_selected_item_index` | 0 | 1000 | 1 |
| New Status Order | `input_number.jotty_new_status_order` | 0 | 20 | 1 |

**Toggle Helpers** (Create 4 toggle helpers):

| Name | Entity ID | Default |
|------|-----------|---------|
| Item Completed | `input_boolean.jotty_item_completed` | off |
| Is Loading | `input_boolean.jotty_is_loading` | off |
| Enable Reminder | `input_boolean.jotty_enable_reminder` | off |
| Show Reminder Popup | `input_boolean.jotty_show_reminder_popup` | off |

**DateTime Helpers** (Create 2 time-only helpers):

| Name | Entity ID | Has Date | Has Time |
|------|-----------|----------|----------|
| From Time | `input_datetime.jotty_reminder_start` | No | Yes |
| Until Time | `input_datetime.jotty_reminder_end` | No | Yes |

**Template Sensors** (Add to configuration.yaml):

Add these template sensors at the bottom of your `configuration.yaml`:

```yaml
template:
  - trigger:
      - platform: homeassistant
        event: start
      - platform: event
        event_type: jotty_reminder_update
    sensor:
      - name: "Jotty Reminders"
        unique_id: jotty_reminders_storage
        state: >
          {% if trigger.platform == 'event' and trigger.event.data.configs is defined %}
            {{ trigger.event.data.configs | length }}
          {% else %}
            {{ this.attributes.configs | default({}) | length }}
          {% endif %}
        attributes:
          configs: >
            {% if trigger.platform == 'event' and trigger.event.data.configs is defined %}
              {{ trigger.event.data.configs }}
            {% else %}
              {{ this.attributes.configs | default({}) }}
            {% endif %}
            
  - trigger:
      - platform: homeassistant
        event: start
      - platform: time_pattern
        hours: "/6"
    sensor:
      - name: "Jotty Available Notifiers"
        unique_id: jotty_available_notifiers
        state: "{{ this.attributes.notifiers | default([]) | length }}"
        attributes:
          notifiers: >
            {% set devices = integration_entities('mobile_app') | select('match','device_tracker') | expand | map(attribute='name') | map('slugify') | list %}
            {% set ns = namespace(services=[]) %}
            {% for device in devices %}
              {% set ns.services = ns.services + ['notify.mobile_app_' ~ device] %}
            {% endfor %}
            {{ ns.services }}
```

### Step 2: Add Scripts

Scripts provide the functionality for the dashboard buttons and automation triggers.

1. Open your `scripts.yaml` file
2. Copy all contents from `demo-dashboard/scripts.yaml`
3. Paste at the bottom of your `scripts.yaml` file (do not overwrite existing content)
4. Save the file
5. Go to Developer Tools > YAML
6. Click "Scripts" under "Reload"

**Scripts Included:**

| Script | Description |
|--------|-------------|
| `jotty_create_note` | Create a new note |
| `jotty_update_note` | Update an existing note |
| `jotty_delete_note` | Delete a note |
| `jotty_save_edited_note` | Save changes to edited note |
| `jotty_delete_edited_note` | Delete note being edited |
| `jotty_delete_note_by_id` | Delete note by ID directly |
| `jotty_create_checklist` | Create a new checklist |
| `jotty_add_item` | Add item to checklist |
| `jotty_check_item` | Mark item as completed |
| `jotty_uncheck_item` | Mark item as incomplete |
| `jotty_delete_checklist` | Delete a checklist |
| `jotty_delete_checklist_item` | Delete a checklist item |
| `jotty_toggle_item_completion` | Toggle item complete/incomplete |
| `jotty_update_task_status` | Update task item status |
| `jotty_add_item_to_selected_list` | Add item to currently selected list |
| `jotty_quick_check_item` | Quick check item by index |
| `jotty_quick_uncheck_item` | Quick uncheck item by index |
| `jotty_create_task` | Create a new task list (Kanban) |
| `jotty_delete_task` | Delete a task list |
| `jotty_add_task_item` | Add item to task list |
| `jotty_update_task_item_status` | Change task item status |
| `jotty_delete_task_item` | Delete a task item |
| `jotty_load_task_statuses` | Load Kanban columns for a task |
| `jotty_create_kanban_status` | Add new Kanban column |
| `jotty_update_kanban_status` | Update Kanban column |
| `jotty_delete_kanban_status` | Delete Kanban column |
| `jotty_force_update_note_picker` | Refresh note dropdown |
| `jotty_force_update_checklist_picker` | Refresh checklist dropdown |
| `jotty_force_update_task_picker` | Refresh task dropdown |
| `jotty_update_both_dropdowns` | Update all dropdowns at once |
| `jotty_refresh_dashboard_data` | Refresh all dashboard data |
| `jotty_load_reminder` | Load reminder configuration for an item |
| `jotty_save_reminder` | Save reminder from popup dialog |
| `jotty_open_reminder_for_list` | Open reminder popup for a checklist |
| `jotty_open_reminder_for_task` | Open reminder popup for a task |
| `jotty_refresh_notifiers` | Refresh available notification services |
| `jotty_save_reminder_inline` | Save reminder via service call |
| `jotty_remove_reminder_inline` | Remove reminder via service call |
| `jotty_update_last_sent` | Update last sent timestamp for reminder |
| `jotty_send_note_to_devices` | Send note content to mobile devices |

### Step 3: Add Automations

Automations keep the dashboard synchronized with your Jotty data.

1. Open your `automations.yaml` file
2. Copy all contents from `demo-dashboard/automations.yaml`
3. Paste at the bottom of your `automations.yaml` file (do not overwrite existing content)
4. Save the file
5. Go to Developer Tools > YAML
6. Click "Automations" under "Reload"

**Automations Included:**

| Automation | Description |
|------------|-------------|
| `jotty_auto_update_note_picker` | Auto refresh note dropdown when notes change |
| `jotty_auto_update_checklist_picker` | Auto- efresh checklist dropdown |
| `jotty_auto_update_task_picker` | Auto refresh task dropdown |
| `jotty_load_note_when_picked` | Load note data when selected |
| `jotty_load_checklist_when_picked` | Load checklist data when selected |
| `jotty_load_checklist_items` | Load items for selected checklist |
| `jotty_load_item_details` | Load item details when selected |
| `jotty_load_task_when_picked` | Load task data when selected |
| `jotty_load_task_items` | Load items for selected task |
| `jotty_quick_list_actions` | Handle quick actions from dashboard |
| `jotty_quick_task_actions` | Handle task actions from dashboard |
| `jotty_quick_delete_item` | Handle item deletion from dashboard |
| `jotty_kanban_actions` | Handle Kanban column management |
| `jotty_load_reminder_on_popup` | Load reminder config when popup opens |
| `jotty_close_reminder_popup` | Clear reminder data when popup closes |
| `jotty_check_reminders` | Check reminders every 30 minutes and send notifications |
| `jotty_handle_notification_actions` | Handle snooze/open actions from notifications |

### Step 4: Add Dashboard

The prebuilt Lovelace dashboard provides a complete user interface.

1. Go to your Lovelace dashboard
2. Click the three dots menu (top right)
3. Select "Edit Dashboard"
4. Click the three dots menu again
5. Select "Raw configuration editor"
6. **Back up your current configuration first!**
7. Copy all contents from `demo-dashboard/demo-dashboard.yaml`
8. Paste into the editor (or create a new view)
9. Click "Save"
10. Exit edit mode

**Dashboard Features:**

| Tab | Features |
|-----|----------|
| **Notes** | Create, edit, delete notes; view all notes with timestamps; send notes to devices |
| **Lists** | Create checklists; add/check/uncheck items; delete items; progress tracking; set reminders |
| **Tasks** | Create Kanban boards; add tasks with status; add sub tasks; manage columns; set reminders |
| **Quick Actions** | One tap templates for common lists and notes |
| **Statistics** | Total counts, completion rates, visual progress |



## Verifying Installation

After completing all steps, verify the integration is working:

### 1. Check Integration Status

- Go to Settings > Devices & Services
- Find "Jotty Notes & Lists"
- Should show "Configured" status

### 2. Check Sensors

Go to Developer Tools > States and search for "jotty". You should see:

| Sensor | Description |
|--------|-------------|
| `sensor.jotty_total_notes` | Total notes count |
| `sensor.jotty_total_checklists` | Total checklists count |
| `sensor.jotty_total_tasks` | Total task lists count |
| `sensor.jotty_total_items` | Total items across all lists |
| `sensor.jotty_completed_items` | Completed items count |
| `sensor.jotty_pending_items` | Pending items count |
| `sensor.jotty_completion_rate` | Overall completion percentage |
| `sensor.jotty_reminders` | Reminder configurations storage |
| `sensor.jotty_available_notifiers` | Available mobile app notifiers |

Plus individual sensors for each note (`sensor.jotty_note_*`), checklist (`sensor.jotty_list_*`), and task (`sensor.jotty_task_*`).

### 3. Test Basic Functions

**Test Creating a Note:**
1. Go to your Jotty dashboard
2. Under "Notes" section, enter a title and content
3. Click "Create"
4. The note should appear in 2-3 seconds

**Test Creating a Checklist:**
1. Under "Lists" section, enter a title
2. Click "Create"
3. Add items using the text field

**Test Creating a Task List:**
1. Under "Tasks" section, enter a title
2. Click "Create"
3. Add task items with status selection
4. Use ⚙️ Columns to customize Kanban columns

**Test Reminder System:**
1. Create a checklist with at least one item
2. Click the 🔔 button on the list
3. Enable the reminder and configure settings
4. Save and verify `sensor.jotty_reminders` has the configuration

### 4. Verify in Jotty App

- Open your Jotty mobile or desktop app
- Check the "Home Assistant" category
- Your test items should be visible

## Known Issues

### Task Item Status Not Persisting

**Issue**: The `jotty.update_task_item_status` service returns success but the status change is not saved by the Jotty API.

**Affected Operations**:
- Moving items between Kanban columns via status dropdown
- Both top level and nested items affected

**Workaround**: 
- Create items with the correct initial status
- To change status: delete and recreate the item with new status

**Status**: Bug reported to Jotty developer. All other API operations work correctly.

## Troubleshooting

### Integration Not Found

- Ensure HACS installed the integration
- Restart Home Assistant completely
- Check `custom_components/jotty/` exists with all files

### "Home Assistant" Category Not Found

- Open Jotty app
- Create category named exactly "Home Assistant" (case-sensitive)
- Must exist in BOTH Notes AND Lists sections

### Sensors Show "Unavailable"

- Check Jotty server is running and accessible
- Verify API key is correct (starts with `ck_`)
- Check Home Assistant logs for connection errors

### Dashboard Not Working

- Verify all helper entities are created
- Reload scripts and automations after adding them
- Check browser console for JavaScript errors
- Ensure required Lovelace plugins are installed

### Dropdowns Empty or Not Updating

- Run the force update scripts:
  - `script.jotty_force_update_note_picker`
  - `script.jotty_force_update_checklist_picker`
  - `script.jotty_force_update_task_picker`
- Check automations are enabled

### Sub tasks Not Appearing

- Ensure using `flat_items` attribute (not `items`) for nested display
- Each item has `index_path` attribute (e.g., "0", "0.1", "0.1.2")

### Reminders Not Working

- Verify `sensor.jotty_reminders` exists and has `configs` attribute
- Check `sensor.jotty_available_notifiers` lists your devices
- Run `script.jotty_refresh_notifiers` to update device list
- Ensure automations `jotty_check_reminders` is enabled
- Check Home Assistant logs for notification errors

### Template Sensors Not Creating

- Verify the template sensor configuration is correctly formatted
- Check for YAML syntax errors in Developer Tools > YAML > Check Configuration
- Ensure templates are at the root level (not nested under another key)
- Restart Home Assistant after adding template sensors

## Getting Help

- [Usage Guide](README.md)
- [GitHub Issues](https://github.com/gelatinescreams/ha-jotty/issues)
- [Home Assistant Community Forum](https://community.home-assistant.io)

## Additional Resources

- Home Assistant Documentation: https://www.home-assistant.io/docs/
- HACS Documentation: https://hacs.xyz
- Jotty Documentation: https://jotty.page