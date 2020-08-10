import unittest
import datetime
import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import APP, format
from models import Movie, Actor, setup_db

# Executive producer token has all permissions.
token = os.environ['EXECUTIVE_PRODUCER_TOKEN']


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'bearer {token}'}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # testGetMoviesSuccess() tests for successful behaviour
    # by checking against the database.
    def testGetMoviesSuccess(self):
        # Ensures there is at least one movie in the database to get.
        movie = Movie('Spirited Away', datetime.datetime(2001, 7, 20))
        movie.add()

        movies = format(Movie.query.all())
        numOfMovies = len(movies)

        response = self.client().get('/movies',
                                     headers=self.headers)
        data = json.loads(response.data.decode())

        # Checks the ids in the response against the ids in the database.
        sameIds = all([data['movies'][i]['id'] ==
                       movies[i].id for i in range(0, numOfMovies)])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data['movies'], list))
        self.assertTrue(sameIds)
        self.assertEqual(len(data['movies']), numOfMovies)

    # testGetActorsFailure() tests for failed behaviour
    # by emptying the table.
    def testGetMoviesFailure(self):
        # Ensures that the movie table is empty.
        Movie.query.delete()

        response = self.client().get('/movies',
                                     headers=self.headers)

        self.assertEqual(response.status_code, 404)

    # testGetActorsSuccess() tests for successful behaviour
    # by checking against the database.
    def testGetActorsSuccess(self):
        # Ensures there is at least one actor in the database to get.
        actor = Actor('James', '21', 'Male')
        actor.add()

        actors = Actor.query.all()
        numOfActors = len(actors)

        response = self.client().get('/actors',
                                     headers=self.headers)
        data = json.loads(response.data.decode())

        # Checks the ids in the response against the ids in the database.
        sameIds = all([data['actors'][i]['id'] ==
                       actors[i].id for i in range(0, numOfActors)])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data['actors'], list))
        self.assertTrue(sameIds)
        self.assertEqual(len(data['actors']), numOfActors)

    # testGetActorsFailure() tests for failed behaviour
    # by emptying the table.
    def testGetActorsFailure(self):
        # Ensures that the actor table is empty.
        Actor.query.delete()

        response = self.client().get('/actors',
                                     headers=self.headers)

        self.assertEqual(response.status_code, 404)

    # testAddMovieSuccess() tests for successful behaviour
    # by checking against the database.
    def testAddMovieSuccess(self):
        numOfMoviesBefore = len(Movie.query.all())
        date = str(datetime.datetime(2001, 7, 20))

        response = self.client().post('/movies',
                                      json=dict(title='Spirited Away',
                                                releaseDate=date),
                                      headers=self.headers)
        data = json.loads(response.data.decode())

        numOfMoviesAfter = len(Movie.query.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(numOfMoviesBefore + 1, numOfMoviesAfter)

    # testAddMovieFailure() tests for failed behaviour
    # with an empty body.
    def testAddMovieFailure(self):
        response = self.client().post('/movies',
                                      headers=self.headers)

        self.assertEqual(response.status_code, 400)

    # testUpdateMovieSuccess() tests for successful behaviour
    # by checking against the database.
    def testUpdateMovieSuccess(self):
        # Ensures there is at least one movie in the database to update.
        movie = Movie('Spirited Away', datetime.datetime(2001, 7, 20))
        movie.add()

        movieId = len(Movie.query.all())

        response = self.client().patch('/movies/' + str(movieId),
                                       json=dict(title='Ponyo'),
                                       headers=self.headers)
        data = json.loads(response.data.decode())

        title = data['title']
        movie = Movie.query.get(movieId)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(title, movie.title)

    # testUpdateMovieFailure() tests for failed behaviour
    # with an empty body.
    def testUpdateMovieFailure(self):
        movieId = len(Movie.query.all())

        response = self.client().patch('/movies/' + str(movieId),
                                       headers=self.headers)

        self.assertEqual(response.status_code, 400)

    # testDeleteActorSuccess() tests for successful behaviour
    # by checking against the database.
    def testDeleteActorSuccess(self):
        # Ensures there is at least one actor in the database to delete.
        actor = Actor('JamesJ', '21', 'Male')
        actor.add()

        numOfActorsBefore = len(Actor.query.all())
        actorId = Actor.query.filter_by(name='JamesJ').first()

        response = self.client().delete('/actors/' + str(actorId.id),
                                        headers=self.headers)
        data = json.loads(response.data.decode())

        numOfActorsAfter = len(Actor.query.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(numOfActorsBefore - 1, numOfActorsAfter)

    # testDeleteActorFailure() tests for failed behaviour
    # with an invalid actor ID.
    def testDeleteActorFailure(self):
        actorId = str(len(Actor.query.all()) + 1)

        response = self.client().delete('/actors/' + actorId,
                                        headers=self.headers)

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
