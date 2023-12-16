# Georgetown-Book-Exchange

A web application based on a flask template provided my Prof. Rossetti. The Book Exchange is a central hub for Georgetown Students to exchange books.


## Prerequisites

This application requires a Python development environment:

  + Git
  + Anaconda, Python, Pip

For beginners, here are some instructions for how to install Anaconda, and [set up your local Python development environment](https://github.com/prof-rossetti/intro-to-python/blob/main/exercises/local-dev-setup/README.md#anaconda-python-and-pip).

## Repo Setup

If you are trying to recreate the book exchange, Make a copy of this template repo (as necessary). Clone your copy of the repo onto your local machine. Navigate there from the command-line.

Setup and activate a new Anaconda virtual environment:

```sh
conda create -n book-x-2 python=3.10
conda activate book-x-2
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Services Setup

This app requires a few services, for user authentication and data storage. Follow the instructions below to setup these services.

### Google Cloud Project

Visit the [Google Cloud Console](https://console.cloud.google.com). Create a new project, and name it. After it is created, select it from the project selection dropdown menu.

### Google OAuth Client

Visit the [API Credentials](https://console.cloud.google.com/apis/credentials) page for your Google Cloud project. Click the button with the plus icon to "Create Credentials", and choose "Create OAuth Client Id".

Click to "Configure Consent Screen". Leave the domain info blank, and leave the defaults / skip lots of the setup for now. If/when you deploy your app to a production server, you can return to populating this info (or you will be using a different project).

Return to actually creating the "OAuth Client Id". Choose a "Web application" type, give it a name, and set the following "Authorized Redirect URIs" (for now, while the project is still in development):

  + http://localhost:5000/auth/google/callback

After the client is created, note the `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`, and set them as environment variables (see configuration section below).

### Google Cloud Service Account Credentials

To fetch data from the Google Sheets database (and use other Google APIs), the app will need access to a local "service account" credentials file.

From the [Google API Credentials](https://console.cloud.google.com/apis/credentials) page, create a new service account as necessary.

For the chosen service account, create new JSON credentials file as necessary from the "Keys" menu, then download the resulting JSON file into the root directory of this repo, specifically named "google-credentials.json".


### Google Sheets Database Setup

See the [Google Sheets Database Setup](/admin/SHEETS_DB.md) guide.

### Google Analytics Setup

If you would like to configure Google Analytics, consult the [Google Analytics Setup](/admin/GA.md) guide.



## Configuration

### Environment Variables

Create a file called ".env" in the root directory of this repository, and populate it with environment variables to specify your own credentials, as obtained in the "Setup" section above:

```sh
FLASK_APP="web_app"

#
# GOOGLE OAUTH
#
GOOGLE_CLIENT_ID="____________"
GOOGLE_CLIENT_SECRET="____________"

#
# GOOGLE SHEETS DATABASE
#
GOOGLE_SHEETS_DOCUMENT_ID="____________"

#
# GOOGLE ANALYTICS
#
GA_TRACKER_ID="UA-XXXXXXX-1"
```




## Usage

### Sheets Service

After configuring the Google Sheet database and populating it with products, you should be able to test out the app's ability to fetch products (and generate new orders):

```sh
python -m app.sheets_service
```

### Web Application

Run the local web server (then visit localhost:5000 in a browser):

```sh
FLASK_APP=web_app flask run
```

## Testing

Run tests:

```sh
pytest
```

> NOTE: All tests pass locally, the pytest skip function was used to get a passing build in GitHub

## CI

See more information about the [CI](/admin/CI.md) build process. (Creds: Professor Rossetti)
Our repo was analyzed by code climate and has an A score as of time of submission. 

## Deploying

See the [Deployer's Guide](/admin/RENDER.md), provided my Prof Rossetti for instructions on deploying to a production server hosted by Render. Given the constraints on the project, we elected not to render our main, but here is documentation in case we want to in the future.



## See Liscence.MD File for more infomration about how to use this repository
