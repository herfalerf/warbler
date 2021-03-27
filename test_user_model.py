"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test Models for User"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        uid1 = 1111
        u1.id = uid1
        
        u2 = User.signup("test2", "email2@email.com", "password", None)

        self.u1 = u1
        self.uid1 = uid1
        self.u2 = u2

        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(str(u), f'<User #{u.id}: {u.username}, {u.email}>')

    def test_is_following(self):
        """Tests if a user is following another user"""
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))
    
    def test_is_followed_by(self):
        """Tests if a user is followed by another user"""
        self.u2.following.append(self.u1)
        db.session.commit()

        self.assertTrue(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))
    
    def test_user_create(self):
        """Does User.signup successfully create a ne wuser given valid credentials?"""
        

        self.assertIsInstance(self.u1, User)
        self.assertRaises(TypeError, lambda: User.signup("test3", "test3@email.com"))

    def test_user_authenticate(self):
        """Does User.authenticate return a user when given a valid username and password, does it fail with wrong username/password?"""

        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)

        self.assertFalse(User.authenticate("failusername", "password")) 
        self.assertFalse(User.authenticate(self.u1.username, "failpassword")) 
