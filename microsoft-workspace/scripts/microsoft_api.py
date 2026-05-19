#!/usr/bin/env python3
"""Microsoft Graph API wrapper for Hermes -- Calendar, Mail, Contacts."""
import json
import sys
import os
from pathlib import Path
from urllib.parse import urlencode

HERMES_HOME = Path.home() / ".hermes"
TOKEN_PATH = HERMES_HOME / "microsoft_token.json"
CLIENT_SECRET_PATH = HERMES_HOME / "microsoft_client_secret.json"
CONFIG_PATH = HERMES_HOME / "microsoft_config.json"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _load_config() -> dict:
    """Load optional user config (sender name, agent name, etc.)."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def _get_token() -> str:
    """Get a valid access token, refreshing if needed."""
    if not TOKEN_PATH.exists():
        print("ERROR: Not authenticated. Run setup.py --auth-url first.")
        sys.exit(1)

    token = json.loads(TOKEN_PATH.read_text())

    import time
    if token.get("expires_at", 0) < time.time() + 300:
        token = _refresh_token(token)

    return token["access_token"]


def _refresh_token(token: dict) -> dict:
    """Refresh the access token using MSAL."""
    import msal

    config = json.loads(CLIENT_SECRET_PATH.read_text())
    app = msal.PublicClientApplication(
        config["client_id"],
        authority="https://login.microsoftonline.com/consumers",
    )

    result = app.acquire_token_by_refresh_token(
        token["refresh_token"],
        scopes=["Calendars.ReadWrite", "Mail.ReadWrite", "Mail.Send", "User.Read", "Contacts.Read"],
    )

    if "access_token" not in result:
        print(f"ERROR: Token refresh failed: {result.get('error_description', 'Unknown')}")
        sys.exit(1)

    TOKEN_PATH.write_text(json.dumps(result, indent=2))
    return result


def _api_call(method: str, endpoint: str, data: dict = None, params: dict = None):
    """Make an authenticated Graph API call."""
    import urllib.request

    token = _get_token()
    url = f"{GRAPH_BASE}{endpoint}"
    if params:
        url += "?" + urlencode(params)

    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    if data:
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (202, 204):
                return {"status": "success"}
            body = resp.read().decode()
            if not body:
                return {"status": "success"}
            return json.loads(body)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            print(f"ERROR {e.code}: {error_json.get('error', {}).get('message', error_body)}")
        except json.JSONDecodeError:
            print(f"ERROR {e.code}: {error_body}")
        sys.exit(1)


# === CALENDAR ===

def calendar_list(start: str = None, end: str = None, max_results: int = 25, upcoming: bool = True):
    """List calendar events. Defaults to upcoming (future) events only."""
    from datetime import datetime, timedelta

    params = {
        "$top": max_results,
        "$orderby": "start/dateTime",
        "$select": "id,subject,start,end,location,bodyPreview,webLink,isOnlineMeeting,onlineMeeting",
    }

    if not start and upcoming:
        start = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        end = (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S")

    if start:
        params["startDateTime"] = start
    if end:
        params["endDateTime"] = end
        result = _api_call("GET", "/me/calendarView", params=params)
    else:
        result = _api_call("GET", "/me/events", params=params)

    events = result.get("value", [])
    if not events:
        print("No events found.")
        return []

    output = []
    for e in events:
        start_time = e["start"].get("dateTime", "N/A")
        end_time = e["end"].get("dateTime", "N/A")
        meet_url = e.get("onlineMeeting", {}).get("joinUrl", "") if e.get("onlineMeeting") else ""
        entry = {
            "id": e["id"],
            "subject": e["subject"],
            "start": start_time,
            "end": end_time,
            "notes": e.get("bodyPreview", "")[:80],
            "meet": meet_url,
            "link": e.get("webLink", ""),
        }
        output.append(entry)
        print(f"  {e['subject']}")
        print(f"    When: {start_time} - {end_time}")
        print(f"    ID: {e['id']}")
        if e.get("bodyPreview"):
            print(f"    Notes: {e['bodyPreview'][:80]}")
        if meet_url:
            print(f"    Teams: {meet_url}")
        print()

    return output


def calendar_create(summary: str, start: str, end: str, description: str = "",
                     attendees: list = None, timezone: str = "America/Toronto",
                     add_teams: bool = True):
    """Create a calendar event."""
    event = {
        "subject": summary,
        "body": {"contentType": "HTML", "content": description},
        "start": {"dateTime": start, "timeZone": timezone},
        "end": {"dateTime": end, "timeZone": timezone},
        "isOnlineMeeting": add_teams,
    }

    if attendees:
        event["attendees"] = [
            {"emailAddress": {"address": email}, "type": "required"}
            for email in attendees
        ]

    result = _api_call("POST", "/me/events", data=event)

    meet_url = result.get("onlineMeeting", {}).get("joinUrl", "")
    output = {
        "status": "created",
        "id": result["id"],
        "subject": result["subject"],
        "start": result["start"]["dateTime"],
        "end": result["end"]["dateTime"],
        "link": result.get("webLink", ""),
        "meet": meet_url,
        "attendees": attendees or [],
    }
    print(json.dumps(output, indent=2))
    return output


def calendar_update(event_id: str, summary: str = None, start: str = None,
                    end: str = None, description: str = None, timezone: str = "America/Toronto"):
    """Update an existing calendar event (partial update)."""
    event = {}
    if summary:
        event["subject"] = summary
    if description is not None:
        event["body"] = {"contentType": "HTML", "content": description}
    if start:
        event["start"] = {"dateTime": start, "timeZone": timezone}
    if end:
        event["end"] = {"dateTime": end, "timeZone": timezone}

    if not event:
        print("ERROR: At least one field to update is required.")
        sys.exit(1)

    result = _api_call("PATCH", f"/me/events/{event_id}", data=event)
    print(f"Updated: {result.get('subject', 'N/A')}")
    print(f"  ID: {result['id']}")
    if start:
        print(f"  Start: {result['start']['dateTime']}")
    if end:
        print(f"  End: {result['end']['dateTime']}")
    return {"status": "updated", "id": result["id"], "subject": result.get("subject", "")}


def calendar_delete(event_id: str):
    """Delete a calendar event."""
    _api_call("DELETE", f"/me/events/{event_id}")
    print(f"Deleted event: {event_id}")


def calendar_freebusy(emails: list, start: str, end: str, timezone: str = "America/Toronto",
                      interval_minutes: int = 30):
    """Check free/busy status for one or more people."""
    data = {
        "schedules": emails,
        "startTime": {"dateTime": start, "timeZone": timezone},
        "endTime": {"dateTime": end, "timeZone": timezone},
        "availabilityViewInterval": interval_minutes,
    }
    result = _api_call("POST", "/me/calendar/getSchedule", data=data)
    schedules = result.get("value", [])
    if not schedules:
        print("No schedule data returned.")
        return []

    output = []
    for s in schedules:
        email = s.get("scheduleId", "Unknown")
        status_str = s.get("availabilityView", "")
        free_blocks = []
        for i, char in enumerate(status_str):
            offset_min = i * interval_minutes
            if char == "0":  # 0 = free
                block_start = start  # approximate
                free_blocks.append(f"  Slot {i}: free")

        entry = {
            "email": email,
            "status": s.get("status", ""),
            "availability": status_str,
        }
        output.append(entry)
        print(f"  {email}")
        print(f"    Status: {s.get('status', 'N/A')}")
        # Decode availability: 0=free, 1=tentative, 2=busy, 3=OOF
        labels = {"0": "Free", "1": "Tentative", "2": "Busy", "3": "OOF"}
        if status_str:
            print(f"    Schedule ({interval_minutes}min blocks):")
            for i, char in enumerate(status_str):
                label = labels.get(char, char)
                print(f"      Block {i}: {label}")
        print()
    return output


def calendar_find_open(emails: list, start: str, end: str, duration_minutes: int = 30,
                       timezone: str = "America/Toronto", interval_minutes: int = 15):
    """Find available time slots where all attendees are free."""
    data = {
        "schedules": emails,
        "startTime": {"dateTime": start, "timeZone": timezone},
        "endTime": {"dateTime": end, "timeZone": timezone},
        "availabilityViewInterval": interval_minutes,
    }
    result = _api_call("POST", "/me/calendar/getSchedule", data=data)
    schedules = result.get("value", [])

    if not schedules:
        print("No schedule data returned.")
        return []

    # Find slots where ALL are free
    all_views = [s.get("availabilityView", "") for s in schedules if s.get("availabilityView")]
    if not all_views:
        print("No availability data.")
        return []

    min_len = min(len(v) for v in all_views)
    blocks_needed = duration_minutes // interval_minutes
    if duration_minutes % interval_minutes:
        blocks_needed += 1

    open_slots = []
    from datetime import datetime, timedelta
    try:
        dt_start = datetime.fromisoformat(start)
    except Exception:
        dt_start = datetime.utcnow()

    for i in range(min_len - blocks_needed + 1):
        if all(v[i + j] == "0" for v in all_views for j in range(blocks_needed)):
            slot_start = dt_start + timedelta(minutes=i * interval_minutes)
            slot_end = slot_start + timedelta(minutes=duration_minutes)
            slot = {
                "start": slot_start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": slot_end.strftime("%Y-%m-%dT%H:%M:%S"),
                "duration": duration_minutes,
            }
            open_slots.append(slot)
            print(f"  Open: {slot['start']} - {slot['end']} ({duration_minutes} min)")

    if not open_slots:
        print("No open slots found in this time range.")
    return open_slots


def calendar_invite(summary: str, start: str, end: str, description: str = "",
                    attendees: list = None, timezone: str = "America/Toronto",
                    meet: bool = False):
    """Create a calendar event with attendees and optional video link."""
    from datetime import datetime

    config = _load_config()
    sender_name = config.get("sender_name", "")
    agent_name = config.get("agent_name", "")

    try:
        dt_start = datetime.fromisoformat(start)
        dt_end = datetime.fromisoformat(end)
        duration = int((dt_end - dt_start).total_seconds() / 60)
        date_str = dt_start.strftime("%A, %B %d, %Y")
        time_str = (dt_start.strftime("%I:%M %p").lstrip("0") + " - " +
                    dt_end.strftime("%I:%M %p").lstrip("0") + " (" +
                    timezone.replace("_", " ").split("/")[-1] + ")")
        duration_str = f"{duration} min"
    except Exception:
        date_str = start
        time_str = f"{start} - {end}"
        duration_str = "30 min"

    desc_html = description.replace("\n", "<br>") if description else ""

    # Build sign-off section
    sign_off = ""
    if sender_name:
        sign_off = f'''
        Best regards,<br>
        <span style="font-weight: 500; color: #333;">{sender_name}</span>'''

    agent_footer = ""
    if agent_name and sender_name:
        agent_footer = f'''
      <div style="font-size: 10px; color: #999; letter-spacing: 1.5px; text-transform: uppercase;">Scheduled by</div>
      <div style="font-size: 13px; color: #444; margin-top: 2px;">
        <span style="font-weight: 600;">{agent_name}</span>
        <span style="color: #999;"> &mdash; </span>
        <span style="font-style: italic; color: #666;">{sender_name}&apos;s AI Assistant</span>
      </div>
      <div style="font-size: 10px; color: #aaa; margin-top: 2px;">Powered by Hermes Agent</div>'''

    body_html = f'''<table width="100%" cellpadding="0" cellspacing="0" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto;">
  <tr>
    <td style="padding: 24px; background: #ffffff;">
      <div style="font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Topic</div>
      <div style="font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 16px;">{summary}</div>
      <div style="font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">Description</div>
      <div style="font-size: 15px; line-height: 1.6; color: #333; margin-bottom: 20px;">
        {desc_html}
      </div>
      <table cellpadding="0" cellspacing="0" style="background: #f5f5f5; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
        <tr>
          <td style="padding: 16px;">
            <table cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td style="padding-bottom: 8px;">
                  <span style="font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1px;">Date</span><br>
                  <span style="font-size: 14px; color: #333; font-weight: 500;">{date_str}</span>
                </td>
              </tr>
              <tr>
                <td style="padding-bottom: 8px;">
                  <span style="font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1px;">Time</span><br>
                  <span style="font-size: 14px; color: #333; font-weight: 500;">{time_str}</span>
                </td>
              </tr>
              <tr>
                <td>
                  <span style="font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1px;">Duration</span><br>
                  <span style="font-size: 14px; color: #333; font-weight: 500;">{duration_str}</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding: 0 24px;">
      <hr style="border: none; border-top: 1px solid #e5e5e5; margin: 0;">
    </td>
  </tr>{sign_off}
  <tr>
    <td style="padding: 8px 24px 4px 24px; background: #fafafa;">{agent_footer}
    </td>
  </tr>
</table>'''

    event = {
        "subject": summary,
        "body": {"contentType": "HTML", "content": body_html},
        "start": {"dateTime": start, "timeZone": timezone},
        "end": {"dateTime": end, "timeZone": timezone},
        "isOnlineMeeting": meet,
    }

    if attendees:
        event["attendees"] = [
            {"emailAddress": {"address": email}, "type": "required"}
            for email in attendees
        ]

    result = _api_call("POST", "/me/events", data=event)
    meet_url = result.get("onlineMeeting", {}).get("joinUrl", "")

    print(f"Created: {result['subject']}")
    print(f"  When: {result['start']['dateTime']} - {result['end']['dateTime']}")
    print(f"  ID: {result['id']}")
    if meet_url:
        print(f"  Meet: {meet_url}")
    if attendees:
        print(f"  Attendees: {', '.join(attendees)}")
    return result


# === MAIL ===

def mail_list(max_results: int = 10, folder: str = "inbox",
              unread: bool = False, important: bool = False):
    """List emails with optional filters."""
    params = {
        "$top": max_results,
        "$orderby": "receivedDateTime desc",
        "$select": "id,from,subject,receivedDateTime,bodyPreview,isRead,importance",
    }
    filters = []
    if unread:
        filters.append("isRead eq false")
    if important:
        filters.append("importance eq 'high'")
    if filters:
        params["$filter"] = " and ".join(filters)

    result = _api_call("GET", f"/me/mailFolders/{folder}/messages", params=params)
    messages = result.get("value", [])
    if not messages:
        print("No messages found.")
        return []
    output = []
    for m in messages:
        sender = m.get("from", {}).get("emailAddress", {}).get("address", "Unknown")
        read = " " if m.get("isRead") else ">"
        imp = "!" if m.get("importance") == "high" else " "
        entry = {
            "id": m["id"],
            "from": sender,
            "subject": m["subject"],
            "date": m["receivedDateTime"],
            "isRead": m.get("isRead", False),
            "importance": m.get("importance", "normal"),
            "preview": m.get("bodyPreview", "")[:80],
        }
        output.append(entry)
        print(f"  {read}{imp} {m['subject']}")
        print(f"    From: {sender}")
        print(f"    Date: {m['receivedDateTime']}")
        print(f"    ID: {m['id']}")
        print()
    return output


def mail_search(query: str, max_results: int = 10, folder: str = "inbox"):
    """Search emails by keyword."""
    params = {
        "$search": f'"{query}"',
        "$top": max_results,
        "$select": "id,from,subject,receivedDateTime,bodyPreview,isRead",
    }
    # $search goes on the endpoint path, not as a query param for mail
    endpoint = f"/me/mailFolders/{folder}/messages"
    url_full = f"{GRAPH_BASE}{endpoint}?{urlencode(params)}"
    result = _api_call("GET", f"{endpoint}", params=params)
    messages = result.get("value", [])
    if not messages:
        print(f"No results for '{query}'.")
        return []
    output = []
    for m in messages:
        sender = m.get("from", {}).get("emailAddress", {}).get("address", "Unknown")
        entry = {
            "id": m["id"],
            "from": sender,
            "subject": m["subject"],
            "date": m["receivedDateTime"],
            "preview": m.get("bodyPreview", "")[:80],
        }
        output.append(entry)
        print(f"  {m['subject']}")
        print(f"    From: {sender}")
        print(f"    Date: {m['receivedDateTime']}")
        print(f"    ID: {m['id']}")
        print()
    return output


def mail_get(message_id: str):
    """Get full email content."""
    result = _api_call("GET", f"/me/messages/{message_id}")
    print(f"Subject: {result['subject']}")
    print(f"From: {result.get('from', {}).get('emailAddress', {}).get('address', 'N/A')}")
    print(f"Date: {result['receivedDateTime']}")
    print(f"Body:\n{result.get('body', {}).get('content', 'N/A')}")


def mail_reply(message_id: str, body: str, html: bool = False):
    """Reply to an email."""
    content_type = "HTML" if html else "Text"
    data = {"comment": body}
    result = _api_call("POST", f"/me/messages/{message_id}/reply", data=data)
    print(f"Replied to message: {message_id}")
    return {"status": "replied", "id": message_id}


def mail_reply_all(message_id: str, body: str, html: bool = False):
    """Reply-all to an email."""
    data = {"comment": body}
    result = _api_call("POST", f"/me/messages/{message_id}/replyAll", data=data)
    print(f"Replied-all to message: {message_id}")
    return {"status": "replied-all", "id": message_id}


def mail_forward(message_id: str, to: str, body: str = "", html: bool = False):
    """Forward an email."""
    data = {
        "comment": body,
        "toRecipients": [{"emailAddress": {"address": to}}],
    }
    result = _api_call("POST", f"/me/messages/{message_id}/forward", data=data)
    print(f"Forwarded message {message_id} to {to}")
    return {"status": "forwarded", "id": message_id, "to": to}


def mail_folders():
    """List all mail folders."""
    params = {
        "$select": "id,displayName,totalItemCount,unreadItemCount",
        "$orderby": "displayName",
    }
    result = _api_call("GET", "/me/mailFolders", params=params)
    folders = result.get("value", [])
    if not folders:
        print("No folders found.")
        return []
    output = []
    for f in folders:
        entry = {
            "id": f["id"],
            "name": f["displayName"],
            "total": f.get("totalItemCount", 0),
            "unread": f.get("unreadItemCount", 0),
        }
        output.append(entry)
        unread_str = f" ({f.get('unreadItemCount', 0)} unread)" if f.get("unreadItemCount", 0) else ""
        print(f"  {f['displayName']}{unread_str}")
        print(f"    ID: {f['id']}")
        print()
    return output


def mail_move(message_id: str, folder_id: str):
    """Move an email to a different folder."""
    data = {"destinationId": folder_id}
    result = _api_call("POST", f"/me/messages/{message_id}/move", data=data)
    print(f"Moved message to: {result.get('parentFolderId', folder_id)}")
    return {"status": "moved", "id": message_id, "destination": folder_id}


def mail_send(to: str, subject: str, body: str, html: bool = False, attachment: str = None):
    """Send an email, optionally with a file attachment."""
    import base64
    import mimetypes

    content_type = "HTML" if html else "Text"

    if attachment:
        draft_data = {
            "subject": subject,
            "body": {"contentType": content_type, "content": body},
            "toRecipients": [{"emailAddress": {"address": to}}],
        }
        draft = _api_call("POST", "/me/messages", data=draft_data)
        message_id = draft["id"]

        file_path = os.path.expanduser(attachment)
        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            sys.exit(1)

        file_size = os.path.getsize(file_path)
        if file_size > 3 * 1024 * 1024:
            print(f"ERROR: Attachment too large ({file_size / 1024 / 1024:.1f} MB). Max 3MB for inline attachments.")
            print("Tip: Compress the image or use a smaller file.")
            sys.exit(1)

        with open(file_path, "rb") as f:
            file_content = base64.b64encode(f.read()).decode("utf-8")

        file_name = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        attach_data = {
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": file_name,
            "contentType": mime_type,
            "contentBytes": file_content,
        }
        _api_call("POST", f"/me/messages/{message_id}/attachments", data=attach_data)
        _api_call("POST", f"/me/messages/{message_id}/send", data={})
        print(f"Sent to {to}: {subject} (with attachment: {file_name})")
    else:
        data = {
            "message": {
                "subject": subject,
                "body": {"contentType": content_type, "content": body},
                "toRecipients": [{"emailAddress": {"address": to}}],
            }
        }
        _api_call("POST", "/me/sendMail", data=data)
        print(f"Sent to {to}: {subject}")


# === CONTACTS ===

def contacts_list(max_results: int = 20):
    """List contacts."""
    params = {"$top": max_results, "$select": "displayName,emailAddresses,mobilePhone"}
    result = _api_call("GET", "/me/contacts", params=params)
    contacts = result.get("value", [])
    if not contacts:
        print("No contacts found.")
        return
    for c in contacts:
        emails = ", ".join(e.get("address", "") for e in c.get("emailAddresses", []))
        phone = c.get("mobilePhone", "")
        print(f"  {c['displayName']}")
        if emails:
            print(f"    Email: {emails}")
        if phone:
            print(f"    Phone: {phone}")
        print()


# === USER PROFILE ===

def user_profile():
    """Get current user's profile info."""
    params = {"$select": "displayName,mail,userPrincipalName,jobTitle,officeLocation"}
    result = _api_call("GET", "/me", params=params)
    profile = {
        "displayName": result.get("displayName", ""),
        "email": result.get("mail") or result.get("userPrincipalName", ""),
        "jobTitle": result.get("jobTitle", ""),
        "office": result.get("officeLocation", ""),
    }
    print(f"  Name: {profile['displayName']}")
    print(f"  Email: {profile['email']}")
    if profile["jobTitle"]:
        print(f"  Title: {profile['jobTitle']}")
    if profile["office"]:
        print(f"  Office: {profile['office']}")
    return profile


# === CLI ===

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: microsoft_api.py <resource> <action> [args]")
        print("Resources: calendar, mail, contacts, user")
        print("Actions:")
        print("  calendar list [--start DATETIME] [--end DATETIME] [--max N] [--all]")
        print("  calendar create --summary TITLE --start DATETIME --end DATETIME [--description TEXT] [--attendees EMAIL1,EMAIL2]")
        print("  calendar invite --summary TITLE --start DATETIME --end DATETIME [--description TEXT] [--attendees EMAIL1,EMAIL2] [--meet]")
        print("  calendar update EVENT_ID [--summary TITLE] [--start DATETIME] [--end DATETIME] [--description TEXT]")
        print("  calendar delete EVENT_ID")
        print("  calendar freebusy --emails EMAIL1,EMAIL2 --start DATETIME --end DATETIME [--interval 30]")
        print("  calendar findopen --emails EMAIL1,EMAIL2 --start DATETIME --end DATETIME [--duration 30] [--interval 15]")
        print("  mail list [--max N] [--folder NAME] [--unread] [--important]")
        print("  mail search --query KEYWORD [--max N] [--folder NAME]")
        print("  mail get MESSAGE_ID")
        print("  mail send --to EMAIL --subject TEXT --body TEXT [--html] [--attachment FILEPATH]")
        print("  mail reply MESSAGE_ID --body TEXT")
        print("  mail replyall MESSAGE_ID --body TEXT")
        print("  mail forward MESSAGE_ID --to EMAIL [--body TEXT]")
        print("  mail folders")
        print("  mail move MESSAGE_ID --folder FOLDER_ID")
        print("  contacts list [--max N]")
        print("  user profile")
        sys.exit(1)

    resource = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "list"

    if resource == "calendar":
        if action == "list":
            start = None
            end = None
            max_r = 25
            upcoming = True
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--start" and i + 1 < len(sys.argv):
                    start = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
                    end = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--max" and i + 1 < len(sys.argv):
                    max_r = int(sys.argv[i + 1]); i += 2
                elif sys.argv[i] == "--all":
                    upcoming = False; i += 1
                else:
                    i += 1
            calendar_list(start, end, max_r, upcoming)

        elif action == "create":
            summary = desc = start = end = ""
            attendees = None
            tz = "America/Toronto"
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--summary" and i + 1 < len(sys.argv):
                    summary = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--description" and i + 1 < len(sys.argv):
                    desc = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--start" and i + 1 < len(sys.argv):
                    start = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
                    end = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--attendees" and i + 1 < len(sys.argv):
                    attendees = sys.argv[i + 1].split(","); i += 2
                else:
                    i += 1
            if not all([summary, start, end]):
                print("ERROR: --summary, --start, and --end are required")
                sys.exit(1)
            calendar_create(summary, start, end, desc, attendees, tz)

        elif action == "update":
            if len(sys.argv) < 4:
                print("Usage: calendar update EVENT_ID [--summary TITLE] [--start DATETIME] [--end DATETIME] [--description TEXT]")
                sys.exit(1)
            event_id = sys.argv[3]
            summary = start = end = None
            desc = None
            tz = "America/Toronto"
            i = 4
            while i < len(sys.argv):
                if sys.argv[i] == "--summary" and i + 1 < len(sys.argv):
                    summary = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--description" and i + 1 < len(sys.argv):
                    desc = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--start" and i + 1 < len(sys.argv):
                    start = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
                    end = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            calendar_update(event_id, summary, start, end, desc, tz)

        elif action == "delete":
            if len(sys.argv) < 4:
                print("Usage: calendar delete EVENT_ID")
                sys.exit(1)
            calendar_delete(sys.argv[3])

        elif action == "invite":
            summary = desc = start = end = ""
            attendees = None
            tz = "America/Toronto"
            use_meet = False
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--summary" and i + 1 < len(sys.argv):
                    summary = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--description" and i + 1 < len(sys.argv):
                    desc = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--start" and i + 1 < len(sys.argv):
                    start = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
                    end = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--attendees" and i + 1 < len(sys.argv):
                    attendees = sys.argv[i + 1].split(","); i += 2
                elif sys.argv[i] == "--meet":
                    use_meet = True; i += 1
                else:
                    i += 1
            if not all([summary, start, end]):
                print("ERROR: --summary, --start, and --end are required")
                sys.exit(1)
            calendar_invite(summary, start, end, desc, attendees, tz, use_meet)

        elif action == "freebusy":
            emails = start = end = None
            tz = "America/Toronto"
            interval = 30
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--emails" and i + 1 < len(sys.argv):
                    emails = sys.argv[i + 1].split(","); i += 2
                elif sys.argv[i] == "--start" and i + 1 < len(sys.argv):
                    start = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
                    end = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--interval" and i + 1 < len(sys.argv):
                    interval = int(sys.argv[i + 1]); i += 2
                else:
                    i += 1
            if not all([emails, start, end]):
                print("ERROR: --emails, --start, and --end are required")
                sys.exit(1)
            calendar_freebusy(emails, start, end, tz, interval)

        elif action == "findopen":
            emails = start = end = None
            tz = "America/Toronto"
            duration = 30
            interval = 15
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--emails" and i + 1 < len(sys.argv):
                    emails = sys.argv[i + 1].split(","); i += 2
                elif sys.argv[i] == "--start" and i + 1 < len(sys.argv):
                    start = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
                    end = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--duration" and i + 1 < len(sys.argv):
                    duration = int(sys.argv[i + 1]); i += 2
                elif sys.argv[i] == "--interval" and i + 1 < len(sys.argv):
                    interval = int(sys.argv[i + 1]); i += 2
                else:
                    i += 1
            if not all([emails, start, end]):
                print("ERROR: --emails, --start, and --end are required")
                sys.exit(1)
            calendar_find_open(emails, start, end, duration, tz, interval)

    elif resource == "mail":
        if action == "list":
            max_r = 10
            folder = "inbox"
            unread = False
            important = False
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--max" and i + 1 < len(sys.argv):
                    max_r = int(sys.argv[i + 1]); i += 2
                elif sys.argv[i] == "--folder" and i + 1 < len(sys.argv):
                    folder = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--unread":
                    unread = True; i += 1
                elif sys.argv[i] == "--important":
                    important = True; i += 1
                else:
                    i += 1
            mail_list(max_r, folder, unread, important)

        elif action == "search":
            query = None
            max_r = 10
            folder = "inbox"
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--query" and i + 1 < len(sys.argv):
                    query = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--max" and i + 1 < len(sys.argv):
                    max_r = int(sys.argv[i + 1]); i += 2
                elif sys.argv[i] == "--folder" and i + 1 < len(sys.argv):
                    folder = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not query:
                print("ERROR: --query is required")
                sys.exit(1)
            mail_search(query, max_r, folder)

        elif action == "get":
            if len(sys.argv) < 4:
                print("Usage: mail get MESSAGE_ID")
                sys.exit(1)
            mail_get(sys.argv[3])

        elif action == "send":
            to = subject = body = ""
            html = False
            attachment = None
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--to" and i + 1 < len(sys.argv):
                    to = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--subject" and i + 1 < len(sys.argv):
                    subject = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--body" and i + 1 < len(sys.argv):
                    body = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--html":
                    html = True; i += 1
                elif sys.argv[i] == "--attachment" and i + 1 < len(sys.argv):
                    attachment = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not all([to, subject, body]):
                print("ERROR: --to, --subject, and --body are required")
                sys.exit(1)
            mail_send(to, subject, body, html, attachment)

        elif action == "reply":
            if len(sys.argv) < 5:
                print("Usage: mail reply MESSAGE_ID --body TEXT")
                sys.exit(1)
            msg_id = sys.argv[3]
            body = ""
            i = 4
            while i < len(sys.argv):
                if sys.argv[i] == "--body" and i + 1 < len(sys.argv):
                    body = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not body:
                print("ERROR: --body is required")
                sys.exit(1)
            mail_reply(msg_id, body)

        elif action == "replyall":
            if len(sys.argv) < 5:
                print("Usage: mail replyall MESSAGE_ID --body TEXT")
                sys.exit(1)
            msg_id = sys.argv[3]
            body = ""
            i = 4
            while i < len(sys.argv):
                if sys.argv[i] == "--body" and i + 1 < len(sys.argv):
                    body = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not body:
                print("ERROR: --body is required")
                sys.exit(1)
            mail_reply_all(msg_id, body)

        elif action == "forward":
            if len(sys.argv) < 5:
                print("Usage: mail forward MESSAGE_ID --to EMAIL [--body TEXT]")
                sys.exit(1)
            msg_id = sys.argv[3]
            to = body = ""
            i = 4
            while i < len(sys.argv):
                if sys.argv[i] == "--to" and i + 1 < len(sys.argv):
                    to = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--body" and i + 1 < len(sys.argv):
                    body = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not to:
                print("ERROR: --to is required")
                sys.exit(1)
            mail_forward(msg_id, to, body)

        elif action == "folders":
            mail_folders()

        elif action == "move":
            if len(sys.argv) < 5:
                print("Usage: mail move MESSAGE_ID --folder FOLDER_ID")
                sys.exit(1)
            msg_id = sys.argv[3]
            folder_id = None
            i = 4
            while i < len(sys.argv):
                if sys.argv[i] == "--folder" and i + 1 < len(sys.argv):
                    folder_id = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not folder_id:
                print("ERROR: --folder is required")
                sys.exit(1)
            mail_move(msg_id, folder_id)

    elif resource == "contacts":
        max_r = 20
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--max" and i + 1 < len(sys.argv):
                max_r = int(sys.argv[i + 1]); i += 2
            else:
                i += 1
        contacts_list(max_r)

    elif resource == "user":
        user_profile()

    else:
        print(f"Unknown resource: {resource}")
        sys.exit(1)
