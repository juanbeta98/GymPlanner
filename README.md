# Gym Planner

A small automation app that generates a weekly training plan and uploads it to Google Calendar. Includes a GUI (desktop app) and CLI.

## Features
- Weekly plan generation with workout rotation logic
- Optional fixed training types (e.g., always Functional for Push)
- Google Calendar upload
- Desktop GUI for date selection and upload

## Project layout
```
config/            # user-editable config
  settings.toml
  legacy_config.py
src/gym_planner/   # application package
scripts/           # helper scripts
data/              # runtime data (token/log/credentials)
```

## Setup (micromamba)
```bash
micromamba create -n gymplannerEnv -f environment.yml
micromamba activate gymplannerEnv
```

## Configuration
Edit `config/settings.toml` for schedule, timezone, and fixed training types.

## Credentials
Place your OAuth client file here:
- `data/credentials.json`

The app writes:
- `data/token.json`
- `data/log.json`

These are ignored by git.

## Run (CLI)
```bash
gym-planner --start_date 2026-01-26
```

## Run (GUI)
```bash
gym-planner-gui
```

## Build macOS app
```bash
scripts/build_app.sh
```
Output will be in `dist/GymPlanner.app`.

## Environment variables
- `GYM_PLANNER_PROJECT_DIR`: override project root
- `GYM_PLANNER_DATA_DIR`: override data directory
- `GYM_PLANNER_CONFIG`: path to config file
- `GYM_PLANNER_CREDENTIALS`: path to OAuth credentials JSON
