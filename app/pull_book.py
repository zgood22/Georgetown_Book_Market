from dotenv import load_dotenv
import os
import requests

# Load environment variables from a .env file
load_dotenv()

# Get the ISBNdb API key from environment variables
ISBNdb_key = os.getenv("ISBNdb_key")

# Define a base class to fetch book details
class BookDetails:
    def __init__(self, title):
        self.title = title
        self.author_name, self.edition, self.image_url, self.published_date = self.get_book_details()

    def get_book_details(self):
        api_key = ISBNdb_key
        url = f'https://api.isbndb.com/books/{self.title}'
        headers = {'Authorization': ISBNdb_key}

        # Send a GET request to the ISBNdb API
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            books = data.get('books', [])
            
            if books:
                book = books[0]  # Assuming we take the first book in the list

                # Extract book details from the API response
                author = book.get('authors', 'Author not found')
                edition = book.get('edition', 'Edition not available')
                image_url = book.get('image', 'Image not available')
                published_date = book.get('date_published', 'Publish date not available')

                return author, edition, image_url, published_date
            else:
                return "No book found with that title.", None, None, None
        else:
            return "Failed to retrieve data from ISBNdb.", None, None, None

# Define a class for selling a book that inherits from BookDetails
class BookSell(BookDetails): #NEEDS functionality that stores a book for sale in the google sheets database 
    def __init__(self, title):
        super().__init__(title)
        self.list_price = 0  # Initialize list price to 0
        self.condition = 0

    def set_list_price(self, list_price):
        try:
            # Convert the input to an integer
            list_price = int(list_price)

            # Check if the input is a positive integer
            if list_price > 0:
                self.list_price = list_price
            else:
                print("List price must be a positive integer. ")
                self.set_list_price(input("Invalid list price. Enter a postive integer for the list price. "))
        except ValueError:
            print("Invalid list price. Please enter a positive integer for the list price. ")
            self.set_list_price(input("Invalid list price. Enter a postiive integer for list price. "))

    def set_condition(self, condition):
        try:
            condition = int(condition)
            if 1 <= condition <= 5:
                self.condition = condition
            else:
                print("Invalid condition. Please enter a number from 1 to 5.")
                self.set_condition(input("Enter Condition (1 to 5 Stars): "))
        except ValueError:
            print("Invalid condition. Please enter a valid number.")
            self.set_condition(input("Enter Condition (1 to 5 Stars): "))

    def display_sell_info(self):
        print("\nSell Information:")
        print("Book Title:", self.title)
        print("Author Name:", self.author_name)
        print("Edition:", self.edition)
        print("Image URL:", self.image_url)
        print("Published Date:", self.published_date)
        print("List Price: $" + str(self.list_price))
        print("Condition:", self.condition, "stars")

# Define a class for exchanging a book that inherits from BookDetails
class BookExchange(BookDetails): #NEEDS functionality that stores a book for exchange in the google sheets database 
    def __init__(self, title):
        super().__init__(title)
        self.exchange_condition = 0

    def set_exchange_condition(self, exchange_condition):
        try:
            exchange_condition = int(exchange_condition)
            if 1 <= exchange_condition <= 5:
                self.exchange_condition = exchange_condition
            else:
                print("Invalid exchange condition. Please enter a number from 1 to 5.")
                self.set_exchange_condition(input("Enter Exchange Condition (1 to 5 Stars): "))
        except ValueError:
            print("Invalid exchange condition. Please enter a valid number.")
            self.set_exchange_condition(input("Enter Exchange Condition (1 to 5 Stars): "))

    def display_exchange_info(self):
        print("\nExchange Information:")
        print("Book Title:", self.title)
        print("Author Name:", self.author_name)
        print("Edition:", self.edition)
        print("Image URL:", self.image_url)
        print("Published Date:", self.published_date)
        print("Exchange Condition:", self.exchange_condition, "stars")

def main(): #NEED functionality that asks user if they want to search for books or upload books
    # Accept user input for the book title 
    
    book_title = input("Enter a book title: ")

    # Ask the user if they want to sell or exchange the book
    action = input("Do you want to buy (B), sell (S), or exchange (E) the book? ").upper()

    if action == "S":
        # Create a BookSell object and collect additional information for selling
        book_sell = BookSell(book_title)
        list_price = input("Enter List Price: ")
        book_sell.set_list_price(list_price)
        condition = input("Enter Condition (1 to 5 Stars): ")
        book_sell.set_condition(condition)
        book_sell.display_sell_info()
    elif action == "E":
        # Create a BookExchange object and collect additional information for exchanging
        book_exchange = BookExchange(book_title)
        exchange_condition = input("Enter Exchange Condition (1 to 5 Stars): ")
        book_exchange.set_exchange_condition(exchange_condition)
        book_exchange.display_exchange_info()


        # Need to incorporate code that checks to see if the book is available for sale. If it is then we need to call the BookSell object that corresponds to it 
    #elif action == "B":   
        #book_exchange = BookExchange(book_title)
        #exchange_condition = input("Enter Exchange Condition (1 to 5 Stars): ")
        #book_exchange.set_exchange_condition(exchange_condition)
        #book_exchange.display_exchange_info()
    else:
        print("Invalid action. Please enter 'S' for sell or 'E' for exchange.")

if __name__ == '__main__':
    main()


