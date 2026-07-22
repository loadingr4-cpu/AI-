#!/usr/bin/env python3
"""
競合他塾 講師求人 月次調査スクリプト

Anthropic API + web_search ツールを使い、関西の個別指導塾の
講師求人情報（コマ給・時給・指導形態・福利厚生）を収集して
data/YYYY-MM.json に保存する。
"""

import json
import os
import sys
import textwrap
from datetime import date
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from config import COMPETITORS, SURVEY_SCHEMA
from storage import save_survey

SYSTEM_PROMPT = textwrap.dedent("""
あなたは日本の学習塾業界の求人情報を専門的に調査するアナリストです。
ウェブ検索を使って指定された個別指導塾の講師（家庭教師・塾講師）の
求人情報を収集し、以下の情報を正確に抽出してください。

抽出する情報:
- 指導形態（生徒:講師の比率、例: 1:1, 1:2, 1:3）
- 時給（下限・上限）
- コマ給（1コマあたりの給与）
- 1コマの授業時間（分）
- 福利厚生（交通費、社保、制服など）
- 雇用形態（アルバイト/正社員/業務委託）
- 対象学年（小学生〜高校生など）
- 求人の参照URL

情報が見つからない場合は null を使用してください。
複数の求人がある場合は最も代表的・最新のものを採用してください。
必ずJSON形式で回答してください。
""").strip()

EXTRACT_PROMPT_TEMPLATE = textwrap.dedent("""
「{school_name}」（関西・大阪府内）の講師（塾講師・家庭教師）アルバイト求人を
ウェブで検索し、以下のJSON形式で情報を返してください。

検索キーワードの例: {keywords}

返却するJSONのスキーマ:
{schema}

必ず以下のJSONのみを返してください（説明文は不要）:
{{
  "name": "{school_name}",
  "teaching_format": ...,
  "hourly_pay_min": ...,
  "hourly_pay_max": ...,
  "session_pay": ...,
  "session_minutes": ...,
  "benefits": [...],
  "employment_type": ...,
  "target_grades": ...,
  "source_url": ...,
  "notes": ...
}}
""").strip()


def survey_school(client: anthropic.Anthropic, school: dict) -> dict:
    prompt = EXTRACT_PROMPT_TEMPLATE.format(
        school_name=school["name"],
        keywords="、".join(school["search_keywords"]),
        schema=json.dumps(SURVEY_SCHEMA, ensure_ascii=False, indent=2),
    )

    print(f"  調査中: {school['name']}", flush=True)

    messages = [{"role": "user", "content": prompt}]
    tools = [{"type": "web_search_20250305", "name": "web_search"}]

    # Agentic loop: allow multiple tool-use rounds
    for _ in range(8):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        # Append assistant turn
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Extract text from final response
            for block in response.content:
                if hasattr(block, "text"):
                    text = block.text.strip()
                    # Strip markdown code fences if present
                    if text.startswith("```"):
                        text = text.split("```")[1]
                        if text.startswith("json"):
                            text = text[4:]
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        pass
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    # web_search results are already in block.content for server-side tools
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": getattr(block, "content", ""),
                    })
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        else:
            break

    # Fallback: return minimal record if extraction failed
    print(f"  警告: {school['name']} のデータ抽出に失敗しました", flush=True)
    return {
        "name": school["name"],
        "teaching_format": None,
        "hourly_pay_min": None,
        "hourly_pay_max": None,
        "session_pay": None,
        "session_minutes": None,
        "benefits": [],
        "employment_type": None,
        "target_grades": None,
        "source_url": school.get("recruitment_url"),
        "notes": "データ取得失敗",
    }


def run_survey() -> Path:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("エラー: ANTHROPIC_API_KEY が設定されていません。.env ファイルを確認してください。")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    today = date.today()

    print(f"=== 競合他塾調査開始: {today.strftime('%Y年%m月%d日')} ===")
    print(f"対象塾数: {len(COMPETITORS)}")
    print()

    schools = []
    for school in COMPETITORS:
        try:
            result = survey_school(client, school)
            schools.append(result)
            pay_info = (
                f"時給 {result['hourly_pay_min']}〜{result['hourly_pay_max']}円"
                if result.get("hourly_pay_min")
                else f"コマ給 {result.get('session_pay')}円"
                if result.get("session_pay")
                else "給与情報なし"
            )
            print(f"  完了: {school['name']} - {pay_info}", flush=True)
        except Exception as e:
            print(f"  エラー: {school['name']} - {e}", flush=True)
            schools.append({
                "name": school["name"],
                "teaching_format": None,
                "hourly_pay_min": None,
                "hourly_pay_max": None,
                "session_pay": None,
                "session_minutes": None,
                "benefits": [],
                "employment_type": None,
                "target_grades": None,
                "source_url": school.get("recruitment_url"),
                "notes": f"エラー: {e}",
            })

    path = save_survey(schools, today)
    print(f"\n調査データを保存しました: {path}")
    return path


if __name__ == "__main__":
    run_survey()
