import hashlib
from ecommerce.db import get_db

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(username, password, db=None):
        if db is None:
            db = get_db()
        user = User(username, password)
        try:
            db.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                              (user.username, user.password_hash))
            db.connection.commit()
            return user
        except db.connection.IntegrityError:
            raise ValueError('User already exists')

    @staticmethod
    def login(username, password, db=None):
        if db is None:
            db = get_db()
        db.cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = db.cursor.fetchone()
        if row:
            stored_password_hash = row[0]
            if stored_password_hash == hashlib.sha256(password.encode()).hexdigest():
                return True
            else:
                raise ValueError('Invalid password')
        else:
            raise ValueError('User not found')

    @staticmethod
    def update_username(current_username, new_username, db=None):
        if db is None:
            db = get_db()
        try:
            db.cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, current_username))
            db.connection.commit()
        except db.connection.IntegrityError:
            raise ValueError('New username is already taken')

    @staticmethod
    def update_password(username, new_password, db=None):
        if db is None:
            db = get_db()
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        db.cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password_hash, username))
        db.connection.commit()

    @staticmethod
    def delete_account(username, db=None):
        if db is None:
            db = get_db()
        db.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        db.connection.commit()

    @staticmethod
    def get_user_id(username, db=None):
        if db is None:
            db = get_db()
        db.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError('User not found')