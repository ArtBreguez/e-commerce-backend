import sqlite3

def get_db(db_name="ecommerce.db"):
    """
    Connect to the SQLite database and create necessary tables if they don't exist.

    Args:
        db_name (str): The name of the SQLite database file. Defaults to 'ecommerce.db'.
    
    Returns:
        Database: A custom `Database` object that wraps the SQLite connection and cursor.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    create_tables(connection)
    return Database(connection, cursor)

def create_tables(connection):
    """
    Create necessary tables for the application: 'users', 'products', 'carts', and 'orders'.

    Args:
        connection (sqlite3.Connection): The SQLite connection object to the database.
    
    Returns:
        None
    """
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password_hash TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        price REAL,
                        description TEXT,
                        user_id INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    
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
    """
    A wrapper class for managing the SQLite database connection and cursor.

    Attributes:
        connection (sqlite3.Connection): The SQLite database connection.
        cursor (sqlite3.Cursor): The cursor for executing queries on the SQLite database.
    """
    def __init__(self, connection, cursor):
        """
        Initialize the Database object with a connection and cursor.

        Args:
            connection (sqlite3.Connection): The SQLite database connection.
            cursor (sqlite3.Cursor): The cursor for executing queries.
        """
        self.connection = connection
        self.cursor = cursor

    def close(self):
        """
        Close the SQLite database connection.

        Returns:
            None
        """
        self.connection.close()
