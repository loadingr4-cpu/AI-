#!/usr/bin/env python3
"""Google スプレッドシート用 CSV 生成モジュール"""

import csv
import io
from datetime import date
from pathlib import Path

from storage import load_latest_two

REPORTS_DIR = Path(__file__).parent / "reports"


def _detect_changes(current: dict, prev: dict | None) -> list[dict]:
    changes = []
    if not prev:
        return changes
    prev_map = {s["name"]: s for s in prev.get("schools", [])}
    for school in current.get("schools", []):
        name = school["name"]
        p = prev_map.get(name)
        if not p:
            changes.append({"塾名": name, "変更内容": "新規掲載", "種別": "新規"})
            continue
        cur_pay = school.get("hourly_pay_min")
        prv_pay = p.get("hourly_pay_min")
        if cur_pay and prv_pay and cur_pay != prv_pay:
            diff = cur_pay - prv_pay
            sign = "+" if diff > 0 else ""
            kind = "給与UP" if diff > 0 else "給与DOWN"
            changes.append({"塾名": name, "変更内容": f"時給 {prv_pay}→{cur_pay}円（{sign}{diff}円）", "種別": kind})
        cur_fmt = school.get("teaching_format")
        prv_fmt = p.get("teaching_format")
        if cur_fmt and prv_fmt and cur_fmt != prv_fmt:
            changes.append({"塾名": name, "変更内容": f"指導形態 {prv_fmt}→{cur_fmt}", "種別": "形態変更"})
        cur_min = school.get("session_minutes")
        prv_min = p.get("session_minutes")
        if cur_min and prv_min and cur_min != prv_min:
            changes.append({"塾名": name, "変更内容": f"コマ時間 {prv_min}→{cur_min}分", "種別": "時間変更"})
    return changes


def generate_csv(
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
        raise ValueError("調査データがありません。先に survey_runner.py を実行してください。")

    survey_date = current_data.get("survey_date", date.today().isoformat())
    schools = current_data.get("schools", [])
    changes = _detect_changes(current_data, prev_data)

    buf = io.StringIO()
    w = csv.writer(buf)

    # ── ヘッダー情報 ──
    w.writerow(["競合他塾 講師求人調査レポート"])
    w.writerow([f"調査日: {survey_date}", f"調査塾数: {len(schools)}塾", f"前月比変更: {len(changes)}件"])
    w.writerow([])

    # ── 前月からの変更点 ──
    w.writerow(["▼ 前月からの変更点"])
    w.writerow(["塾名", "種別", "変更内容"])
    if changes:
        for c in changes:
            w.writerow([c["塾名"], c["種別"], c["変更内容"]])
    else:
        w.writerow(["（変更なし）", "", ""])
    w.writerow([])

    # ── 塾別詳細一覧 ──
    w.writerow(["▼ 塾別詳細一覧"])
    w.writerow([
        "塾名", "自社/競合", "指導形態",
        "時給・代表値", "時給・最低", "時給・最高",
        "コマ給", "コマ時間（分）", "雇用形態", "対象学年",
        "福利厚生", "備考（大阪市内地域差など）", "参照URL",
    ])
    for s in schools:
        benefits = "／".join(s.get("benefits") or [])
        label = "◎自社" if s.get("is_own_company") else "競合"
        w.writerow([
            s.get("name", ""),
            label,
            s.get("teaching_format", ""),
            s.get("hourly_pay_mode") or "",
            s.get("hourly_pay_min") or "",
            s.get("hourly_pay_max") or "",
            s.get("session_pay") or "",
            s.get("session_minutes") or "",
            s.get("employment_type") or "",
            s.get("target_grades") or "",
            benefits,
            s.get("notes") or "",
            s.get("source_url") or "",
        ])

    csv_text = buf.getvalue()

    if output_path is None:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = REPORTS_DIR / f"{survey_date[:7]}-report.csv"

    output_path.write_text(csv_text, encoding="utf-8-sig")  # utf-8-sig = Excel/Sheets互換BOM付き
    print(f"CSVを生成しました: {output_path}")
    return output_path


if __name__ == "__main__":
    path = generate_csv()
    print(f"完了: {path}")
