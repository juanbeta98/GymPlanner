import argparse
from datetime import datetime

from .planner import generate_week
from .google_calendar import upload_events_to_google
from .config import SETTINGS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gym Planner Calendar uploader")
    parser.add_argument(
        "--start_date",
        type=str,
        required=True,
        help="Monday date of the week in YYYY-MM-DD format",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
    events = generate_week(start_date)
    upload_events_to_google(events, calendar_name=SETTINGS.calendar_name)
    print(f"✅ Weekly plan uploaded to {SETTINGS.calendar_name} calendar starting {args.start_date}")


if __name__ == "__main__":
    main()
