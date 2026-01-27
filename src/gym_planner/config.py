from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os
import sys
import tomllib

from .paths import get_project_root


@dataclass(frozen=True)
class Settings:
    timezone: str
    calendar_name: str
    schedule: Dict[int, List[Tuple[str, str, str]]]
    fixed_training_types: Dict[str, Optional[str]]


def _load_settings_from_file(path: Path) -> Settings:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    timezone = data.get("timezone", "UTC")
    calendar_name = data.get("calendar_name", "Training")

    schedule_entries = data.get("schedule", [])
    schedule: Dict[int, List[Tuple[str, str, str]]] = {}
    for entry in schedule_entries:
        weekday = int(entry["weekday"])
        label = entry["label"]
        start = entry["start"]
        end = entry["end"]
        schedule.setdefault(weekday, []).append((label, start, end))

    fixed_raw = data.get("fixed_training_types", {}) or {}
    fixed_types: Dict[str, Optional[str]] = {}
    for key, value in fixed_raw.items():
        cleaned = str(value).strip() if value is not None else ""
        fixed_types[key] = cleaned if cleaned else None

    return Settings(
        timezone=timezone,
        calendar_name=calendar_name,
        schedule=schedule,
        fixed_training_types=fixed_types,
    )


def get_settings() -> Settings:
    override = os.environ.get("GYM_PLANNER_CONFIG")
    if override:
        return _load_settings_from_file(Path(override).expanduser().resolve())

    config_path = get_project_root() / "config" / "settings.toml"
    if config_path.exists():
        return _load_settings_from_file(config_path)

    bundle_base = getattr(sys, "_MEIPASS", None)
    if bundle_base:
        bundled = Path(bundle_base) / "config" / "settings.toml"
        if bundled.exists():
            return _load_settings_from_file(bundled)

    return _load_settings_from_file(config_path)


def get_writable_config_path() -> Path:
    override = os.environ.get("GYM_PLANNER_CONFIG")
    if override:
        return Path(override).expanduser().resolve()
    return get_project_root() / "config" / "settings.toml"


def _serialize_settings(data: dict) -> str:
    lines: list[str] = []
    lines.append(f"timezone = \"{data['timezone']}\"")
    lines.append(f"calendar_name = \"{data['calendar_name']}\"")
    lines.append("")
    lines.append("[fixed_training_types]")
    fixed = data.get("fixed_training_types", {}) or {}
    for key in sorted(fixed.keys()):
        value = fixed[key] or ""
        lines.append(f"{key} = \"{value}\"")
    lines.append("")
    for entry in data.get("schedule", []):
        lines.append("[[schedule]]")
        lines.append(f"weekday = {int(entry['weekday'])}")
        lines.append(f"label = \"{entry['label']}\"")
        lines.append(f"start = \"{entry['start']}\"")
        lines.append(f"end = \"{entry['end']}\"")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def update_fixed_training_types(new_fixed: Dict[str, Optional[str]]) -> None:
    config_path = get_writable_config_path()
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with config_path.open("rb") as f:
        data = tomllib.load(f)

    fixed = data.get("fixed_training_types", {}) or {}
    for key, value in new_fixed.items():
        fixed[key] = value or ""
    data["fixed_training_types"] = fixed

    config_path.write_text(_serialize_settings(data))
