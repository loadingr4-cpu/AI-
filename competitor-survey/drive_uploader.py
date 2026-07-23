#!/usr/bin/env python3
"""Google Drive へのレポートアップロードモジュール"""

from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_ID = "16NZeceeR72VLJHMSqPd9G4Tzqy_ocyMT"
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"


def _get_service():
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(f"credentials.json が見つかりません: {CREDENTIALS_PATH}")
    credentials = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_PATH), scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)


def upload_report(report_path: Path) -> str:
    """
    HTMLレポートをGoogleドライブにアップロード。
    同名ファイルが既にあれば上書き、なければ新規作成。
    Returns: 閲覧URL（失敗時は空文字）
    """
    if not report_path.exists():
        print(f"[Drive] エラー: レポートファイルが存在しません: {report_path}")
        return ""

    try:
        service = _get_service()
    except FileNotFoundError as e:
        print(f"[Drive] 認証エラー: {e}")
        return ""
    except Exception as e:
        print(f"[Drive] サービス初期化エラー: {e}")
        return ""

    filename = report_path.name

    try:
        query = f"name='{filename}' and '{FOLDER_ID}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id,name)").execute()
        existing = results.get("files", [])
    except HttpError as e:
        print(f"[Drive] ファイル検索エラー (HTTP {e.status_code}): {e}")
        return ""
    except Exception as e:
        print(f"[Drive] ファイル検索エラー: {e}")
        return ""

    media = MediaFileUpload(str(report_path), mimetype="text/html", resumable=False)

    try:
        if existing:
            file_id = existing[0]["id"]
            updated = service.files().update(
                fileId=file_id,
                media_body=media,
                fields="id,webViewLink",
            ).execute()
            link = updated.get("webViewLink", "")
            print(f"Googleドライブを更新しました: {link}")
        else:
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
    except HttpError as e:
        print(f"[Drive] アップロードエラー (HTTP {e.status_code}): {e}")
        return ""
    except Exception as e:
        print(f"[Drive] アップロードエラー: {e}")
        return ""

    return link


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使い方: python drive_uploader.py <report.html>")
        sys.exit(1)
    path = Path(sys.argv[1])
    url = upload_report(path)
    print(f"URL: {url}")
