from pathlib import Path
import os
import sys


def get_project_root() -> Path:
    override = os.environ.get("GYM_PLANNER_PROJECT_DIR")
    if override:
        return Path(override).expanduser().resolve()

    if getattr(sys, "frozen", False):
        exe_path = Path(sys.executable).resolve()
        # When the .app bundle sits next to the project source folder (e.g.
        # Training/GymPlanner.app alongside Training/GymPlanner/), resolve the
        # sibling directory with the same stem as the bundle.
        app_bundle = exe_path.parents[2]  # .../GymPlanner.app
        sibling = app_bundle.parent / app_bundle.stem  # .../GymPlanner
        if sibling.is_dir() and (sibling / "config" / "settings.toml").exists():
            return sibling
        # Legacy: app was built inside dist/ within the project root, so
        # parents[4] pointed directly at the project root.
        try:
            return exe_path.parents[4]
        except IndexError:
            return exe_path.parent

    return Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    override = os.environ.get("GYM_PLANNER_DATA_DIR")
    if override:
        data_dir = Path(override).expanduser().resolve()
    else:
        data_dir = get_project_root() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_token_path() -> Path:
    return get_data_dir() / "token.json"


def get_log_path() -> Path:
    return get_data_dir() / "log.json"


def get_credentials_path() -> Path:
    override = os.environ.get("GYM_PLANNER_CREDENTIALS")
    if override:
        return Path(override).expanduser().resolve()

    candidates = [
        get_data_dir() / "credentials.json",
        get_project_root() / "credentials.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    bundle_base = getattr(sys, "_MEIPASS", None)
    if bundle_base:
        bundled = Path(bundle_base) / "credentials.json"
        if bundled.exists():
            return bundled

    return candidates[0]
