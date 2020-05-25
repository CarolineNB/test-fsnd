import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtnekozVTAyaGFvWkwwajJDMmdEVSJ9.eyJpc3MiOiJodHRwczovL2NiLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYmM3MTkyZGNlODBjNmYxODBmZDIiLCJhdWQiOiJDYXN0cyIsImlhdCI6MTU5MDQyMzQzNCwiZXhwIjoxNTkwNTA5ODM0LCJhenAiOiJ6SnV0WDJNbEVyalRUTEpPT0FCT0dnekdyWTFiTkVnTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.w8nsBM5QpU0hmHSyp8U0eXol-GAJXCYOqIpAgYetBmAIYuHM0SaSLbIDbVQGQXgWKZbgl3920MqK6oSE9POKmAcyW64_Z01idH3LCjiNLGZJly2agX4kbB7C0Ozx5ZH5xJFZvV4uYEvus_ok3zDaCtkdU7gdAYoaaP6MQZs1i6QL65q8Xe9UBaIaTlb4u6Qopzvo-pIyDdY31fLIo2EohFJI_duGjsti5Hb2djp56JfGAvFKOpxOKA29iluVRnpNujOv7_-xiwBc6zsncREjL9W3xzGo1SLqiwRi1wf6TrxG01zXGtKj5ebO_Rj9wQ9YKx_oiOLNF21DfbPMmnoh5Q"
        self.director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtnekozVTAyaGFvWkwwajJDMmdEVSJ9.eyJpc3MiOiJodHRwczovL2NiLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYmQwMWVlNTZjNDBjNmQ4NTRmZDYiLCJhdWQiOiJDYXN0cyIsImlhdCI6MTU5MDQyMzQ3NCwiZXhwIjoxNTkwNTA5ODc0LCJhenAiOiJ6SnV0WDJNbEVyalRUTEpPT0FCT0dnekdyWTFiTkVnTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicG9zdDphY3RvcnMiXX0.qsfhLBzbqmFSQwdaDQuZ5Qh2RidRZKrEISH6jl5oU8BweSsA7X33nl7jFbNurgjkUIKmTXPCvxDu8X2OfofPjQ5ZjXPo5odwhLS8BojIc-X86P7HeV6EmLQI3R0T6lgrG2ZP1k9ooqqWOA5MHA6vnUlcyt0WKlWPiT65Xly32gw5U3ObcADFJxkHF_LHAcxlxdTZJ11mHsGYExcJ293m7YWkprrJrw2dGWbCzKDRCU595uvpHjtmuPdCyZMZnCW5O-KrlyS8Jgnwq7QEbqLFIAWB-Y3AIPMFdotvDYmhIrtY4R1tlSfei7Y8XN-tG42P_mz2AfI5GSQAOCr0H_BygA"
        self.producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtnekozVTAyaGFvWkwwajJDMmdEVSJ9.eyJpc3MiOiJodHRwczovL2NiLWNhcHN0b25lLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWNhYmQyMTkyZGNlODBjNmYxODE0M2UiLCJhdWQiOiJDYXN0cyIsImlhdCI6MTU5MDQyMzUyNiwiZXhwIjoxNTkwNTA5OTI2LCJhenAiOiJ6SnV0WDJNbEVyalRUTEpPT0FCT0dnekdyWTFiTkVnTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.Jap4hi6zfWeYZBKmSjZ6C2LTjsyS-3PGrVmlOyRYouqgwMFlzRybhmTu8bOz5KEguOL3tJIBzNcrRNjdKgAOmaydjaZFaHXkpt_hqaxHSy8rgEXn12W_W2A6vNto8jDlNw1lK2k8mI2UZxnEpa0qTVfwLbaHMNTwvoXXk6J3KZfsr5ylvxVbqfm7Sn4Bot_Ggt94EQ4y9e7gGzts0SGXrE6fc9sqqQ2BqlOwHClOjdYvovL7MPVIZIee6UbJ_zz7bFWgHP9JdbDv0hT0Zv_HMRyTg7qAkQmBGOqBz_ODBa7ZFMu1CpTLj9sbqcDfN4OFr1m2ES8QiFy1m8Xjo7mcbQ"
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres: @localhost:5432/{}"\
            .format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                         'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total actors'], len(Actor.query.all()))

    def test_get_actors_invalid_permission(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                         'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total movies'], len(Movie.query.all()))

    def test_get_movies_invalid_permission(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_director(self):
        res = self.client().delete('/actors/2',
                                   headers={'Authorization':
                                            'Bearer '+self.director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_producer(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization':
                                            'Bearer '+self.producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_error_assistant(self):
        res = self.client().delete('/actors/4',
                                   headers={'Authorization':
                                            'Bearer '+self.assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_invalid(self):
        res = self.client().delete('/actors/999',
                                   headers={'Authorization':
                                            'Bearer '+self.director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_actor_producers(self):
        actor = {
            'name': 'name2',
            'gender': 'gender2',
            'age': 22
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_director(self):
        actor = {
            'name': 'name',
            'gender': 'gender',
            'age': 20
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.director)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_producer(self):
        actor = {
            'name': 'name2',
            'gender': 'gender2',
            'age': 22
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_producers(self):
        actor = {
            'name': 'changename',
            'gender': 'gender2',
            'age': 223
        }
        res = self.client().patch('/actors/5',
                                  headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                  }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_director(self):
        actor = {
            'name': 'changeNameAgain',
            'gender': 'gender2',
            'age': 223
        }
        res = self.client().patch('/actors/6',
                                  headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.director)
                                  }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_assistant_error(self):
        actor = {
            'name': 'changeNameAgain',
            'gender': 'gender2',
            'age': 223
        }
        res = self.client().patch('/actors/3',
                                  headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.assistant)
                                  }, json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        movie = {
            'name': 'this is a name',
            'date': 100799
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_director_error(self):
        movie = {
            'name': 'this is a name',
            'date': 100799
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.director)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie_invalid(self):
        movie = {
            'name': 333,
            'date': 100799
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization":
                                     "Bearer {}".format(
                                         self.producer)
                                 }, json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
