## Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Deployment
This app is hosted on heroku. The link to the app is here, [here, click me!](https://casting-agency-deploy.herokuapp.com/).. The backend is up and running. The frontend is still under construction.

Refer to the credentials given below to login in order to access the JWT for each role mentioned below. Ensure that your browser history is cleared at least for the last 1 hour before login into each account.

## Authentication
The app uses Auth0 as a third party authentication service.

Three roles have been created to manage the system. Each role is restricted to perform certain CRUD operations on the system as assigned and permitted by Auth0 service.

## Installation and Database Setup
Clone the repo by running 

```bash
git clone https://github.com/abkumarofficial/Casting-Agency.git
```
### Dependencies

Install Python 3.8 or Above

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the ptoject directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

Recommmended is you create a python virtual environment ( virtualenv ) to install all these packages.

### Database Setup
- Create two databases for **testing** and **development**
- Generate database tables from the migration files included by executing: 
  `python manage.py db upgrade`
- Add dummy data by executing:
  `python manage.py seed`
  
## Running the Server Locally
From within the project directory first ensure you are working using your created virtual environment.

- To run the **development** server, execute:
`bash setup.sh` 
but before running , uncomment the following lines
export FLASK_APP=app.py
export FLASK_DEBUG=true
export FLASK_ENV=development
flask run --reload

## Testing
There is a Postman Json File , just import that in Postman and run the test
OR
You can run the testing script written in python , i.e test_app.py

Note: In Both the ways, I am calling a function in the starting which is going to create dummy data.

## Endpoints
```
GET '/dummy'
- Creates Dummy data for you to work on
- Response
{
  "success": True
}

GET '/actors'
- Fetches all actors on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:actors)
- Response
{
  "actors": [
    {
        "age": 22,
        "gender": "Male",
        "id": 3,
        "name": "Vivek"
    },
    {
        "age": 50,
        "gender": "Male",
        "id": 4,
        "name": "Pranshant"
    },
  ],
  "success": true
}

GET '/movies'
- Fetches all movies on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:movies)
- Response
{
  "movies": [
    {
      "id": 3,
      "release_date": "Thu, 23 Jun 2005 00:00:00 GMT",
      "title": "A fall from Grace"
    },
    {
      "id": 1,
      "release_date": "Thu, 28 Jun 2000 00:00:00 GMT",
      "title": "Jumanji"
    }
  ],
  "success": True
}

POST '/actors'
- Creates a new actor with the provided parameters
- Request Arguments: None
- Allowed users: Executive Producer and casting Director
- Required permission ('post:actors')
- Request Body: {
    "name": "Rick Astley",
    "age": 22,
    "gender": "Male"
}

- Response
{
    "success": True
    "actor": [
        {
            "name": "Rick Astley",
            "age": 22,
            "gender": "Male"
        }
    ]
}

POST '/movies'
- Creates a new movie with the provided parameters
- Request Arguments: None
- Allowed users: Executive Producer
- Required permission (post:movies)
- Request Body: {
    "title": "Sherlock Homes 4",
    "release_year": 2090,
    "actor_id": 1
}

- Response
{
  "movie":
      [
        {
            "title": "Sherlock Homes 4",
            "release_year": 2090,
            "actor_id": 1
        }
    ]
  "success": true
}

PATCH '/actors/<id>'
- Updates a specific actor with the provided parameters
- Request Arguments: actor_id (The ID of the actor to update)
- Allowed users: Executive Producer and Casting Director
- Required permission ('patch:actors')
- Request Body: {
    "age": 99
}

- Response
{
  "actor": {
    "age": 44,
    "gender": "Male",
    "id": 23,
    "name": "Raman"
  },
  "success": true
}

PATCH '/movies/<id>'
- Updates a specific movie with the provided parameters
- Request Arguments: movie_id (The ID of the movie to update)
- Allowed users: Executive Producer, Casting Director
- Required permission (patch:movies)
- Request Body: {
    "title": "Never Gonna Give you up",
    "release_year": 1995
}

- Response
{
  "movie": {
    "id": 43,
    "release_year": 2020,
    "title": "Never Gonna Give you up",
    "actor_id": 23
  },
  "success": true
}

DELETE '/movies/<id>'
- Deletes a specific movie
- Request Arguments: movie_id (The ID of the movie to delete)
- Allowed users: Executive Producer
- Required permission (delete:movie)
- Response
{
  "delete": id,
  "success": true
}

DELETE '/actors/<id>'
- Deletes a specific actor
- Request Arguments: actor_id (The ID of the actor to delete)
- Required permission (delete:actors)
- Response
{
  "delete": id,
  "success": true
}

Errors

400 (Bad Request)
  {
    "success": False, 
    "error": 400,
    "message": "bad request, please check your input"
  }

401 (Unauthorised)
  {
    "success": False, 
    "error": 401,
    "message": "authorisation error"
  }

403 (Forbiddden request)
  {
    "success": False, 
    "error": 403,
    "message": "You are not allowed to access this resource"
  }

404 (Resource Not Found)
  {
    "success": False, 
    "error": 404,
    "message": "resource not found"
  }

405 (Method not allowed)
  {
    "success": False, 
    "error": 405,
    "message": "Method not allowed"
  }

422 (Unprocessable entity)
  {
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }
```