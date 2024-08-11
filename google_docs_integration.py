import os
import traceback
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import re

load_dotenv()


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        title = re.sub(r'[\[\]]', '', lines[0].strip())
        content = ''.join(lines[2:]).strip()
    return title, content


def get_document_length(service, document_id):
    document = service.documents().get(documentId=document_id).execute()
    return document.get('body').get('content')[-1].get('endIndex')


def create_tables_with_content(service, document_id, files):
    current_index = 0
    for original_text_path, translated_text_path in files:
        print(f"handle {original_text_path}...")
        original_title, original_content = read_file_content(original_text_path)
        translated_title, translated_content = read_file_content(translated_text_path)

        requests = [
            {
                "insertTable": {
                    "rows": 2,
                    "columns": 2,
                    "location": {
                        "index": current_index + 1
                    }
                }
            },
            {
                "insertText": {
                    "text": translated_content,
                    "location": {
                        "index": current_index + 12
                    }
                }
            },
            {
                "insertText": {
                    "text": original_content,
                    "location": {
                        "index": current_index + 10
                    }
                }
            },
            {
                "insertText": {
                    "text": translated_title,
                    "location": {
                        "index": current_index+ 7
                    }
                }
            },
            {
                "insertText": {
                    "text": original_title,
                    "location": {
                        "index": current_index+ 5
                    }
                }
            }
        ]


        service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        print("Content inserted successfully.")

        # 獲取最新的文檔長度
        current_index = get_document_length(service, document_id) - 2
        print(f"Updated document length: {current_index}")


def create_google_doc():
    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    try:
        service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

        file_metadata = {
            'name': 'Translated Lyrics',
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.document'
        }

        file = drive_service.files().create(body=file_metadata).execute()
        document_id = file.get('id')

        print(f"Document created with ID: {document_id}")

        text_files = sorted(
            [f for f in os.listdir('text') if f.endswith('.txt') and 'lyrics' in f and 'translated' not in f],
            key=lambda x: int(re.search(r'\d+', x).group())
        )

        lyrics_files = [(os.path.join('text', f), os.path.join('text', f.replace('-lyrics', '-lyrics-translated'))) for
                        f in text_files]

        create_tables_with_content(service, document_id, lyrics_files)

        print(f"Document created with ID: {document_id} in folder ID: {folder_id}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    create_google_doc()
