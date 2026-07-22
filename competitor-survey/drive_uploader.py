#!/usr/bin/env python3
"""Google Drive へのレポートアップロードモジュール"""

from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_ID = "16NZeceeR72VLJHMSqPd9G4Tzqy_ocyMT"
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"


def _get_service():
    credentials = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_PATH), scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)


def upload_report(report_path: Path) -> str:
    """
    HTMLレポートをGoogleドライブにアップロード。
    同名ファイルが既にあれば上書き、なければ新規作成。
    Returns: 閲覧URL
    """
    service = _get_service()
    filename = report_path.name

    # 同名ファイルが既存フォルダ内にあるか確認
    query = f"name='{filename}' and '{FOLDER_ID}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id,name)").execute()
    existing = results.get("files", [])

    media = MediaFileUpload(str(report_path), mimetype="text/html", resumable=False)

    if existing:
        # 既存ファイルを上書き
        file_id = existing[0]["id"]
        updated = service.files().update(
            fileId=file_id,
            media_body=media,
            fields="id,webViewLink",
        ).execute()
        link = updated.get("webViewLink", "")
        print(f"Googleドライブを更新しました: {link}")
    else:
        # 新規アップロード
        metadata = {
            "name": filename,
            "parents": [FOLDER_ID],
            "mimeType": "text/html",
        }
        created = service.files().create(
            body=metadata,
            media_body=media,
            fields="id,webViewLink",
        ).execute()
        link = created.get("webViewLink", "")
        print(f"Googleドライブにアップロードしました: {link}")

    return link


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使い方: python drive_uploader.py <report.html>")
        sys.exit(1)
    path = Path(sys.argv[1])
    url = upload_report(path)
    print(f"URL: {url}")
