#!/usr/bin/env python3
"""HTML レポート生成モジュール"""

from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from storage import load_latest_two, load_survey

TEMPLATES_DIR = Path(__file__).parent / "templates"
REPORTS_DIR = Path(__file__).parent / "reports"


def _pay_label(school: dict) -> str:
    if school.get("hourly_pay_min"):
        lo = school["hourly_pay_min"]
        hi = school.get("hourly_pay_max") or lo
        return f"{lo}〜{hi}円/h"
    if school.get("session_pay"):
        return f"コマ給{school['session_pay']}円"
    return "不明"


def _detect_changes(current: dict, prev: dict | None) -> tuple[list[dict], list[dict]]:
    """
    Returns:
        changes: list of change dicts for the banner
        rows_with_change: enriched row list with change info
    """
    changes = []
    rows = []

    prev_map = {}
    if prev:
        prev_map = {s["name"]: s for s in prev.get("schools", [])}

    for school in current.get("schools", []):
        name = school["name"]
        row = dict(school)
        row["change_summary"] = None
        row["change_type"] = "neutral"

        prev_school = prev_map.get(name)
        if not prev_school:
            row["change_summary"] = "新規"
            row["change_type"] = "new"
            changes.append({"type": "new", "type_label": "新規", "school": name, "detail": "今月初めて掲載"})
        else:
            diffs = []

            # Time pay change
            cur_pay = school.get("hourly_pay_min")
            prv_pay = prev_school.get("hourly_pay_min")
            if cur_pay and prv_pay and cur_pay != prv_pay:
                diff = cur_pay - prv_pay
                sign = "+" if diff > 0 else ""
                diffs.append(f"時給 {prv_pay}→{cur_pay}円（{sign}{diff}）")
                if diff > 0:
                    changes.append({"type": "up", "type_label": "↑給与UP", "school": name, "detail": f"時給 {prv_pay}→{cur_pay}円（{sign}{diff}円）"})
                else:
                    changes.append({"type": "down", "type_label": "↓給与DOWN", "school": name, "detail": f"時給 {prv_pay}→{cur_pay}円（{sign}{diff}円）"})

            # Teaching format change
            cur_fmt = school.get("teaching_format")
            prv_fmt = prev_school.get("teaching_format")
            if cur_fmt and prv_fmt and cur_fmt != prv_fmt:
                diffs.append(f"指導形態 {prv_fmt}→{cur_fmt}")
                changes.append({"type": "chg", "type_label": "形態変更", "school": name, "detail": f"指導形態 {prv_fmt}→{cur_fmt}"})

            # Session minutes change
            cur_min = school.get("session_minutes")
            prv_min = prev_school.get("session_minutes")
            if cur_min and prv_min and cur_min != prv_min:
                diffs.append(f"コマ時間 {prv_min}→{cur_min}分")
                changes.append({"type": "chg", "type_label": "時間変更", "school": name, "detail": f"コマ時間 {prv_min}→{cur_min}分"})

            if diffs:
                row["change_summary"] = " ／ ".join(diffs)
                row["change_type"] = "up" if "給与UP" in " ".join(d.get("type_label", "") for d in changes if d["school"] == name) else "chg"

        rows.append(row)

    return changes, rows


def generate_report(
    current_data: dict | None = None,
    prev_data: dict | None = None,
    output_path: Path | None = None,
) -> Path:
    if current_data is None or prev_data is None:
        cur, prv = load_latest_two()
        if current_data is None:
            current_data = cur
        if prev_data is None:
            prev_data = prv

    if not current_data:
        raise ValueError("現在の調査データがありません。先に survey_runner.py を実行してください。")

    survey_date_str = current_data.get("survey_date", date.today().isoformat())
    survey_date = date.fromisoformat(survey_date_str)

    changes, rows = _detect_changes(current_data, prev_data)

    # Summary stats
    pays = [
        s.get("hourly_pay_max") or s.get("hourly_pay_min")
        for s in current_data.get("schools", [])
        if s.get("hourly_pay_max") or s.get("hourly_pay_min")
    ]
    min_pays = [
        s.get("hourly_pay_min")
        for s in current_data.get("schools", [])
        if s.get("hourly_pay_min")
    ]

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    template = env.get_template("report.html")

    html = template.render(
        year=survey_date.year,
        month=survey_date.month,
        survey_date=survey_date_str,
        total_schools=len(current_data.get("schools", [])),
        max_pay=max(pays) if pays else "—",
        min_pay=min(min_pays) if min_pays else "—",
        change_count=len(changes),
        changes=changes,
        rows=rows,
    )

    if output_path is None:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = REPORTS_DIR / f"{survey_date_str[:7]}-report.html"

    output_path.write_text(html, encoding="utf-8")
    print(f"レポートを生成しました: {output_path}")
    return output_path


if __name__ == "__main__":
    path = generate_report()
    print(f"完了: {path}")
