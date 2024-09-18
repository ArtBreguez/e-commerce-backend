import unittest
import os
import sqlite3
from ecommerce.models import User
from ecommerce.db import get_db, create_tables

class TestUserModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists("test_ecommerce.db"):
            os.remove("test_ecommerce.db")

    def setUp(self):
        self.db = get_db("test_ecommerce.db")  
        create_tables(self.db.connection)

    def tearDown(self):
        self.db.close()
        if os.path.exists("test_ecommerce.db"):
            os.remove("test_ecommerce.db")

    def test_user_registration(self):
        db = get_db("test_ecommerce.db")  
        username = "testuser"
        password = "testpassword"
        User.register(username, password, db)
        
        db.cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        user_in_db = db.cursor.fetchone()
        self.assertIsNotNone(user_in_db)
        self.assertEqual(user_in_db[0], username)
    
    def test_user_login(self):
        db = get_db("test_ecommerce.db")  
        username = "testuser"
        password = "testpassword"
        User.register(username, password, db)

        self.assertTrue(User.login(username, password, db))

        with self.assertRaises(ValueError):
            User.login(username, "wrongpassword", db)

        with self.assertRaises(ValueError):
            User.login("nonexistentuser", "password", db)

if __name__ == '__main__':
    unittest.main()
