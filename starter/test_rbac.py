import unittest
import datetime
import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import APP, format
from models import Movie, Actor, setup_db

token = os.environ.get('token')


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        self.database_path = 'postgresql://Nouf:nono2314@localhost:5432/capstone'
        setup_db(self.app, self.database_path)
        self.headers = {'Content-Type': 'application/json'}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Tests that demonstrate role-based access control.

    def testCastingAssistantGetMovies(self):
        response = self.client().get('/movies',
                                     token=token)
        self.assertEqual(response.status_code, 200)

    def testCastingAssistantGetActors(self):
        response = self.client().get('/actors',
                                     token=token)
        self.assertEqual(response.status_code, 200)

    def testCastingDirectorUpdateMovie(self):
        movieId = len(Movie.query.all())

        response = self.client().patch('/movies/' + str(movieId),
                                       data=json.dumps(dict(title='Ponyo')),
                                       headers=self.headers,
                                       token=token)
        self.assertEqual(response.status_code, 200)

    def testCastingDirectorDeleteActor(self):
        actor = Actor('JamesJ', '21', 'Male')
        actor.add()

        actorId = Actor.query.filter_by(name='JamesJ').first()

        response = self.client().delete('/actors/' + str(actorId.id),
                                        token=token)
        self.assertEqual(response.status_code, 200)

    def testExecutiveProducerUpdateMovie(self):
        movieId = len(Movie.query.all())

        response = self.client().patch('/movies/' + str(movieId),
                                       data=json.dumps(dict(title='Ponyo')),
                                       headers=self.headers,
                                       token=token)
        self.assertEqual(response.status_code, 200)

    def testExecutiveProducerAddMovie(self):
        date = str(datetime.datetime(2001, 7, 20))

        response = self.client().post('/movies',
                                      data=json.dumps(
                                           dict(title='Spirited Away',
                                                releaseDate=date)),
                                      headers=self.headers,
                                      token=token)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
