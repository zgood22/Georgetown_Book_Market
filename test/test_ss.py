import os
from datetime import datetime, timezone
import pytest


from dotenv import load_dotenv
from gspread import Spreadsheet as Document, Worksheet

from app.ss import SpreadsheetService



load_dotenv()

CI_ENV = (os.getenv("CI", default="false") == "true")
CI_SKIP_MESSAGE = "taking a lighter touch to testing on the CI server, to reduce API usage and prevent rate limits"

ss = SpreadsheetService()

#
def test_generate_timestamp():
    #dt = ss.generate_timestamp()
    dt = ss.generate_timestamp()
    assert isinstance(dt, datetime)
    assert dt.tzinfo == timezone.utc





def test_get_records():

    
    sheet, records = ss.get_records("books")
    assert records[1]['genre'] == "Fiction"



    





