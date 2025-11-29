# Jotty Notes & Lists for Home Assistant

Home Assistant/HACS integration for Jotty that enables you to manage notes and checklists directly from your Home Assistant dashboard.

![ha-hacs-jotty-preview](assets/ha-hacs-jotty-preview.gif)

### Basically it does this

- **Full Note Management**: Create, edit, and delete notes from Home Assistant
- **Checklist Support**: Create and manage both simple checklists and task lists
- **Real Time Synchronization**: Changes sync with your Jotty server automatically
- **Granule Notifications**: Every note, list and item is imported as an entity, giving you control over every detail
- **Demo Dashboard**: Pre built Lovelace dashboard with full functionality included
- **Statistics Tracking**: Monitor note counts, list completion rates, and more

### Requirements

- **Home Assistant**: Version 2024.1.0 or newer
- **Jotty**: A running [Jotty](https://github.com/fccview/jottyinstance)
- **API Key**: Valid [Jotty](https://github.com/fccview/jottyinstance) API key with read/write permissions
- **HACS**: Home Assistant Community Store for easy installation and updates
- **File Editor**: Studio Code Server or File Editor addon for configuration
- **Lovelace UI**: Standard Home Assistant frontend

### Before You Begin

You must create a category named "Home Assistant" in your [Jotty](https://github.com/fccview/jottyinstance) application:

1. Open [Jotty](https://github.com/fccview/jottyinstance) on mobile or desktop
2. Go to Notes section
3. Create a new category called "Home Assistant"
4. Go to Lists section
5. Create a new category called "Home Assistant"

This category is REQUIRED for the integration to work. All notes and lists created from Home Assistant will automatically use this category.

## Installation

Complete instructions are available in the [Jotty: Notes and lists for Home Assistant Installation Guide](INSTALLATION.md).

## Notification blueprint
*a ready made notficiation blueprint for this integration is available below*

[![Notification blueprint](https://community-assets.home-assistant.io/original/4X/d/7/6/d7625545838a4970873f3a996172212440b7e0ae.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/gelatinescreams/HA-HACS-Notes-and-Lists-Jotty-integration/refs/heads/main/blueprints/automation/jotty_notifications_blueprint.yaml)

## Usage

### Creating Notes

**Full interactive dashboard available in [Jotty: Notes and lists for Home Assistant Installation Guide](INSTALLATION.md)**:
1. Go to the Notes tab on your Jotty dashboard
2. Enter a title and content in the "New Note" section
3. Click "Create"
4. The note appears immediately in the "All Notes" section

**Via Service Call**:
```yaml
service: jotty.create_note
data:
  title: "My Note Title"
  content: "Note content goes here"
```

**Via Automation**:
```yaml
action:
  - service: jotty.create_note
    data:
      title: "Reminder: {{ now().strftime('%A') }}"
      content: "Do not forget to check the mail"
```

### Creating Checklists

**Full interactive dashboard available in [Jotty: Notes and lists for Home Assistant Installation Guide](INSTALLATION.md)**:
1. Go to the Lists tab
2. Enter a title and select type (simple or task)
3. Click "Create"
4. The list appears in your lists view

**Via Service Call**:
```yaml
service: jotty.create_checklist
data:
  title: "Shopping List"
  type: "simple"
```

### Managing Items

**Add Item to List**:
```yaml
service: jotty.add_checklist_item
data:
  checklist_id: "YOUR_CHECKLIST_ID"
  text: "Buy milk"
  status: "todo"  # Only for task lists
```

**Check Item**:
```yaml
service: jotty.check_item
data:
  checklist_id: "YOUR_CHECKLIST_ID"
  item_index: 0  # First item
```

**Uncheck Item**:
```yaml
service: jotty.uncheck_item
data:
  checklist_id: "YOUR_CHECKLIST_ID"
  item_index: 0
```

### Editing and Deleting

**Update Note**:
```yaml
service: jotty.update_note
data:
  note_id: "YOUR_NOTE_ID"
  title: "Updated Title"
  content: "Updated content"
```

**Delete Note**:
```yaml
service: jotty.delete_note
data:
  note_id: "YOUR_NOTE_ID"
```

**Delete Checklist**:
```yaml
service: jotty.delete_checklist
data:
  checklist_id: "YOUR_CHECKLIST_ID"
```

## Available Services

### jotty.create_note
Create a new note in Jotty.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | The title of the note |
| content | string | No | The content of the note |

### jotty.update_note
Update an existing note.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| note_id | string | Yes | The UUID of the note |
| title | string | No | New title for the note |
| content | string | No | New content for the note |

### jotty.delete_note
Delete a note from Jotty.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| note_id | string | Yes | The UUID of the note |

### jotty.create_checklist
Create a new checklist.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | The title of the checklist |
| type | string | No | Type: "simple" or "task" (default: "simple") |

### jotty.add_checklist_item
Add an item to a checklist.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| checklist_id | string | Yes | The UUID of the checklist |
| text | string | Yes | The text of the item |
| status | string | No | Status for task lists: "todo", "in_progress", "paused", "completed" |

### jotty.check_item
Mark a checklist item as completed.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| checklist_id | string | Yes | The UUID of the checklist |
| item_index | integer | Yes | The index of the item (0-based) |

### jotty.uncheck_item
Mark a checklist item as incomplete.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| checklist_id | string | Yes | The UUID of the checklist |
| item_index | integer | Yes | The index of the item (0-based) |

### jotty.delete_checklist
Delete a checklist from Jotty.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| checklist_id | string | Yes | The UUID of the checklist |

## Sensors are why we all do it

The integration creates multiple sensors for monitoring your Jotty data:

### Statistics Sensors

- **sensor.jotty_total_notes**: Total number of notes in the "Home Assistant" category
- **sensor.jotty_total_checklists**: Total number of checklists in the "Home Assistant" category
- **sensor.jotty_total_items**: Total number of items across all checklists
- **sensor.jotty_completed_items**: Number of completed items
- **sensor.jotty_pending_items**: Number of pending (incomplete) items
- **sensor.jotty_completion_rate**: Overall completion rate percentage

### Dynamic Sensors

The integration also creates individual sensors for each note and checklist:

- **sensor.jotty_note_[title]**: One sensor per note containing title, content, and metadata
- **sensor.jotty_list_[title]**: One sensor per checklist containing title, items, and statistics

Each sensor includes attributes with detailed information such as IDs, creation dates, update times, and item lists.

## Automation Examples

### Create Shopping List Every Sunday
```yaml
automation:
  - alias: "Create Weekly Shopping List"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: jotty.create_checklist
        data:
          title: "Shopping List {{ now().strftime('%B %d') }}"
          type: "simple"
```

### Reminder Note When Leaving Home
```yaml
automation:
  - alias: "Create Reminder When Leaving"
    trigger:
      - platform: state
        entity_id: person.your_name
        from: "home"
        to: "not_home"
    action:
      - service: jotty.create_note
        data:
          title: "Left Home Reminder"
          content: "You left home at {{ now().strftime('%I:%M %p') }}. Did you remember to lock the door?"
```

### Notify When Tasks Are Completed
```yaml
automation:
  - alias: "Notify on Task Completion"
    trigger:
      - platform: state
        entity_id: sensor.jotty_completion_rate
    condition:
      - condition: numeric_state
        entity_id: sensor.jotty_completion_rate
        above: 95
    action:
      - service: notify.mobile_app
        data:
          message: "Great job! You have completed {{ states('sensor.jotty_completed_items') }} tasks today!"
```

### Auto-Create Daily Task List
```yaml
automation:
  - alias: "Create Daily Tasks"
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: jotty.create_checklist
        data:
          title: "Tasks for {{ now().strftime('%A, %B %d') }}"
          type: "task"
      #- delay: "00:00:03"
      - service: jotty.add_checklist_item
        data:
          checklist_id: "{{ state_attr('sensor.jotty_total_checklists', 'last_created_id') }}"
          text: "Review daily schedule"
          status: "todo"
```

## Dashboard Overview

The included dashboard provides a complete interface for managing your notes and lists:

### Notes Tab
- Create new notes with title and content
- Edit existing notes using dropdown picker
- Delete notes with confirmation
- View all notes with timestamps
- See formatted content

### Lists Tab
- Create new checklists (simple or task type)
- Manage existing lists using dropdown picker
- Add items to selected list
- Toggle item completion status
- *Update task statuses. Coming Soon [Roadmap](#roadmap)*
- Delete lists with confirmation
- View progress bars and statistics

### Quick Actions Tab
- One tap creation of common note types
- Quick list templates
- Shopping list creator
- Daily task list creator
- Meal plan template
- Packing list template
- Force refresh button
- Update dropdowns button

### Statistics Tab
- Visual statistics cards
- Total notes count
- Total lists count
- Completion rate percentage
- Items completed counter
- Pending items counter
- Detailed statistics table

### Getting Help & Troubleshooting

- [Notes and lists for Home Assistant Installation Guide](INSTALLATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Acknowledgments

- [Home Assistant Community](https://www.home-assistant.io)  for excellent documentation and support
- [Jotty](https://jotty.page) developer for creating an amazing notes and lists application with API
- [HACS](https://www.hacs.xyz) for making custom integrations accessible to everyone

## Roadmap

- API update for advanced task lists from Jotty. All task list code is already done in anticipation of this api addition.
- Clean old notes and list from sensors (May not be possbile automatically)
- Advanced filtering and search
- Calendar integration for task deadlines