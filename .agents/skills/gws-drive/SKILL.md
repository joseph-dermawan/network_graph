---
name: gws-drive
description: Use this skill whenever the user asks to list, fetch, search, or inspect files in Google Drive using the gws CLI. Trigger on phrases like "list drive files", "find file in drive", or "search workspace drive".
---

# Google Workspace Drive Operations

## Goal
Query and retrieve metadata or contents of Google Drive files via the `gws` terminal CLI.

## Instructions
1. Identify whether the user wants to list recent files or search by keyword.
2. To list recent files, run:
   `gws drive files list --params '{"pageSize": 10}'`
3. To search by name or query:
   `gws drive files list --params '{"q": "name contains \"<query>\""}'`
4. Parse the returned JSON payload and summarize file names, IDs, and MIME types in a clean Markdown table.

## Constraints
- Never delete (`rm` / `delete`) files from Drive without explicit, separate user confirmation.
- Always pass structured parameters via valid `--params` JSON strings.
