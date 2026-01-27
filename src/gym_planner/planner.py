import json
import random
from datetime import date, timedelta
from typing import List, Tuple

from .config import SETTINGS
from .paths import get_log_path
from .workouts import workouts


LogType = dict
EventType = Tuple[date, str, str, str]


def load_log() -> LogType:
    log_path = get_log_path()
    if log_path.exists():
        with log_path.open("r") as f:
            return json.load(f)
    return {
        "last_used": {},
        "legs_rotation_index": 0,
        "last_calisthenics": None,
        "week_toggle": 0,
    }


def save_log(log: LogType) -> None:
    log_path = get_log_path()
    with log_path.open("w") as f:
        json.dump(log, f, indent=2)


def choose_with_no_repeat(options, last_used):
    choices = [o for o in options if o != last_used]
    return random.choice(choices if choices else options)


def select_push_pull(day: str, log: LogType) -> str:
    fixed_type = (SETTINGS.fixed_training_types.get(day) or "").strip()
    if fixed_type:
        training_type = fixed_type
    else:
        is_even_week = log["week_toggle"] % 2 == 0
        if day == "Push":
            training_type = "Functional" if is_even_week else "Strength"
        else:
            training_type = "Strength" if is_even_week else "Functional"

    if training_type not in workouts[day]:
        raise ValueError(f"Invalid training type '{training_type}' for {day}")

    key = f"{day}_{training_type}"
    last = log["last_used"].get(key)
    letter = choose_with_no_repeat(workouts[day][training_type], last)
    log["last_used"][key] = letter
    return f"{day} – {training_type} ({letter})"


def select_legs(log: LogType) -> str:
    fixed_type = (SETTINGS.fixed_training_types.get("Legs") or "").strip()
    if fixed_type:
        training_type = fixed_type
    else:
        types = list(workouts["Legs"].keys())
        idx = log["legs_rotation_index"] % len(types)
        training_type = types[idx]

    if training_type not in workouts["Legs"]:
        raise ValueError(f"Invalid training type '{training_type}' for Legs")

    key = f"Legs_{training_type}"
    last = log["last_used"].get(key)
    letter = choose_with_no_repeat(workouts["Legs"][training_type], last)
    log["last_used"][key] = letter

    if not fixed_type:
        log["legs_rotation_index"] += 1

    return f"Legs – {training_type} ({letter})"


def select_calisthenics(log: LogType) -> str:
    last = log.get("last_calisthenics")
    letter = "B" if last == "A" else "A"
    log["last_calisthenics"] = letter
    return f"Calisthenics/Core ({letter})"


def generate_week(start_date: date) -> List[EventType]:
    log = load_log()
    events: List[EventType] = []

    for weekday in sorted(SETTINGS.schedule):
        day_events = SETTINGS.schedule[weekday]
        event_date = start_date + timedelta(days=weekday)
        for label, start, end in day_events:
            if label == "Push":
                title = select_push_pull("Push", log)
            elif label == "Pull":
                title = select_push_pull("Pull", log)
            elif label == "Legs":
                title = select_legs(log)
            elif label == "Calisthenics":
                title = select_calisthenics(log)
            else:
                title = label

            events.append((event_date, title, start, end))

    log["week_toggle"] += 1
    save_log(log)
    return events
