## Table of Contents

1. Prerequisites
2. Installation Method A: HACS (Recommended)
3. Installation Method B: Manual Installation
4. Post Installation Configuration (Required for prebuilt lovelace dashboard)
5. Troubleshooting

## Prerequisites

Before installing the Jotty integration, you must have:

1. **A Jotty Server Running**
   - A Jotty server instance accessible from your Home Assistant installation
   - Server URL (example: http://10.200.80.100:1122 or https://jotty.yourdomain.com)
   - Valid API key from your Jotty server (starts with ck_)

2. **Home Assistant Community Store (HACS) Installed** (for HACS method)
   - HACS must be installed and configured
   - Visit https://hacs.xyz for HACS installation instructions

3. **File Editor** (recommended)
   - Needed for editing configuration files

4. **"Home Assistant" Category in Jotty**
   - Open your Jotty mobile or desktop app
   - Create a category called "Home Assistant" in BOTH Notes and Lists
   - This category is REQUIRED for the integration to work
  
4. **"Prebuilt Lovelace dashboard requires the VERY FINE work of these plugins**
   - [Lovelace HTML card](https://github.com/PiotrMachowski/lovelace-html-card)
   - [Multiline Text Input Card](https://github.com/faeibson/lovelace-multiline-text-input-card)
   - *these must be installed to use the prebuilt dashboard*

## Installation Method A: HACS (Recommended)

### Step 1: Add Custom Repository to HACS

1. Open Home Assistant
2. Navigate to HACS in the sidebar
3. Click the three dots menu (top right)
4. Select "Custom repositories"
5. Add the repository:
   - **Repository URL**: https://github.com/gelatinescreams/ha-jotty
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

### Step 3: Configure the Integration

1. Go to Settings > Devices & Services
2. Click "Add Integration" (blue button, bottom right)
3. Search for "Jotty"
4. Enter your configuration:
   - **Jotty Server URL**: Your server URL (example: http://192.168.1.100:1122)
   - **API Key**: Your Jotty API key (starts with ck_)
5. Click "Submit"
6. If successful, the Jotty integration will appear in your integrations list
7. Complete the "Post Installation Configuration" for ready to use scripts, automations, helpers and a full featured dashboard.
8. *Post Installation Configuration must be completed for use of the prebuilt lovelace dashboard*

## Installation Method B: Manual Installation

### Step 1: Download Integration Files

1. Download the latest release from GitHub:
   - Visit: https://github.com/gelatinescreams/ha-jotty/releases
   - Download the latest .zip file
   - Extract the archive

### Step 2: Copy Files to Home Assistant

1. Access your Home Assistant configuration directory
   - This is where your configuration.yaml file is located
   - Location varies by installation type:
     - **Home Assistant OS**: Use File Editor or Samba share
     - **Home Assistant Container**: Direct file system access
     - **Home Assistant Core**: /home/homeassistant/.homeassistant/

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

After installing the integration, you must complete these additional configuration steps for full functionality.

### Step 1: Create Required Helper Entities

Helper entities are required for the dashboard and scripts to function. You can create them via the UI or configuration file.

#### Method A: Create Helpers via UI

1. Go to Settings > Devices & Services > Helpers
2. Click "Create Helper" (blue button, bottom right)
3. Create each helper as specified below

**Text Helpers** (Create 11 text helpers):

| Name | Entity ID | Max Length |
|------|-----------|------------|
| Jotty Note ID | input_text.jotty_note_id | 255 |
| Jotty Note Title | input_text.jotty_note_title | 255 |
| Jotty Note Content | input_text.jotty_note_content | 5000 |
| Jotty Edit Note Title | input_text.jotty_edit_note_title | 255 |
| Jotty Edit Note Content | input_text.jotty_edit_note_content | 5000 |
| Jotty Checklist ID | input_text.jotty_checklist_id | 255 |
| Jotty Checklist Title | input_text.jotty_checklist_title | 255 |
| Jotty Selected Checklist ID | input_text.jotty_selected_checklist_id | 255 |
| Jotty Selected Checklist Title | input_text.jotty_selected_checklist_title | 255 |
| Jotty Selected Checklist Type | input_text.jotty_selected_checklist_type | 50 |
| Jotty Item Text | input_text.jotty_item_text | 500 |
| Jotty Item Index | input_text.jotty_item_index | 10 |

**Dropdown Helpers** (Create 6 dropdown helpers):

| Name | Entity ID | Options |
|------|-----------|---------|
| Jotty Checklist Type | input_select.jotty_checklist_type | simple, task |
| Jotty Task Status | input_select.jotty_task_status | todo, in_progress, paused, completed |
| Jotty Note Picker | input_select.jotty_note_picker | -- Pick a note -- |
| Jotty Checklist Picker | input_select.jotty_checklist_picker | -- Pick a checklist -- |
| Jotty Item Picker | input_select.jotty_item_picker | -- Select item -- |
| Jotty Item Status | input_select.jotty_item_status | -- Select status --, todo, in_progress, paused, completed |

**Number Helper** (Create 1 number helper):

| Name | Entity ID | Min | Max | Step |
|------|-----------|-----|-----|------|
| Jotty Selected Item Index | input_number.jotty_selected_item_index | 0 | 1000 | 1 |

**Toggle Helper** (Create 1 toggle helper):

| Name | Entity ID |
|------|-----------|
| Jotty Item Completed | input_boolean.jotty_item_completed |

#### Method B: Create Helpers via Configuration File

1. Open your configuration.yaml file
2. If you do not already have sections for input_text, input_select, input_number, and input_boolean, add them *(DO NOT OVERWRITE YOUR CURRENT FILE. ADD THESE AT THE END)*
3. Copy the contents from demo-dashboard/input_helpers.yaml into your configuration.yaml
4. Save the file
5. Go to Developer Tools > YAML > Restart (under Configuration validation)
6. Check for errors, then click "Restart"

### Step 2: Add Scripts

Scripts provide the functionality to create, edit, and delete notes and checklists.

1. Open your scripts.yaml file (or create it if it does not exist) 
2. Copy all contents from demo-dashboard/scripts.yaml *(DO NOT OVERWRITE YOUR CURRENT FILE. ADD THESE AT THE END)*
3. Paste at the bottom of your scripts.yaml file
4. Save the file
5. Go to Developer Tools > YAML
6. Click "Restart" under "Scripts"

### Step 3: Add Automations

Automations keep the dashboard synchronized with your Jotty data.

1. Open your automations.yaml file (or use the UI)
2. Copy all contents from demo-dashboard/automations.yaml *(DO NOT OVERWRITE YOUR CURRENT FILE. ADD THESE AT THE END)*
3. Paste at the bottom of your automations.yaml file
4. Save the file
5. Go to Developer Tools > YAML
6. Click "Restart" under "Automations"

### Step 4: Add Dashboard

The prebuilt lovelace dashboard provides a user interface for managing notes and lists.

1. Go to your Lovelace dashboard
2. Click the three dots menu (top right)
3. Select "Edit Dashboard"
4. Click the three dots menu again
5. Select "Raw configuration editor"
6. Copy all contents from demo-dashboard/demo-dashboard.yaml
7. Paste into the editor (this will replace your existing dashboard, so back it up first)
8. Alternatively, create a new view and paste the content there
9. Click "Save"
10. Exit edit mode

## Verifying Installation

After completing all steps, verify the integration is working:

1. **Check Integration Status**:
   - Go to Settings > Devices & Services
   - Find "Jotty Notes & Lists"
   - Should show "Configured" status

2. **Check Sensors**:
   - Go to Developer Tools > States
   - Search for "jotty"
   - You should see sensors like:
     - sensor.jotty_total_notes
     - sensor.jotty_total_checklists
     - sensor.jotty_total_items
     - sensor.jotty_completed_items
     - sensor.jotty_pending_items
     - sensor.jotty_completion_rate

3. **Test Creating a Note**:
   - Go to your Jotty dashboard
   - Under "New Note" section:
     - Enter a title
     - Enter some content
     - Click "Create"
   - Wait 2-3 seconds
   - The note should appear in the "All Notes" section

4. **Test Creating a Checklist**:
   - Under "New List" section:
     - Enter a title
     - Select type (simple or task)
     - Click "Create"
   - Wait 2-3 seconds
   - The list should appear

5. **Verify in Jotty App**:
   - Open your Jotty mobile or desktop app
   - Check the "Home Assistant" category
   - Your test note and list should be visible there

### Getting Help & Troubleshooting

- [Jotty: Notes and lists for Home Assistant Installation Guide](INSTALLATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Additional Resources

- Home Assistant Documentation: https://www.home-assistant.io/docs/
- HACS Documentation: https://hacs.xyz
- Jotty Documentation: https://jotty.page
- Home Assistant Community Forum: https://community.home-assistant.io
