import os
from dotenv import load_dotenv
import requests
from app.book_query import get_book_details

# Load environment variables from a .env file
load_dotenv()

# Get the ISBNdb API key from environment variables
ISBNdb_key = os.getenv("ISBNdb_key")

def test_get_book_detail():
    data = get_book_details("Dune", genre="Fiction", condition=None, list_price=None)
    assert isinstance(data, list)
    assert len(data) == 20
    assert data[0]['author'] == 'Herbert, Frank' 
    
    

