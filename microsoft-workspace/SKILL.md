---
name: microsoft-workspace
description: Outlook Calendar, Email, Contacts, and To-Do integration via Microsoft Graph API. Uses OAuth2 with automatic token refresh. Supports Hotmail/Outlook/Microsoft 365 accounts.
version: 1.2.0
author: hermes-community
license: MIT
required_credential_files:
  - path: microsoft_token.json
    description: Microsoft OAuth2 token (created by setup script)
  - path: microsoft_client_secret.json
    description: Microsoft app credentials (from Azure Portal)
metadata:
  hermes:
    tags: [Microsoft, Outlook, Calendar, Email, OneDrive, Graph API, OAuth, Hotmail]
---

# Microsoft Workspace (Outlook/Hotmail)

Outlook Calendar, Email, Contacts, and To-Do integration via Microsoft Graph API.

## Quick Setup

```bash
# Save credentials
./scripts/auth.sh --client-id "YOUR_CLIENT_ID" --client-secret "YOUR_CLIENT_SECRET"

# Get auth URL and authorize
python3 scripts/setup.py --auth-url
python3 scripts/setup.py --auth-code "PASTE_REDIRECT_URL"

# Verify
./scripts/auth.sh --check
```

See `README.md` for full Azure App Registration setup instructions.

## Scripts

- `scripts/microsoft_api.py` -- API wrapper CLI
- `scripts/setup.py` -- OAuth2 setup (run once to authorize)
- `scripts/auth.sh` -- Credential management and auth verification
- `scripts/safe_mail_send.sh` -- Preview emails before sending (prevents $ mangling and duplicates)

## Usage

```bash
GAPI="python3 ~/.hermes/skills/productivity/microsoft-workspace/scripts/microsoft_api.py"

# --- CALENDAR ---

# List upcoming events (default)
$GAPI calendar list
$GAPI calendar list --all
$GAPI calendar list --start 2026-04-10T00:00:00 --end 2026-04-10T23:59:59

# Create event (auto-adds Teams link)
$GAPI calendar create --summary "Meeting" --start "2026-04-10T15:00:00-04:00" --end "2026-04-10T15:30:00-04:00" --description "Syncing on ideas" --attendees "john@example.com"

# Create invite with video link (uses branded HTML template if configured)
$GAPI calendar invite --summary "Project Sync" --start "2026-04-11T14:00:00-04:00" --end "2026-04-11T14:30:00-04:00" --description "Let's discuss" --attendees "john@example.com" --meet

# Update an existing event (partial -- only update what you pass)
$GAPI calendar update EVENT_ID --summary "New Title"
$GAPI calendar update EVENT_ID --start "2026-04-11T16:00:00-04:00" --end "2026-04-11T16:30:00-04:00"

# Delete event
$GAPI calendar delete EVENT_ID

# Check free/busy status for people
$GAPI calendar freebusy --emails "user@example.com,other@example.com" --start "2026-04-14T09:00:00-04:00" --end "2026-04-14T17:00:00-04:00" --interval 30

# Find open slots where all attendees are free
$GAPI calendar findopen --emails "user@example.com" --start "2026-04-14T09:00:00-04:00" --end "2026-04-14T17:00:00-04:00" --duration 30 --interval 15

# --- EMAIL ---

# List emails (add --unread for unread only, --important for high importance)
$GAPI mail list --max 10
$GAPI mail list --unread
$GAPI mail list --important --folder archive

# Search emails by keyword
$GAPI mail search --query "invoice" --max 5
$GAPI mail search --query "project report" --folder sent

# Get full email content
$GAPI mail get MESSAGE_ID

# Send email
$GAPI mail send --to user@example.com --subject "Hello" --body "Message text"

# Send with attachment (max 3MB)
$GAPI mail send --to user@example.com --subject "Here's the file" --body "See attached" --attachment /path/to/file.png

# Reply to an email
$GAPI mail reply MESSAGE_ID --body "Thanks for the update!"

# Reply-all to an email
$GAPI mail replyall MESSAGE_ID --body "Sounds good, team."

# Forward an email
$GAPI mail forward MESSAGE_ID --to "forward@example.com" --body "FYI"

# List all mail folders
$GAPI mail folders

# Move an email to a different folder (get folder ID from 'mail folders')
$GAPI mail move MESSAGE_ID --folder FOLDER_ID

# --- CONTACTS ---

$GAPI contacts list --max 20

# --- USER PROFILE ---

$GAPI user profile
```

## Safe Email Sending

Use the `safe_mail_send.sh` script to preview before sending:

```bash
SAFE="~/.hermes/skills/productivity/microsoft-workspace/scripts/safe_mail_send.sh"

# Preview only (does not send)
$SAFE --to "user@example.com" --subject "Hello" --body-file /tmp/email_body.txt

# Preview + send
$SAFE --to "user@example.com" --subject "Hello" --body-file /tmp/email_body.txt --confirm

# With attachment
$SAFE --to "user@example.com" --subject "See attached" --body-file /tmp/email_body.txt --attachment /path/to/file.png --confirm
```

The script checks for `$` shell variable issues, large attachments, and missing files before sending.

## Configuration

Optional config at `~/.hermes/microsoft_config.json`:

```json
{
  "sender_name": "Your Name",
  "agent_name": "YourAgent"
}
```

When set, calendar invites include a branded sign-off. Without this config, invites use a clean template with no personal info.

Set via: `./scripts/auth.sh --config --name "Your Name" --agent "AgentName"`

## Output Format

All commands return JSON or structured text. Key fields:
- **Calendar list**: `[{id, subject, start, end, notes, meet, link}]`
- **Calendar create**: `{status, id, subject, start, end, link, meet, attendees}`
- **Calendar free/busy**: `[{email, status, availability}]`
- **Calendar find open**: `[{start, end, duration}]`
- **Mail list**: `[{id, from, subject, date, isRead, importance, preview}]`
- **Mail search**: `[{id, from, subject, date, preview}]`
- **Mail folders**: `[{id, name, total, unread}]`
- **Contacts list**: `[{displayName, emailAddresses, phones}]`
- **User profile**: `{displayName, email, jobTitle, office}`

## Sending Emails Safely (IMPORTANT)

**The `$` character is interpreted as a shell variable.** `$20` becomes empty (treated as `$2` + `0`). This causes mangled subjects and forces re-sends.

**NEVER do this:**
```bash
$GAPI mail send --to user@example.com --subject "Refund of $20" --body "I paid $50"
```

**ALWAYS do this:** Write the body to a temp file first:
```bash
cat > /tmp/email_body.txt << 'EOF'
Subject: Refund of $20

Hi, I was charged $20 and would like a refund.
EOF

# Preview
echo "To: user@example.com"
cat /tmp/email_body.txt

# Send
BODY=$(cat /tmp/email_body.txt)
$GAPI mail send --to "user@example.com" --subject "Refund of $20" --body "$BODY"
```

Or use `safe_mail_send.sh` which handles this automatically.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run `auth.sh --check` then re-authorize |
| `REFRESH_FAILED` | Token expired -- re-run `setup.py --auth-url` |
| `AADSTS700016` | Wrong client_id or tenant_id |
| `AADSTS65001` | User not consented -- check API permissions |
| `Insufficient privileges` | Need Calendars.ReadWrite permission |
| `$20` becomes `0` | Use `safe_mail_send.sh` or temp file pattern |
| Attachment too large | Max 3MB -- compress or split the file |
