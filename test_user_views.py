"""USER View tests."""

import os
from unittest import TestCase

from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser1 = User.signup(username="testuser1",
                                    email="test1@test.com",
                                    password="password",
                                    image_url=None)
        self.testuser1_id = 1000
        self.testuser1.id = self.testuser1_id

        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="password",
                                    image_url=None)
        self.testuser2_id = 2000
        self.testuser2.id = self.testuser2_id

        self.testuser3 = User.signup(username="testuser3",
                                    email="test3@test.com",
                                    password="password",
                                    image_url=None)
        self.testuser3_id = 3000
        self.testuser3.id = self.testuser3_id

        self.testuser4 = User.signup(username="testuser4",
                                    email="test4@test.com",
                                    password="password",
                                    image_url=None)
        self.testuser4_id = 4000
        self.testuser4.id = self.testuser4_id

        self.testuser1.following.append(self.testuser3)
        self.testuser2.following.append(self.testuser1)
        self.testuser3.following.append(self.testuser4)



        db.session.commit()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_follower_pages_loggedin(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id
            

            resp1 = c.get("/users/3000/followers", follow_redirects=True)
            self.assertEqual(resp1.status_code, 200)
            self.assertIn("@testuser1", str(resp1.data))
            
            resp2 = c.get("/users/4000/followers", follow_redirects=True)
            self.assertEqual(resp2.status_code, 200)
            self.assertIn("@testuser3", str(resp2.data))

            resp3 = c.get("/users/1000/following", follow_redirects=True)
            self.assertEqual(resp3.status_code, 200)
            self.assertIn("@testuser3", str(resp3.data))

    def test_follower_pages_loggedout(self):
        with self.client as c:     
            resp = c.get("/users/1000/followers", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", str(resp.data))
    
    def test_following_pages_loggedout(self):
        with self.client as c:     
            resp = c.get("/users/1000/following", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", str(resp.data))

    
    

