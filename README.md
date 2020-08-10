# FSND-Capstone
An API for managing actors and movies.\
Live Heroku App URL: https://capstone-nouf.herokuapp.com/
> Please note that currently the application does not have a front-end.

## Motivation
Capstone project submission for Udacity's Full-Stack Developer Nanodegree.

The purpose of the project is to strengthen and demonstrate all of the skills and knowledge acquired from the program, which are:
1. Data Modeling using SQLAlchemy.
2. Creating Flask Applications with Python
3. Setting up a Postgres DB.
4. Setting up third-party services.
5. Setting up Auth0 for authentication and authorization.
6. Validating JWT tokens and checking for permissions.
7. Defining roles and permissions.
8. Creating test cases using unittest module in Python.
9. 

## Dependencies
### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

### Style Guide
The code adheres to the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, use **pycodestyle** to verify:
`pycodestyle <name of file>`
> pycodestyle is a tool to check Python code against style conventions in PEP 8.

## Setup
> If you are on Windows OS then it is recommended to install [Git Bash](https://gitforwindows.org/) to run bash commands.
1. Install dependencies:\
`pip install -r requirements.txt`
2. Load environment variables:\
`source setup.sh`
3. Setup flask app:\
`export FLASK_APP=app`
4. Run the server:\
`flask run --reload`

## Testing
The **unittest** python module was used in creating the following test files:
1. test_app.py - Tests each endpoint for a **successful** behaviour and a **failure** behaviour.
2. test_rbac.py - Tests **two** RBAC **permissions** for each role.

> Before running any test files, the setup bash script must run to allow the current shell environment you are in to be aware of the environment variables.
It is required by the application and defined in **setup.sh**.\
`source setup.sh`

### Command Line
* Run **all tests** in a single test file: `python <name of file>`
* Run a **single test** from a test file: `python <name of file> CapstoneTestCase.<name of test>`

### Postman
For convenience a postman collection is provided, it includes requests for all endpoints and roles.
However, access tokens must be refreshed as they have an **expiration limit** of one day.

## API
### GET /movies
- Gets all movies from the DB.
- Returns a list of movies.
### GET /actors
- Gets all actors from the DB.
- Returns a list of actors.
### POST /movies
- Adds a movie to the DB.
- Returns
### PATCH /movies/<int:movie_id>
- Updates a movie's title in the DB.
- Returns
### DELETE /actors/<int:actor_id>
- Deletes an actor from the DB.
- Returns

## Authentication and RBAC
All endpoints require authentication and permissions which is handled by Auth0.
> Auth0 is a third-party service for quick and flexible authentication and authorization.

### Permissions
The project includes **four** permissions defined in **Auth0** as follows:
1. `('view:content')` - The ability to view actors and movies stored in the DB.
2. `('add:movie')` - The ability to add a movie to the DB.
3. `('modify:movie')` - The ability to update a movie's title in the DB.
4. `('delete:actor')` - The ability to delete an actor from the DB.

### Roles
The project includes **three** roles defined in **Auth0** with different permissions as follows:
1. Executive Producer - **All Permissions**
    - ('view:content')
    - ('add:movie')
    - ('modify:movie')
    - ('delete:actor')
2. Casting Director
    - ('view:content')
    - ('modify:movie')
    - ('delete:actor')
3. Casting Assistant
    - ('view:content')
