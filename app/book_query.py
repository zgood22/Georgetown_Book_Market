from dotenv import load_dotenv
import os
import requests
from app.ss import SpreadsheetService

# Load environment variables from a .env file
load_dotenv()

# Get the ISBNdb API key from environment variables
ISBNdb_key = os.getenv("ISBNdb_key")

# Initialize SpreadsheetService
ss = SpreadsheetService()

def get_book_details(title, condition=None, list_price=None):

    headers = {'Authorization': ISBNdb_key}
    url = f'https://api.isbndb.com/books/{title}'

    # Send a GET request to the ISBNdb API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        books = data.get('books', [])

        if books:
            # Limit the results to top 30 books
            top_books = books[:30]

            # Prepare the list of book details
            book_details = []
            for book in top_books:
                # Add condition and listPrice to book_info
                book_info = {
                    'title': book.get('title', 'Title not found'),
                    'author': book.get('authors', 'Author not found'),
                    'image_url': book.get('image', 'Image not available'),
                    'published_date': book.get('date_published', 'Publish date not available'),
                    'condition': condition,  # Now included in book_info
                    'list_price': list_price,   # Now included in book_info

                }
                
                book_details.append(book_info)

            return book_details
        else:
            return "No book found with that title."
    else:
        return "Failed to retrieve data from ISBNdb."

# The part below is correct, assuming it's meant for a simple CLI interaction
if __name__ == '__main__':
    book_search = input('Please enter the name of the book you are searching for: ')
    book_details = get_book_details(book_search)
    print(book_details[1])  # This will print the second book's details if there are at least two books
