import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, drop_all_and_create_all

assistant_token = "Bearer {}".format(os.environ.get('CASTING_ASSISTANT'))
director_token = "Bearer {}".format(os.environ.get('CASTING_DIRECTOR'))
producer_token = "Bearer {}".format(os.environ.get('CASTING_PRODUCER'))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://postgres:root@localhost:5432/capstone"
        setup_db(self.app, self.database_path)
        # use the below lien to add Dummy data, otherwise comment it out
        # You might have to edit some route if you comment this out, according to your data
        drop_all_and_create_all()

        self.new_actor = {
            "name": "pickle Rick",
            "age": 19,
            "gender": "Male"
        }

        self.new_movie = {
            "title": "Nio and rocky",
            "release_year": 2090,
            "actor_id": 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self): 
        """Executed after reach test"""
        pass

    # Sucess
    def test_get_actor(self):
        res = self.client().get('/actors', headers={ "Authorization": ( assistant_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']) >= 0)

    # Failed
    def test_failed_get_actors (self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Success
    def test_get_movies (self):
        res = self.client().get('/movies', headers={ "Authorization": ( assistant_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) >= 0)

    # Failed
    def test_failed_get_movies (self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Sucess
    def test_post_actors (self):
        res = self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( director_token ) })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) == 1)

    # Failed
    def test_failed_create_actors (self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Sucess
    def test_create_movies (self):
        res = self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) == 1)

    # Failed
    def test_failed_create_movies (self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Sucess
    def test_update_actors (self):
        res = self.client().patch('/actors/1', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) == 1)

    # Failed
    def test_failed_update_actors (self):
        res = self.client().patch('/actors/2342', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # Sucess
    def test_update_movies (self):
        self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( director_token ) })
        res = self.client().patch('/movies/1', json=self.update_movie, headers={ "Authorization": ( director_token ) })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) == 1)

    # Failed
    def test_404_update_movies (self):
        res = self.client().patch('/movies/1000', json=self.update_movie, headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # Success for Delete Actors
    def test_delete_actors (self):
        res = self.client().delete('/actors/1', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], '2')
        self.assertTrue(data['success'])

    # failed for Delete Actor
    def test_404_delete_actors (self):
        res = self.client().delete('/actors/1000', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # Success for Delete Movies
    def test_delete_movies (self):
        self.client().post('/movies', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
        self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
        res = self.client().delete('/movies/1', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], '2')
        self.assertTrue(data['success'])

    # Failed for Delete Movies
    def test_404_delete_movies (self):
        res = self.client().delete('/movies/1000', headers={ "Authorization": ( producer_token ) })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()