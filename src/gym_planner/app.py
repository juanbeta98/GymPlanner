from datetime import datetime
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY
from ttkbootstrap.widgets import DateEntry

from .planner import generate_week
from .google_calendar import upload_events_to_google
from .config import get_settings, update_fixed_training_types
from .workouts import workouts

ALTERNATING_LABEL = "Alternating"


def _default_selection(_value: str | None) -> str:
    return ALTERNATING_LABEL


def _normalize_selection(value: str) -> str | None:
    return None if value == ALTERNATING_LABEL else value


def run_plan(date_picker, date_entry, status_var, root, push_var, pull_var, legs_var):
    manual_value = date_entry.get().strip()
    try:
        update_fixed_training_types(
            {
                "Push": _normalize_selection(push_var.get()),
                "Pull": _normalize_selection(pull_var.get()),
                "Legs": _normalize_selection(legs_var.get()),
            }
        )

        if manual_value:
            start_date = datetime.strptime(manual_value, "%Y-%m-%d").date()
        else:
            start_date = date_picker.get_date().date()

        status_var.set("Generating and uploading…")
        root.update_idletasks()

        events = generate_week(start_date)
        upload_events_to_google(events)

        status_var.set("Done. Calendar updated.")
        messagebox.showinfo("Success", "Weekly plan uploaded to Google Calendar.")
    except Exception as exc:
        status_var.set("Error. See details.")
        messagebox.showerror("Error", str(exc))


def build_ui():
    settings = get_settings()

    root = ttk.Window(themename="flatly")
    root.title("Gym Planner")
    root.geometry("520x620")
    root.minsize(480, 520)

    container = ttk.Frame(root, padding=24)
    container.pack(fill=tk.BOTH, expand=True)

    title = ttk.Label(container, text="Weekly Gym Planner", font=("Avenir Next", 20, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(
        container,
        text="Pick a Monday start date (or type one) and upload to Google Calendar.",
        font=("Avenir Next", 12),
        wraplength=440,
    )
    subtitle.pack(anchor="w", pady=(8, 24))

    date_frame = ttk.LabelFrame(container, text="Start Date")
    date_frame.pack(fill=tk.X, pady=(0, 16))

    date_inner = ttk.Frame(date_frame, padding=16)
    date_inner.pack(fill=tk.X)

    ttk.Label(date_inner, text="Calendar picker", font=("Avenir Next", 11)).grid(row=0, column=0, sticky="w")
    date_picker = DateEntry(date_inner, width=14, dateformat="%Y-%m-%d")
    date_picker.grid(row=1, column=0, sticky="w", pady=(6, 0))

    ttk.Label(date_inner, text="Or type (YYYY-MM-DD)", font=("Avenir Next", 11)).grid(
        row=0, column=1, sticky="w", padx=(24, 0)
    )
    date_entry = ttk.Entry(date_inner, width=18)
    date_entry.grid(row=1, column=1, sticky="w", padx=(24, 0), pady=(6, 0))

    types_frame = ttk.LabelFrame(container, text="Fixed Training Types")
    types_frame.pack(fill=tk.X, pady=(0, 16))

    types_inner = ttk.Frame(types_frame, padding=16)
    types_inner.pack(fill=tk.X)

    push_options = [ALTERNATING_LABEL] + list(workouts["Push"].keys())
    pull_options = [ALTERNATING_LABEL] + list(workouts["Pull"].keys())
    legs_options = [ALTERNATING_LABEL] + list(workouts["Legs"].keys())

    push_var = tk.StringVar(value=_default_selection(settings.fixed_training_types.get("Push")))
    pull_var = tk.StringVar(value=_default_selection(settings.fixed_training_types.get("Pull")))
    legs_var = tk.StringVar(value=_default_selection(settings.fixed_training_types.get("Legs")))

    ttk.Label(types_inner, text="Push", font=("Avenir Next", 11)).grid(row=0, column=0, sticky="w")
    push_combo = ttk.Combobox(types_inner, values=push_options, textvariable=push_var, state="readonly", width=24)
    push_combo.grid(row=1, column=0, sticky="w", pady=(6, 12))

    ttk.Label(types_inner, text="Pull", font=("Avenir Next", 11)).grid(row=2, column=0, sticky="w")
    pull_combo = ttk.Combobox(types_inner, values=pull_options, textvariable=pull_var, state="readonly", width=24)
    pull_combo.grid(row=3, column=0, sticky="w", pady=(6, 12))

    ttk.Label(types_inner, text="Legs", font=("Avenir Next", 11)).grid(row=4, column=0, sticky="w")
    legs_combo = ttk.Combobox(types_inner, values=legs_options, textvariable=legs_var, state="readonly", width=24)
    legs_combo.grid(row=5, column=0, sticky="w", pady=(6, 0))

    status_var = tk.StringVar(value="Ready")
    status = ttk.Label(container, textvariable=status_var, font=("Avenir Next", 11))
    status.pack(anchor="w", pady=(0, 12))

    action = ttk.Button(
        container,
        text="Generate & Upload",
        bootstyle=PRIMARY,
        command=lambda: run_plan(date_picker, date_entry, status_var, root, push_var, pull_var, legs_var),
    )
    action.pack(anchor="w")

    footer = ttk.Label(
        container,
        text="Tip: leave the text box empty to use the calendar picker.",
        font=("Avenir Next", 10),
    )
    footer.pack(anchor="w", pady=(16, 0))

    return root


def main():
    app = build_ui()
    app.mainloop()


if __name__ == "__main__":
    main()
