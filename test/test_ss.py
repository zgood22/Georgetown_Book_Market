import os
from datetime import datetime, timezone
from pprint import pprint

from flask import session

from dotenv import load_dotenv
import gspread
from gspread.exceptions import SpreadsheetNotFound
from app.ss import SpreadsheetService

load_dotenv()


ss = SpreadsheetService()
#
def test_create_records():
    new_record = {
        "id": "test", 
        "user_email": "test@test.com",  # Use a valid email format for consistency
        "user_name": "Test User",
        "genre": "Test Genre",
        "title": "Test Title",
        "author": "Test Author",
        "published_date": "2023-03-08",
        "condition": "New",
        "list_price": "10.99",
        "image_url": "http://testurl.com/testimage.jpg",
        "created_at": "2023-03-08 19:59:16.471152+00:00"
    }
    
    ss.create_records("books", new_record)  # Assuming "books" is the correct sheet name
    
    sheet, records = ss.get_records("books")
    record = [book for book in records if book['title'].lower() == "test title"]
    
    assert len(record) > 0 and record[0]['title'] == "Test Title"



def test_get_records():
    sheet, records = ss.get_records("books")
    assert records[1]['genre'] == "Fiction"


def test_query_record():
    record = ss.query_records("books", "Mockingjay")
    
    assert record('title') == "Mockingjay"
    





