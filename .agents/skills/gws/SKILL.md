---
name: gws
description: Use this skill whenever the user wants to interact with Google Workspace services (Google Drive, Gmail, Google Sheets, Google Docs, Google Calendar, Tasks) using the gws CLI. Trigger on phrases like "gws", "google workspace", "gmail", "google sheets", "google docs", "google calendar", or "workspace cli".
---

# Google Workspace CLI (`gws`) Operations

## Goal
Query, inspect, and interact with Google Workspace services via the `gws` terminal CLI tool.

## Key Service Commands & Patterns

### 1. Google Drive (`gws drive`)
- **List Recent Files**:
  `gws drive files list --params '{"pageSize": 10}'`
- **Search Files by Name**:
  `gws drive files list --params '{"q": "name contains \"<query>\" and trashed = false"}'`
- **Get File Details**:
  `gws drive files get --params '{"fileId": "<file-id>"}'`
- **Export File**:
  `gws drive files export --params '{"fileId": "<file-id>", "mimeType": "application/pdf"}' --output "<path>"`.

### 2. Google Sheets (`gws sheets`)
- **Get Metadata**:
  `gws sheets spreadsheets get --params '{"spreadsheetId": "<spreadsheet-id>"}'`
- **Read Values**:
  `gws sheets spreadsheets values get --params '{"spreadsheetId": "<spreadsheet-id>", "range": "Sheet1!A1:E20"}'`

### 3. Google Docs (`gws docs`)
- **Get Document Text/Structure**:
  `gws docs documents get --params '{"documentId": "<document-id>"}'`

### 4. Gmail (`gws gmail`)
- **List Messages**:
  `gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'`
- **Read Message**:
  `gws gmail users messages get --params '{"userId": "me", "id": "<message-id>"}'`

### 5. Calendar (`gws calendar`)
- **List Upcoming Events**:
  `gws calendar events list --params '{"calendarId": "primary", "maxResults": 10}'`

### 6. Endpoint Schema Discovery (`gws schema`)
- Inspect any endpoint's supported parameters:
  `gws schema <service>.<resource>.<method>` (e.g., `gws schema drive.files.list`)

## Rules & Constraints
- Always construct valid JSON parameters for `--params`.
- Format returned JSON into user-friendly Markdown tables or clear summaries.
- Obtain explicit confirmation before performing write/delete/send operations.
