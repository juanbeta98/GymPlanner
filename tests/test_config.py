from gym_planner.config import get_settings


def test_settings_loads():
    settings = get_settings()
    assert settings.calendar_name
    assert settings.timezone
    assert settings.schedule
