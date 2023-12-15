

# tests for each page:

def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Books For Sale:" in response.data
    assert b"Account Page" in response.data

def test_about_page(test_client):
    response = test_client.get("/about")
    assert response.status_code == 200
    assert b"Welcome to Our About Page!" in response.data
    assert b"Thank you for choosing Georgetown Book Exchange." in response.data
    assert b"Georgetown Book Exchange is more than just a platform" in response.data
    assert b"About the Creators!" in response.data
    assert b"Samantha Miller is a senior at Georgetown University" in response.data
    assert b"Zachary Goodman is a senior at Georgetown University" in response.data


def test_products(test_client):
    response = test_client.get("/products")
    assert response.status_code == 200
    assert b"<h1>Products</h1>" in response.data


    assert b"Textbook" in response.data
    assert b"Cup of Tea" in response.data
    assert b"Strawberries" in response.data
