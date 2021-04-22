from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
from models import setup_db,drop_all_and_create_all, Actor, Movie
import sys
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  Set up CORS.
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  Using the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


  @app.route('/')
  def index():
    return jsonify({
    'message': 'Welcome to the casting agency'
    })
  #  Creating Dummy data for Testing
  # If you are going to test the application, please run this API
  # it will drop all table
  # then create all table
  # and will add dummy data to it
  @app.route('/dummy')
  def create_dummy_data():
    drop_all_and_create_all()
    return jsonify({
      'success': True,
    })

  #  GET Actors
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(jwt):
    try:
      return jsonify({
        'success': True,
        'actors': [actor.format() for actor in Actor.query.all()]
      })
    except Exception as e:
      print ('Exception', e)
      abort(400)

  #  GET Movies
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(jwt):
    try:
      return jsonify({
        'success': True,
        'movies': [movie.format() for movie in Movie.query.all()]
      })
    except Exception as e:
      print ('Exception', e)
      abort(400, e)

  #  POST Actors
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(jwt):
    try:
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      # Abort 400 if any fields are missing
      if not ('name' in body and 'age' in body and 'gender' in body):
          abort(400, 'name, age and gender are required fields.')

      # Create and insert a new actor
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()

      # Return Success with newly created actor
      return jsonify({
        'success': True,
        'actor': [Actor.query.get(actor.id).format()]
      })
    except Exception as e:
      print ('Exception', e)
      abort(400, e)
  #  POST Movies
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(jwt):
    try:
      body = request.get_json()
      title = body.get('title', None)
      release_year = body.get('release_year', None)
      actor_id = body.get('actor_id', None)

      # Abort 400 if any fields are missing
      if not ('title' in body and 'release_year' in body and 'actor_id' in body):
          abort(400, 'title, release year and actor ID are required fields')

      # Create and insert a new movie
      movie = Movie(title=title, release_year=release_year, actor_id=actor_id)
      movie.insert()

      # Return the newly created movie
      return jsonify({
        'success': True,
        'movies': [Movie.query.get(movie.id).format()]
      })
    except Exception as e:
      abort(400, e)

  #  PATCH Actors
  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor_details(jwt, actor_id):
    try:
      actor = Actor.query.get(actor_id)

      # If Actor not Found
      if actor is None:
        abort(404)

      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      # Update the actor with the requested fields
      if ((name != None) and (name != '')):
          actor.name = name

      if ((age != None) and (age != '')):
          actor.age = age

      if ((gender != None) and (gender != '')):
          actor.gender = gender
      actor.update()

      # Return the updated actor
      return jsonify({
        'success': True,
        'actors': [Actor.query.get(actor_id).format()]
      })
    except Exception as e:
      print ('Exception', e)
      abort(400, e)

  #  PATCH Movies
  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, movie_id):
    try:
      movie = Movie.query.get(movie_id)

      # Abort not Found
      if movie is None:
        abort(404)

      body = request.get_json()
      title = body.get('title', None)
      release_year = body.get('release_year', None)
      actor_id = body.get('actor_id', None)


      # Update Entry
      if ((title != None) and (title != '')):
          movie.title = title
      if ((release_year != None) and (release_year != '')):
          movie.release_year = release_year
      if ((actor_id != None) and (actor_id != '')):
          actor_id = actor_id
      movie.update()

      # Return the updated movie
      return jsonify({
        'success': True,
        'movies': [Movie.query.get(movie_id).format()]
      })
    except Exception as e:
      print ('Exception', e)
      abort(400, e)

  #  DELETE Actors
  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    try:
      actor = Actor.query.get(actor_id)

      # If actor not found
      if actor is None:
        abort(404)

      # Delete the actor
      actor.delete()

      return jsonify({
        'success': True,
        'delete': actor_id
      })
    except Exception as e:
      print ('Exception', e)
      abort(400, e)

  #  DELETE Movies
  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    try:
      movie = Movie.query.get(movie_id)
      # Abort 404 if the movie was not found
      if movie is None:
        abort(404)

      # Delete the movie
      movie.delete()

      return jsonify({
        'success': True,
        'delete': movie_id
      })
    except Exception as e:
      print ('Exception', e)
      abort(400, e)

  #----------------------------------------------------------------------------#
  # Error Handling.
  #----------------------------------------------------------------------------#
  # Unprocessable Entity
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unable to process your request. Please try again later."
    }), 422

  # Not Found
  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource not found."
    }), 404

  # Bad Request
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": str(error)
    }), 400

  # AuthError exceptions raised by the @requires_auth(permission) decorator method
  @app.errorhandler(AuthError)
  def auth_error(auth_error):
    return jsonify({
      "success": False,
      "error": auth_error.status_code,
      "message": auth_error.error['description']
    }), auth_error.status_code

  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)