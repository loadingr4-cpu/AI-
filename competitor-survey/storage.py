import json
import os
from datetime import datetime, date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def _month_key(dt: date | None = None) -> str:
    if dt is None:
        dt = date.today()
    return dt.strftime("%Y-%m")


def _data_path(month_key: str) -> Path:
    return DATA_DIR / f"{month_key}.json"


def save_survey(schools: list[dict], survey_date: date | None = None) -> Path:
    if survey_date is None:
        survey_date = date.today()
    key = _month_key(survey_date)
    data = {
        "survey_date": survey_date.isoformat(),
        "schools": schools,
    }
    path = _data_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_survey(month_key: str) -> dict | None:
    path = _data_path(month_key)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_latest_two() -> tuple[dict | None, dict | None]:
    """Return (current_month, previous_month) survey data."""
    today = date.today()
    current_key = _month_key(today)

    prev_month = today.replace(day=1)
    if prev_month.month == 1:
        prev_month = prev_month.replace(year=prev_month.year - 1, month=12)
    else:
        prev_month = prev_month.replace(month=prev_month.month - 1)
    prev_key = _month_key(prev_month)

    return load_survey(current_key), load_survey(prev_key)


def list_available_months() -> list[str]:
    if not DATA_DIR.exists():
        return []
    keys = sorted(
        p.stem for p in DATA_DIR.glob("*.json")
    )
    return keys
