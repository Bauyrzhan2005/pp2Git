"""JSON helpers for settings and leaderboard."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "sound": True,
    "car_color": "Blue",
    "difficulty": "Normal",
}


def load_json(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        save_json(path, default)
        return default
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        save_json(path, default)
        return default


def save_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_settings() -> Dict[str, Any]:
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())
    fixed = DEFAULT_SETTINGS.copy()
    fixed.update(settings)
    return fixed


def save_settings(settings: Dict[str, Any]) -> None:
    save_json(SETTINGS_FILE, settings)


def load_leaderboard() -> List[Dict[str, Any]]:
    data = load_json(LEADERBOARD_FILE, [])
    if not isinstance(data, list):
        return []
    return data


def add_score(name: str, score: int, distance: int, coins: int) -> None:
    leaderboard = load_leaderboard()
    leaderboard.append({
        "name": name[:12] or "Player",
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins),
    })
    leaderboard.sort(key=lambda item: item.get("score", 0), reverse=True)
    save_json(LEADERBOARD_FILE, leaderboard[:10])
