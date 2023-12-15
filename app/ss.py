# adapted from:
# ... https://developers.google.com/sheets/api/guides/authorizing
# ... https://gspread.readthedocs.io/en/latest/oauth2.html
# ... https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# ... https://github.com/s2t2/birthday-wishes-py/blob/master/app/sheets.py
# ... https://raw.githubusercontent.com/prof-rossetti/flask-sheets-template-2020/master/web_app/spreadsheet_service.py

import os
from datetime import datetime, timezone
from pprint import pprint

from flask import session

from dotenv import load_dotenv
import gspread
from gspread.exceptions import SpreadsheetNotFound


load_dotenv()

DEFAULT_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "google-credentials.json")
GOOGLE_CREDENTIALS_FILEPATH = os.getenv("GOOGLE_CREDENTIALS_FILEPATH", default=DEFAULT_FILEPATH)

GOOGLE_SHEETS_DOCUMENT_ID = os.getenv("GOOGLE_SHEETS_DOCUMENT_ID", default="OOPS Please get the spreadsheet identifier from its URL, and set the 'GOOGLE_SHEETS_DOCUMENT_ID' environment variable accordingly...")


class SpreadsheetService:
    # TODO: consider implementing a locking mechanism on sheet writes, to prevent overwriting (if it becomes an issue)
    # ... however we know that if we want a more serious database solution, we would choose SQL database (and this app is just a small scale demo)

    def __init__(self, credentials_filepath=GOOGLE_CREDENTIALS_FILEPATH, document_id=GOOGLE_SHEETS_DOCUMENT_ID):
        print("INITIALIZING NEW SPREADSHEET SERVICE...")

        #self.credentials = credentials or ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
        #self.credentials = ServiceAccountCredentials._from_parsed_json_keyfile(json.loads(GOOGLE_API_CREDENTIALS), AUTH_SCOPE)
        #self.client = gspread.authorize(self.credentials) #> <class 'gspread.client.Client'>
        self.client = gspread.service_account(filename=credentials_filepath)

        self.document_id = document_id

        # TODO: consider storing and caching the latest version of each sheet, given the small number of sheets
        # ... showing preference for speed over brevity
        #self.products_sheet = None
        #self.orders_sheet = None

    @property
    def doc(self):
        """note: this will make an API call each time, to get the new data"""
        return self.client.open_by_key(self.document_id) #> <class 'gspread.models.Spreadsheet'>

    def get_sheet(self, sheet_name):
        return self.doc.worksheet(sheet_name)

    @staticmethod
    def generate_timestamp():
        return datetime.now(tz=timezone.utc)

    @staticmethod
    def parse_timestamp(ts:str):
        """
            ts (str) : a timestamp string like '2023-03-08 19:59:16.471152+00:00'
        """
        date_format = "%Y-%m-%d %H:%M:%S.%f%z"
        return datetime.strptime(ts, date_format)

    
    def get_records(self, sheet_name):
        """Gets all records from a sheet,
            converts datetime columns back to Python datetime objects
        """
    

        #print(f"GETTING RECORDS FROM SHEET: '{sheet_name}'")
        sheet = self.get_sheet(sheet_name) #> <class 'gspread.models.Worksheet'>

        raw_records = sheet.get_all_records() #> <class 'list'>

        records = [record for record in raw_records if any(value != '' for value in record.values())]



        for record in records:
            if record.get("created_at"):
                record["created_at"] = self.parse_timestamp(record["created_at"])
        return sheet, records
    
    def create_records(self, sheet_name: str, new_record: dict):
        model_class = {"products": Product, "orders": Order, "books": Book}[sheet_name]

        sheet, records = self.get_records(sheet_name)
        next_row_number = len(records) + 2  # plus headers plus one

        #print(records)
        


        # auto-increment integer identifier
        if any(records):
        # Ensure each id is an integer
            existing_ids = [int(r["id"]) for r in records if isinstance(r["id"], (int, str)) and str(r["id"]).isdigit()]
            next_id = max(existing_ids) + 1
        else:
            next_id = 1

         #Get user email
        def user_email():
            if 'current_user' in session:
                user_email = session['current_user']['email']
                return user_email
        
        def user_name():
            if 'current_user' in session:
                user_name = session['current_user']['name']
                return user_name
        
        
        


        # Create a new dictionary with the updated values
        updated_record = {
            "id": next_id,
            "user_email": user_email(),
            "user_name": user_name(),
            "genre": new_record["genre"],
            "title": new_record["title"],
            "author": new_record["author"],
            "published_date": new_record["published_date"],
            "condition": new_record["condition"],
            "list_price": new_record["list_price"],
            "image_url": new_record["image_url"],
            "created_at": '2023-03-08 19:59:16.471152+00:00',
        }

        new_row = model_class(updated_record).to_row

        sheet.insert_rows([new_row], row=next_row_number)

    def remove_record(self, sheet_name: str, book_title: str, user_email: str):
        """
        Removes a record from the specified sheet based on the book's title and user email.

        Params:
            sheet_name (str): the name of the sheet (e.g., "books")
            book_title (str): the title of the book to remove
            user_email (str): the email of the user associated with the book
        """

        # Get the sheet and all current records
        sheet, records = self.get_records(sheet_name)
        print("Step 1 achieved")

        # Find the row number of the record to remove
        row_to_remove = None
        for idx, record in enumerate(records, start=2):  # start=2 to account for header row
            if record.get("title") == book_title and record.get("user_email") == user_email:
                row_to_remove = idx
                break

        # If the record is found, delete the row
        if row_to_remove:
            sheet.delete_rows(row_to_remove)
            print(f"Book titled '{book_title}' by user '{user_email}' removed from '{sheet_name}' sheet.")
        else:
            print(f"No book titled '{book_title}' found for user '{user_email}'.")

    def query_records(self, sheet_name:str, book_title: str):
        sheet, records = self.get_records(sheet_name)
        filtered_books = [book for book in records if book_title.lower() in book['title'].lower()]
        return filtered_books

        

   




# FIXED SCHEMA / DECORATORS
# ... to make sure when writing to sheet the values are in the proper order

class Product:
    def __init__(self, attrs):
        self.id = attrs.get("id")
        self.name = attrs.get("name")
        self.description = attrs.get("description")
        self.price = attrs.get("price")
        self.url = attrs.get("url")
        self.created_at = attrs.get("created_at")

    @property
    def to_row(self):
        return [self.id, self.name, self.description, self.price, self.url, str(self.created_at)]


class Order:
    def __init__(self, attrs):
        self.id = attrs.get("id")
        self.user_email = attrs.get("user_email")
        self.product_id = attrs.get("product_id")
        self.product_name = attrs.get("product_name")
        self.product_price = attrs.get("product_price")
        self.created_at = attrs.get("created_at")


    @property
    def to_row(self):
        return [self.id, self.user_email, self.product_id, self.product_name, self.product_price, str(self.created_at)]


class Book:
    def __init__(self, attrs):
        self.id = attrs.get("id")
        self.user_email = attrs.get("user_email")
        self.user_name = attrs.get("user_name")
        self.genre = attrs.get("genre")
        self.title = attrs.get("title")
        self.author = attrs.get("author")
        self.published_date = attrs.get("published_date")
        self.condition = attrs.get("condition")
        self.list_price = attrs.get("list_price")
        self.image_url = attrs.get("image_url")
        self.created_at = attrs.get("created_at")
        
        
        


    @property
    def to_row(self):
        return[self.id, self.user_email, self.user_name, self.genre, self.title, self.author, self.published_date, self.condition, self.list_price, self.image_url, self.created_at]
    


