import sqlite3

def get_db(db_name="ecommerce.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    create_tables(connection)
    return Database(connection, cursor)

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password_hash TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                price REAL,
                                description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS carts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                product_id INTEGER,
                                quantity INTEGER,
                                FOREIGN KEY(user_id) REFERENCES users(id),
                                FOREIGN KEY(product_id) REFERENCES products(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                order_details TEXT,
                                total REAL,
                                FOREIGN KEY(user_id) REFERENCES users(id))''')
    connection.commit()

class Database:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def close(self):
        self.connection.close()
