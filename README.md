# FSND-Capstone
An API for managing actors and movies.\
Live Heroku App URL: https://capstone-nouf.herokuapp.com/movies
> Please note that currently the application does not have a front-end.

## Motivation
Capstone project submission for Udacity's Full-Stack Developer Nanodegree.

The purpose of the project is to strengthen and demonstrate all of the skills and knowledge acquired from the program, which are:
1. Data modeling using SQLAlchemy.
2. Creating Flask applications with Python.
3. Setting up a Postgres DB.
4. Setting up third-party services.
5. Setting up Auth0 for authentication and authorization.
6. Validating JWT tokens and checking for permissions.
7. Defining roles and permissions.
8. Creating test cases using unittest module in Python.
9. Performing CRUD operations on a Postgres DB.
10. Document an API and its development details.
11. Deploying an application with Heroku.

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
### Local
1. Install dependencies:\
`pip install -r requirements.txt`
2. Update DATABASE_PATH variable in setup.sh:\
`postgresql://**USERNAME**:**PASSWORD**@localhost:5432/**DB_NAME**`
3. Populate DB with sample data:\
`psql <name of DB> < capstoneDB.psql`
4. Load environment variables:\
`source setup.sh`
5. Setup flask app:\
`export FLASK_APP=app`
6. Run the server:\
`flask run --reload`

### Live on Heroku
> You must have an account on [Heroku](www.heroku.com) and install Heroku CLI to be able to deploy the application.
1. Clone this repository:\
`git clone <GitHub repository URL>`
2. Login to Heroku:\
`heroku login`
3. Create an app on Heroku:\
`heroku create <name of the app>`
4. Add git remote for Heroku to local repository:\
`git remote add heroku <Heroku Git URL>`
5. Add postgresql heroku addon:\
`heroku addons:create heroku-postgresql:hobby-dev --app <Application Name>`
6. Configure variables in Heroku dashboard:
```
AUTH0_DOMAIN='fsnd-nouf.auth0.com'
ALGORITHMS='RS256'
AUDIENCE='capstone'
EXECUTIVE_PRODUCER_TOKEN=''
CASTING_DIRECTOR_TOKEN=''
CASTING_ASSISTANT_TOKEN=''
```
7. Push the repository to Heroku:\
`git push heroku master`

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
The postman collection allows for both **local** (Local folder) and **live testing** (Live Heroku App folder) of the application which is indicated by the folder name.

## API
### Movies
#### GET `/movies`
- Gets all movies from the DB.
- Returns a list of movies.
- Headers:
    - Authorization with 'view:content' permission.
- Request Arguments: None.
- Response Codes:
    - 200 OK - Successful.
    - 404 Not Found - Empty table.
```
{
    "movies": [
        {
            "id": 1,
            "releaseDate": "Fri, 20 Jul 2001 00:00:00 GMT",
            "title": "Spirited Away"
        },
        {
            "id": 2,
            "releaseDate": "Sat, 19 Jul 2008 00:00:00 GMT",
            "title": "Ponyo"
        },
        {
            "id": 3,
            "releaseDate": "Sat, 29 Jul 1989 00:00:00 GMT",
            "title": "Kikis Delivery Service"
        },
        {
            "id": 4,
            "releaseDate": "Fri, 20 Jul 2001 00:00:00 GMT",
            "title": "Only Yesterday"
        },
        {
            "id": 5,
            "releaseDate": "Sat, 16 Apr 1988 00:00:00 GMT",
            "title": "My Neighbor Totoro"
        }
    ],
    "success": true
}
```
#### POST `/movies`
- Adds a movie to the DB.
- Headers:
    - Authorization with 'add:movie' permission.
- Request Arguments:
    - title - Movie's title (String)
    - releaseDate - Movie's release date (Datetime object)
        - Format: YYYY-MM-DD HH:MM:SS
- Response Codes:
    - 200 OK - Successful.
    - 400 Bad Request - Missing body.
```
{
    "success": true
}
```
#### PATCH `/movies/<int:movie_id>`
- Updates a movie's title in the DB.
- Headers:
    - Authorization with 'modify:movie' permission.
- Request Arguments:
    - title - Movie's title (String)
- Response Codes:
    - 200 OK - Successful.
    - 400 Bad Request - Missing body.
    - 404 Not Found - Empty table.
```
{
    "success": true,
    "title": "Ponyo"
}
```
### Actors
#### GET `/actors`
- Gets all actors from the DB.
- Returns a list of actors.
- Headers:
    - Authorization with 'view:content' permission.
- Request Arguments: None.
- Response Codes:
    - 200 OK - Successful.
    - 404 Not Found - Empty table.
```
{
    "actors": [
        {
            "age": 0,
            "gender": "NA",
            "id": 1,
            "name": "No-Face"
        },
        {
            "age": 12,
            "gender": "Male",
            "id": 2,
            "name": "Haku"
        },
        {
            "age": 0,
            "gender": "Male",
            "id": 3,
            "name": "Totoro"
        },
        {
            "age": 13,
            "gender": "Female",
            "id": 4,
            "name": "Kiki"
        },
        {
            "age": 13,
            "gender": "Male",
            "id": 5,
            "name": "Jiji"
        }
    ],
    "success": true
}
```
#### DELETE `/actors/<int:actor_id>`
- Deletes an actor from the DB.
- Headers:
    - Authorization with 'delete:actor' permission.
- Request Arguments: None.
- Response Codes:
    - 200 OK - Successful.
    - 404 Not Found - An actor with the ID was not found in the DB.
```
{
    "actor_id": 1,
    "success": true
}
```

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
