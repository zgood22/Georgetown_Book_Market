# this is the "web_app/__init__.py" file...

# this is the "web_app/__init__.py" file...

import os

from flask import Flask
from authlib.integrations.flask_client import OAuth

from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes
from web_app.routes.auth_routes import auth_routes

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret") # set this to something else on production!!!
#Google Log-in
CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID1'),
client_secret=os.getenv('GOOGLE_CLIENT_SECRET1'),

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    #Registering Oauth here
    oauth = OAuth(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
        client_id=CLIENT_ID,
        client_secret=client_secret,
        #authorize_params={"access_type": "offline"} # give us the refresh token! see: https://stackoverflow.com/questions/62293888/obtaining-and-storing-refresh-token-using-authlib-with-flask
    )
    app.config["OAUTH"] = oauth



    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(auth_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)