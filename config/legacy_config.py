# Deprecated: use config/settings.toml
TIMEZONE = "Europe/Amsterdam"  # change if needed
CALENDAR_NAME = "Training"     # your calendar

# Weekly schedule: weekday -> list of (label, start_time, end_time)
SCHEDULE = {
    0: [("Push", "06:00", "07:30")],  # Monday
    1: [("Run – Quality", "06:30", "07:15"),
        ("Mobility Routine", "18:30", "19:15")],  # Tuesday
    2: [("Pull", "06:00", "07:30")],  # Wednesday
    3: [("Legs", "06:00", "07:30")],  # Thursday
    4: [("Calisthenics", "06:00", "07:30")],  # Friday
    5: [("Run – Aerobic", "08:00", "08:45"),
        ("Swimming/Mobility", "11:00", "11:45")],  # Saturday
    6: [("HYROX Madness", "08:00", "10:00")],  # Sunday
}

# Optional: force a fixed training type per category.
# Use None or "" to keep existing rotation logic.
FIXED_TRAINING_TYPES = {
    "Push": 'Functional',  # e.g. "Functional"
    "Pull": 'Functional',  # e.g. "Strength"
    "Legs": None,  # e.g. "Therapy/Mobility"
}
