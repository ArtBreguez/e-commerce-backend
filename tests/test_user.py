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
        username = "testuser"
        password = "testpassword"
        User.register(username, password, self.db)
        self.db.cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        user_in_db = self.db.cursor.fetchone()
        self.assertIsNotNone(user_in_db)
        self.assertEqual(user_in_db[0], username)

    def test_user_login(self):
        username = "testuser"
        password = "testpassword"
        User.register(username, password, self.db)
        self.assertTrue(User.login(username, password, self.db))
        with self.assertRaises(ValueError):
            User.login(username, "wrongpassword", self.db)

    def test_update_username(self):
        username = "testuser"
        new_username = "newtestuser"
        password = "testpassword"
        User.register(username, password, self.db)
        User.update_username(username, new_username, self.db)
        self.db.cursor.execute("SELECT username FROM users WHERE username = ?", (new_username,))
        user_in_db = self.db.cursor.fetchone()
        self.assertEqual(user_in_db[0], new_username)

    def test_update_password(self):
        username = "testuser"
        password = "testpassword"
        new_password = "newtestpassword"
        User.register(username, password, self.db)
        User.update_password(username, new_password, self.db)
        self.assertTrue(User.login(username, new_password, self.db))

    def test_delete_account(self):
        username = "testuser"
        password = "testpassword"
        User.register(username, password, self.db)
        User.delete_account(username, self.db)
        self.db.cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        user_in_db = self.db.cursor.fetchone()
        self.assertIsNone(user_in_db)

if __name__ == '__main__':
    unittest.main()
