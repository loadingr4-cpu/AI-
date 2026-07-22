#!/usr/bin/env python3
"""
競合他塾調査 メインエントリーポイント

1. 求人調査（survey_runner.py）
2. HTMLレポート生成（report_generator.py）
3. メール送信（emailer.py）

使い方:
  python main.py               # 調査→レポート→メール送信
  python main.py --report-only # 既存データからレポートのみ再生成
  python main.py --no-email    # 調査→レポート（メール送信なし）
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


def main():
    parser = argparse.ArgumentParser(description="競合他塾 講師求人 月次調査")
    parser.add_argument("--report-only", action="store_true", help="既存データからレポートのみ再生成")
    parser.add_argument("--no-email", action="store_true", help="メール送信をスキップ")
    args = parser.parse_args()

    report_path = None

    if not args.report_only:
        from survey_runner import run_survey
        data_path = run_survey()
        print(f"\nデータ保存: {data_path}")

    from report_generator import generate_report
    report_path = generate_report()
    print(f"レポート生成: {report_path}")

    from drive_uploader import upload_report
    drive_url = upload_report(report_path)
    if drive_url:
        print(f"ドライブURL: {drive_url}")

    print("\n=== 完了 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
