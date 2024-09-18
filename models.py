import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="ecommerce.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                password_hash TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                price REAL,
                                description TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS carts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                product_id INTEGER,
                                quantity INTEGER,
                                FOREIGN KEY(user_id) REFERENCES users(id),
                                FOREIGN KEY(product_id) REFERENCES products(id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                order_details TEXT,
                                total REAL,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')
        self.connection.commit()

    def close(self):
        self.connection.close()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(db, username, password):
        user = User(username, password)
        try:
            db.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                              (user.username, user.password_hash))
            db.connection.commit()
            return user
        except sqlite3.IntegrityError:
            raise ValueError('User already exists')

    @staticmethod
    def login(db, username, password):
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
