#!/usr/bin/env python3
"""メール送信モジュール（Gmail SMTP）"""

import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


def send_report(report_path: Path, survey_date: date | None = None) -> bool:
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    report_to = os.environ.get("REPORT_TO")

    if not all([smtp_user, smtp_pass, report_to]):
        print("メール設定が不完全です（SMTP_USER / SMTP_PASS / REPORT_TO を .env に設定してください）")
        return False

    if survey_date is None:
        survey_date = date.today()

    subject = f"【競合調査】{survey_date.year}年{survey_date.month}月 関西個別指導塾 講師求人レポート"

    html_body = report_path.read_text(encoding="utf-8")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = report_to
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [report_to], msg.as_string())
        print(f"レポートをメール送信しました: {report_to}")
        return True
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使い方: python emailer.py <report.html>")
        sys.exit(1)
    path = Path(sys.argv[1])
    send_report(path)
