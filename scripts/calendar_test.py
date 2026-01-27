from datetime import datetime, timedelta

from gym_planner.config import get_settings
from gym_planner.google_calendar import get_service, get_training_calendar_id


def main():
    settings = get_settings()
    service = get_service()

    calendar_id = get_training_calendar_id(service, settings.calendar_name)

    now = datetime.now()
    event = {
        "summary": "🔥 TEST – Gym Planner",
        "start": {
            "dateTime": now.isoformat(),
            "timeZone": settings.timezone,
        },
        "end": {
            "dateTime": (now + timedelta(minutes=30)).isoformat(),
            "timeZone": settings.timezone,
        },
        # No colorId: will inherit calendar default
    }

    created_event = service.events().insert(
        calendarId=calendar_id,
        body=event
    ).execute()

    print("✅ Event created in Training calendar:")
    print(created_event["htmlLink"])


if __name__ == "__main__":
    main()
