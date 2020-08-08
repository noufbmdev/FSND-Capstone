from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, setup_db
from auth import requires_auth, AuthError
import os

database_path = 'postgresql://Nouf:nono2314@localhost:5432/capstone'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, database_path)
    CORS(app)
    return app


APP = create_app()


def format(list):
    return [item.format() for item in list]


def get(table):
    data = table.query.all()

    if len(data) == 0:
        abort(404)

    return data


@APP.route('/movies')
@requires_auth('view:content')
def getMovies(token):

    movies = get(Movie)

    return jsonify({
        'success': True,
        'movies': format(movies)
    })


@APP.route('/actors')
@requires_auth('view:content')
def getActors(token):

    actors = get(Actor)

    return jsonify({
        'success': True,
        'actors': format(actors)
    })


@APP.route('/movies', methods=['POST'])
@requires_auth('add:movie')
def postMovie(token):

    body = request.get_json()
    if body is None:
        abort(400)

    title = body.get('title')
    releaseDate = body.get('releaseDate')

    movie = Movie(title, releaseDate)
    movie.add()

    return jsonify({
        'success': True
    })


@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('modify:movie')
def patchMovie(token, movie_id):

    body = request.get_json()
    if body is None:
        abort(400)

    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)

    title = body.get('title')
    movie.title = title
    movie.update()

    return jsonify({
        'success': True,
        'title': title
    })


@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def deleteActor(token, actor_id):

    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)

    actor.delete()

    return jsonify({
        'success': True,
        'actor_id': actor_id
    })


@APP.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request.'
    }), 400


@APP.errorhandler(401)
def unauthorized_error(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized.'
    }), 401


@APP.errorhandler(404)
def not_found_error(error):
    return jsonify({
         'success': False,
         'error': 404,
         'message': 'Resource not found.'
    }), 404


@APP.errorhandler(422)
def unprocessable_error(error):
    return jsonify({
         'success': False,
         'error': 422,
         'message': 'Unprocessable entity.'
    }), 422


@APP.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
         'success': False,
         'error': error.status_code,
         'message': error.error
    }), error.status_code


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
