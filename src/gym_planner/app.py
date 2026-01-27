from datetime import datetime
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY
from ttkbootstrap.widgets import DateEntry

from .planner import generate_week
from .google_calendar import upload_events_to_google


def run_plan(date_picker, date_entry, status_var, root):
    manual_value = date_entry.get().strip()
    try:
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
    root = ttk.Window(themename="flatly")
    root.title("Gym Planner")
    root.geometry("520x360")
    root.minsize(480, 320)

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

    status_var = tk.StringVar(value="Ready")
    status = ttk.Label(container, textvariable=status_var, font=("Avenir Next", 11))
    status.pack(anchor="w", pady=(0, 12))

    action = ttk.Button(
        container,
        text="Generate & Upload",
        bootstyle=PRIMARY,
        command=lambda: run_plan(date_picker, date_entry, status_var, root),
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
