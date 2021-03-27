"""message model tests"""

import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test Models for User"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        uid1 = 1111
        u1.id = uid1
        
        u2 = User.signup("test2", "email2@email.com", "password", None)
        uid2 = 2222
        u2.id = uid2

        m1 = Message(text="text1", user_id=1111)
        mid1 = 111
        m1.id = mid1

        db.session.add(m1)
        db.session.commit()
        
        self.u1 = u1
        self.uid1 = uid1
        self.u2 = u2
        self.uid2 = uid2
        
        self.m1 = m1
        self.mid1 = mid1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """does the basic message model work?"""

        m = Message(
            text="test text",
            user_id=1111
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u1.messages), 2)
        self.assertEqual(str(m), f'<Message 1>')

    def test_user_message(self):
        """Does the message belong to the correct user?"""

        m = Message(
            text="test text",
            user_id=2222
        )

        db.session.add(m)
        db.session.commit()

        self.assertIn(self.m1, self.u1.messages)
        self.assertIn(m, self.u2.messages)
        self.assertNotIn(self.m1, self.u2.messages)
        self.assertNotIn(m, self.u1.messages)

        