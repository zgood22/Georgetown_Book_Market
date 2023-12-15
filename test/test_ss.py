import os
from datetime import datetime, timezone
from pprint import pprint

from flask import session

from dotenv import load_dotenv
import gspread
from gspread.exceptions import SpreadsheetNotFound
from app.ss import SpreadsheetService

load_dotenv()

DEFAULT_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "google-credentials.json")
GOOGLE_CREDENTIALS_FILEPATH = os.getenv("GOOGLE_CREDENTIALS_FILEPATH", default=DEFAULT_FILEPATH)

GOOGLE_SHEETS_DOCUMENT_ID = os.getenv("GOOGLE_SHEETS_DOCUMENT_ID", default="OOPS Please get the spreadsheet identifier from its URL, and set the 'GOOGLE_SHEETS_DOCUMENT_ID' environment variable accordingly...")

ss = SpreadsheetService()

def test_create_records():
    new_record = {"id": "test", "user_email": "test","user_name": "test","genre": "test","title": "test","author": "test","published_date": "test","condition": "test","list_price": "test","image_url": "test","created_at": "2023-03-08 19:59:16.471152+00:00",}
    
    ss.create_records("test", new_record)
    
    sheet, records = ss.get_records("test")

    assert any(record for record in records if record["id"]=="test")


def test_get_records():
    sheet, records = ss.get_records("books")
    assert sheet == "books"


#def test_query_record():






