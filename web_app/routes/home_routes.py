
# this is the "web_app/routes/home_routes.py" file...

from flask import Blueprint, request, render_template
from app.ss import SpreadsheetService


home_routes = Blueprint("home_routes", __name__)


books = [
    {
        "image_url": "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGJvb2slMjBjb3ZlcnN8ZW58MHx8MHx8fDA%3D",
        "title": "The Art of Programming",
        "price": 29.99,
        "owner_email_address": "owner1@example.com"
    },
    {
        "image_url": "https://media.istockphoto.com/id/1210701957/vector/abstract-minimal-geometric-circle-background-for-business-annual-report-book-cover-brochure.jpg?s=612x612&w=0&k=20&c=ZfeNQNhrDFK_tZZqANCvuAg0eAEwJclsUYTb8_80k-Q=",
        "title": "Data Science Essentials",
        "price": 39.99,
        "owner_email_address": "owner2@example.com"
    },
    {
        "image_url": "https://i.pinimg.com/736x/6a/60/d9/6a60d9b3d79e81f52e34c7a4ebc65928.jpg",
        "title": "Introduction to Machine Learning",
        "price": 24.99,
        "owner_email_address": "owner3@example.com"
    },
    {
        "image_url": "https://marketplace.canva.com/EAFaQMYuZbo/1/0/1003w/canva-brown-rusty-mystery-novel-book-cover-hG1QhA7BiBU.jpg",
        "title": "Python for Beginners",
        "price": 19.99,
        "owner_email_address": "owner4@example.com"
    },
    {
        "image_url": "https://i.pinimg.com/736x/f6/e3/d6/f6e3d640a08ba14ce3291375ff7a7473.jpg",
        "title": "Web Development with Django",
        "price": 49.99,
        "owner_email_address": "owner5@example.com"
    },
    {
        "image_url": "https://edit.org/images/cat/book-covers-big-2019101610.jpg",
        "title": "Artificial Intelligence Explained",
        "price": 34.99,
        "owner_email_address": "owner6@example.com"
    },
    {
        "image_url": "https://img.freepik.com/free-psd/vertical-poster-template-with-travel-vegetation-style_23-2149432065.jpg?size=338&ext=jpg&ga=GA1.1.1222169770.1701907200&semt=ais",
        "title": "Blockchain Basics",
        "price": 44.99,
        "owner_email_address": "owner7@example.com"
    },
    {
        "image_url": "https://img.freepik.com/free-vector/bike-guy-wattpad-book-cover_23-2149452163.jpg?size=338&ext=jpg&ga=GA1.1.1222169770.1701907200&semt=ais",
        "title": "Mobile App Development with React Native",
        "price": 29.99,
        "owner_email_address": "owner8@example.com"
    },
    {
        "image_url": "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781982137373/the-night-she-disappeared-9781982137373_hr.jpg",
        "title": "Cybersecurity Fundamentals",
        "price": 39.99,
        "owner_email_address": "owner9@example.com"
    },
    {
        "image_url": "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781982173685/state-of-terror-9781982173685_hr.jpg",
        "title": "Game Development in Unity",
        "price": 49.99,
        "owner_email_address": "owner10@example.com"
    }
]



@home_routes.route("/")
@home_routes.route("/home")
def index():
    ss=SpreadsheetService()
    sheet, records =ss.get_records("books")
    records = records[:10]

    return render_template("home.html", books=records)


@home_routes.route("/about")
def about():
    print("ABOUT...")
    #return "About Me"
    return render_template("about.html")

