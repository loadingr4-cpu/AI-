#!/usr/bin/env python3
"""
競合他塾 講師求人 月次調査スクリプト

フロー:
  1. config の source_urls を requests で直接フェッチ
  2. 掲載終了 / エラーの場合は全8媒体を web_search_20250305 で再検索
  3. それでも見つからない場合のみ「取得不能」として記録・報告
"""

import json
import os
import re
import sys
import textwrap
from datetime import date
from pathlib import Path

import requests as http
import anthropic
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from config import COMPETITORS, SURVEY_SCHEMA
from storage import save_survey

# 求人情報を探す8媒体
SEARCH_DOMAINS = [
    "jukunavi.com",
    "juku.st",
    "baito.mynavi.jp",
    "indeed.com",
    "jukukoushi.jp",
    "townwork.net",
    "baitoru.com",
    "gaku-baito.com",
]

# 掲載終了・エラーページの判定キーワード
EXPIRED_MARKERS = [
    "掲載終了", "この求人は終了", "求人が見つかりません",
    "ページが見つかりません", "お探しのページが", "404 Not Found",
    "このページは存在しません", "求人掲載が終了", "募集を終了",
    "現在この求人は掲載していません",
]

FETCH_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja,en;q=0.9",
}

SYSTEM_PROMPT = textwrap.dedent("""
あなたは日本の学習塾業界の求人情報を専門的に調査するアナリストです。
提供されたHTMLから、大阪市内の個別指導塾講師求人情報を正確に抽出してください。

重要なルール:
- 大阪市内の教室データを優先（梅田・なんばの超繁華街特殊案件は除外し、一般的な相場を記録）
- 時給代表値 = 求人ページ記載の基本額
- 大阪府最低賃金（1,177円/時）を下回る値は入力しない
- 確認できない項目は null
- source_url は実際に参照したURLを記録
""").strip()

EXTRACT_PROMPT = textwrap.dedent("""
以下は「{school_name}」の講師求人ページのHTMLです。
大阪市内の教室に関する求人情報を抽出してJSON形式で返してください。

参照URL: {source_url}

HTML（先頭部分）:
{html}

スキーマ定義:
{schema}

必ず以下のJSONのみを返してください（```json〜```で囲んでも可）:
{{
  "name": "{school_name}",
  "is_own_company": false,
  "teaching_format": null,
  "hourly_pay_min": null,
  "hourly_pay_max": null,
  "hourly_pay_mode": null,
  "session_pay": null,
  "session_minutes": null,
  "benefits": [],
  "employment_type": null,
  "target_grades": null,
  "source_url": "{source_url}",
  "notes": null
}}
""").strip()

SEARCH_URL_PROMPT = textwrap.dedent("""
「{school_name}」（大阪市内）の塾講師・家庭教師アルバイト求人を以下の媒体で検索してください。

検索ワード: {keywords}
対象媒体: {domains}

掲載中（掲載終了でない）の求人ページURLを最大5件、JSON配列で返してください。
見つからない場合は空配列 [] を返してください。

["https://...", ...]
""").strip()


def fetch_page(url: str) -> str | None:
    """URLのHTMLを取得。失敗時はNone。"""
    try:
        r = http.get(url, headers=FETCH_HEADERS, timeout=10, allow_redirects=True)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return None


def is_expired(html: str) -> bool:
    """掲載終了・エラーページを判定。"""
    return any(marker in html for marker in EXPIRED_MARKERS)


def html_to_text(html: str) -> str:
    """HTMLからスクリプト・スタイル・ナビを除去し、本文テキストを抽出。"""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    # 連続する空行を圧縮
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)[:8000]


def _parse_json_from_text(text: str):
    """テキストからJSONを抽出してパース。失敗時はNone。"""
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def extract_from_html(client: anthropic.Anthropic, school_name: str, html: str, source_url: str) -> dict | None:
    """HTMLをClaudeに渡して構造化データを抽出。BeautifulSoupで本文テキスト化してから渡す。"""
    page_text = html_to_text(html)
    prompt = EXTRACT_PROMPT.format(
        school_name=school_name,
        source_url=source_url,
        html=page_text,
        schema=json.dumps(SURVEY_SCHEMA, ensure_ascii=False, indent=2),
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if hasattr(block, "text"):
            result = _parse_json_from_text(block.text)
            if isinstance(result, dict):
                return result
    return None


def _run_web_search(client: anthropic.Anthropic, prompt: str) -> str:
    """web_search_20250305 ツールを使って検索し、最終テキスト応答を返す。"""
    messages = [{"role": "user", "content": prompt}]
    tools = [{"type": "web_search_20250305", "name": "web_search"}]

    for _ in range(8):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": getattr(block, "content", ""),
                    })
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        else:
            break
    return ""


def search_all_domains(client: anthropic.Anthropic, school: dict) -> dict | None:
    """全8媒体をweb_searchで再検索し、有効な求人ページのデータを返す。"""
    name = school["name"]
    keywords = "、".join(school["search_keywords"])
    domains_str = " / ".join(SEARCH_DOMAINS)

    prompt = SEARCH_URL_PROMPT.format(
        school_name=name,
        keywords=keywords,
        domains=domains_str,
    )

    text = _run_web_search(client, prompt)

    # テキストからURL配列を抽出
    urls: list[str] = []
    candidate = _parse_json_from_text(text)
    if isinstance(candidate, list):
        urls = [u for u in candidate if isinstance(u, str) and u.startswith("http")]
    else:
        urls = re.findall(r'https?://[^\s"\'>\]]+', text)

    # 対象媒体のURLのみに絞り込み
    urls = [u for u in urls if any(d in u for d in SEARCH_DOMAINS)]

    for url in urls[:5]:
        html = fetch_page(url)
        if html is None:
            print(f"    → {url} フェッチ失敗")
            continue
        if is_expired(html):
            print(f"    → {url} 掲載終了")
            continue
        result = extract_from_html(client, name, html, url)
        if result:
            print(f"    → {url} 取得成功")
            return result

    return None


def survey_school(client: anthropic.Anthropic, school: dict) -> dict:
    name = school["name"]

    print(f"  調査中: {name}", flush=True)

    # ── Phase 1: 既知のsource_urlsを直接フェッチ ──
    has_source_urls = bool(school.get("source_urls"))
    any_expired = False

    for url in school.get("source_urls", []):
        html = fetch_page(url)
        if html is None:
            print(f"    → {url} フェッチ失敗")
            any_expired = True
            continue
        if is_expired(html):
            print(f"    → {url} 掲載終了")
            any_expired = True
            continue
        result = extract_from_html(client, name, html, url)
        if result:
            return result

    # ── Phase 2: 全8媒体をweb_searchで再検索 ──
    if has_source_urls and any_expired:
        print(f"    掲載終了/エラーあり → 全8媒体再検索中 ({name})...", flush=True)
    elif not has_source_urls:
        print(f"    source_url未設定 → 全8媒体検索 ({name})...", flush=True)
    else:
        print(f"    全8媒体検索 ({name})...", flush=True)

    result = search_all_domains(client, school)
    if result:
        return result

    # ── Phase 3: 取得不能を記録・報告 ──
    print(f"  [要報告] {name}: 全8媒体検索でも求人が見つかりませんでした", flush=True)
    return {
        "name": name,
        "is_own_company": school.get("is_own_company", False),
        "teaching_format": None,
        "hourly_pay_min": None,
        "hourly_pay_max": None,
        "hourly_pay_mode": None,
        "session_pay": None,
        "session_minutes": None,
        "benefits": [],
        "employment_type": None,
        "target_grades": None,
        "source_url": None,
        "notes": "全8媒体（jukunavi/juku.st/indeed等）検索でも求人情報が見つかりませんでした",
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
    print(f"検索媒体: {', '.join(SEARCH_DOMAINS)}")
    print()

    schools = []
    not_found_names: list[str] = []

    for school in COMPETITORS:
        try:
            result = survey_school(client, school)
            result["is_own_company"] = school.get("is_own_company", False)
            schools.append(result)

            if "全8媒体" in (result.get("notes") or ""):
                not_found_names.append(school["name"])
                pay_info = "取得不能"
            elif result.get("hourly_pay_min"):
                pay_info = f"時給 {result['hourly_pay_min']}〜{result['hourly_pay_max']}円"
            elif result.get("session_pay"):
                pay_info = f"コマ給 {result['session_pay']}円"
            else:
                pay_info = "給与情報なし"
            print(f"  完了: {school['name']} - {pay_info}", flush=True)

        except Exception as e:
            print(f"  エラー: {school['name']} - {e}", flush=True)
            schools.append({
                "name": school["name"],
                "is_own_company": school.get("is_own_company", False),
                "teaching_format": None,
                "hourly_pay_min": None,
                "hourly_pay_max": None,
                "hourly_pay_mode": None,
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

    if not_found_names:
        print("\n【要確認】以下の塾は全8媒体検索でも求人が見つかりませんでした:")
        for n in not_found_names:
            print(f"  - {n}")

    return path


if __name__ == "__main__":
    run_survey()
