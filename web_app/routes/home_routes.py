
# this is the "web_app/routes/home_routes.py" file...


from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from app.ss import SpreadsheetService
from app.email_service import send_email


home_routes = Blueprint("home_routes", __name__)






@home_routes.route("/")
@home_routes.route("/home")
def index():
    ss=SpreadsheetService()
    sheet, records =ss.get_records("books")
    #records = records[:12]
    query = request.args.get('query')

    if query:
        # Function to search books based on query
        total_books = ss.query_records("books", query)
        books = total_books[:12]
    else:
        # Function to get all books if no query
        books, total_books = ss.get_records("books")
        books = total_books[:12]


    return render_template("home.html", books=books)




    



@home_routes.route("/purchase", methods=["GET", "POST"])
def purchase():
    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)


    ss = SpreadsheetService()
    sheet, records = ss.get_records("books")

    # Get the book ID from URL parameters
    book_id = request.args.get('id')

    # Search for the book with the given ID
    book = next((record for record in records if str(record.get("id")) == book_id), None)

    if book:
        # Fetch the seller's email and name
        seller_email = book.get("user_email")
        # Assume you have a way to fetch the seller's name based on the email
        
        
        seller_name = book.get("user_name")  # Replace this with actual code to fetch the seller's name

        return render_template("purchase.html", book=book, seller_email=seller_email, seller_name=seller_name)
    else:
        return "Book not found", 404





@home_routes.route("/account")
def account():
    print("Displaying account information")
    ss = SpreadsheetService()

    my_books = []  # Initialize an empty list for user's books
    user = None  # Initialize user as None

    # Check if there is a current user in the session
    if 'current_user' in session:
        user = session['current_user']
        user_email = user.get('email')  # Assuming the user's email is stored under the key 'email'

        # Get all records from the 'books' sheet
        sheet, records = ss.get_records("books")

        # Filter records where user_email matches
        my_books = [record for record in records if record.get('user_email') == user_email]

    # Pass both my_books and user to the template
    return render_template("account.html", my_books=my_books, user=user)


@home_routes.route("/send-inquiry", methods=["GET", "POST"])
def send_inquiry():

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)


    inquiry_text = request.args.get('inquiry_text')

    print(inquiry_text)
    return render_template("send_inquiry.html", inquiry_text=inquiry_text)

@home_routes.route("/delist-book", methods=["POST"])
def delist_book():
    ss=SpreadsheetService()
    book_title = request.form.get('book_title')
    current_user = session['current_user'] 
    user_email = current_user.get('email')
    try:
        ss.remove_record("books", book_title, user_email)
        print("records found and removed")
    except:
        print("No records found for user and title")
    return redirect(url_for('home_routes.account'))

@home_routes.route("/inquiry-sent", methods=['POST'])
def inquiry_sent():
    inquiry_text = request.form.get('inquiry_text')
    seller_email = request.form.get('seller_email')
    send_email(seller_email, "YOU HAVE A POTENTIAL BOOK BUYER", inquiry_text)
    flash("Your inquiry has been sent")
    return redirect(url_for('home_routes.index'))


    print(inquiry_text)
    return render_template("send-inquiry.html", inquiry_text=inquiry_text)