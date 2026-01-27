#!/usr/bin/env bash
set -euo pipefail

APP_NAME="GymPlanner"
ADD_DATA=()

if [[ -f config/settings.toml ]]; then
  ADD_DATA+=(--add-data "config/settings.toml:config")
fi

if [[ -f data/credentials.json ]]; then
  ADD_DATA+=(--add-data "data/credentials.json:data")
fi

micromamba run -n gymplannerEnv pyinstaller \
  --noconfirm \
  --windowed \
  --name "$APP_NAME" \
  --paths src \
  "${ADD_DATA[@]}" \
  app_entry.py
