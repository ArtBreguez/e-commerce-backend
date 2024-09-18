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
