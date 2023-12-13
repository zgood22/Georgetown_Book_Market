from flask import Blueprint, request, render_template
from app.book_query import get_book_details
from app.ss import SpreadsheetService



#from web_app.book_routes import listing_search

from app.ss import SpreadsheetService



book_routes = Blueprint("book_routes", __name__)


# Assuming you have an existing Blueprint named 'book_routes'
# If not, replace 'book_routes' with your Blueprint name or app

@book_routes.route('/new-listing')
def new_listing():
    return render_template('book_form.html')

@book_routes.route('/listing-search', methods=["GET", "POST"])
def listing_search():
    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    author_fname = str(request_data.get("authorFirstName"))
    author_lname = str(request_data.get("authorLastName"))
    author_fullname = author_fname + " " + author_lname
    condition = request_data.get("condition")
    list_price = request_data.get("list_price")
    book_title = str(request_data.get("title"))
    book_results = get_book_details(book_title, condition, list_price)
    # ... existing code ...
    print(condition, list_price)
    return render_template('listing_search.html', book_title=book_title, author_fullname=author_fullname, condition=condition, list_price=list_price, book_results=book_results)


@book_routes.route('/selected-book', methods=["GET", "POST"])
def selected_book():
    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    book_details = {
        'title': request.form.get('title'),
        'author': request.form.get('author'),
        'published_date': request.form.get('published_date'),
        'image_url': request.form.get('image_url'),
        'condition': request.form.get('condition'),
        'list_price': request.form.get('list_price'),
        'created_at': request.form.get('created_at'),
    }
    


    ss = SpreadsheetService()
    print("Book Details:", book_details)
    ss.create_records("books", book_details)
    return render_template('selected_book.html', book_details=book_details)
