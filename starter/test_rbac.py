import unittest
import datetime
import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import APP, format
from models import Movie, Actor, setup_db

EPToken = os.environ['EXECUTIVE_PRODUCER_TOKEN']
CDToken = os.environ['CASTING_DIRECTOR_TOKEN']
CAToken = os.environ['CASTING_ASSISTANT_TOKEN']

EPAuth = {'Authorization': f'bearer {EPToken}'}
CDAuth = {'Authorization': f'bearer {CDToken}'}
CAAuth = {'Authorization': f'bearer {CAToken}'}


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Tests that demonstrate role-based access control.

    def testCastingAssistantGetMovies(self):
        movie = Movie('Spirited Away', datetime.datetime(2001, 7, 20))
        movie.add()

        response = self.client().get('/movies',
                                     headers=CAAuth)
        self.assertEqual(response.status_code, 200)

    def testCastingAssistantGetActors(self):
        actor = Actor('James', '21', 'Male')
        actor.add()

        response = self.client().get('/actors',
                                     headers=CAAuth)
        self.assertEqual(response.status_code, 200)

    def testCastingDirectorUpdateMovie(self):
        movie = Movie('Spirited Away', datetime.datetime(2001, 7, 20))
        movie.add()

        movieId = len(Movie.query.all())

        response = self.client().patch('/movies/' + str(movieId),
                                       json=dict(title='Ponyo'),
                                       headers=CDAuth)
        self.assertEqual(response.status_code, 200)

    def testCastingDirectorDeleteActor(self):
        actor = Actor('JamesJ', '21', 'Male')
        actor.add()

        actorId = Actor.query.filter_by(name='JamesJ').first()

        response = self.client().delete('/actors/' + str(actorId.id),
                                        headers=CDAuth)
        self.assertEqual(response.status_code, 200)

    def testExecutiveProducerUpdateMovie(self):
        movie = Movie('Spirited Away', datetime.datetime(2001, 7, 20))
        movie.add()

        movieId = len(Movie.query.all())

        response = self.client().patch('/movies/' + str(movieId),
                                       json=dict(title='Ponyo'),
                                       headers=EPAuth)
        self.assertEqual(response.status_code, 200)

    def testExecutiveProducerAddMovie(self):
        date = str(datetime.datetime(2001, 7, 20))

        response = self.client().post('/movies',
                                      json=dict(title='Spirited Away',
                                                releaseDate=date),
                                      headers=EPAuth)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
