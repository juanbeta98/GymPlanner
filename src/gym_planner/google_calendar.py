from datetime import datetime
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import SETTINGS
from .paths import get_credentials_path, get_token_path

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_MAX_AGE_SECONDS = 2 * 60 * 60


def get_service():
    creds = None
    token_path = get_token_path()

    if token_path.exists():
        token_age = time.time() - token_path.stat().st_mtime
        if token_age > TOKEN_MAX_AGE_SECONDS:
            token_path.unlink()

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = get_credentials_path()
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"OAuth credentials not found at {credentials_path}. "
                    "Place credentials.json in data/ or set GYM_PLANNER_CREDENTIALS."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def get_training_calendar_id(service, calendar_name: str):
    calendars = service.calendarList().list().execute()
    for cal in calendars["items"]:
        if cal["summary"] == calendar_name:
            return cal["id"]
    raise ValueError(f"Calendar '{calendar_name}' not found")


def upload_events_to_google(events, calendar_name: str | None = None):
    service = get_service()
    calendar_id = get_training_calendar_id(service, calendar_name or SETTINGS.calendar_name)

    for date, title, start, end in events:
        start_dt = datetime.combine(date, datetime.strptime(start, "%H:%M").time())
        end_dt = datetime.combine(date, datetime.strptime(end, "%H:%M").time())

        event_body = {
            "summary": title,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": SETTINGS.timezone},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": SETTINGS.timezone},
        }

        service.events().insert(calendarId=calendar_id, body=event_body).execute()
