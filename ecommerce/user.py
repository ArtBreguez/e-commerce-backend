import hashlib
from ecommerce.db import get_db

class User:
    """
    A class representing a User model. Provides methods to register, login,
    update, and delete user accounts in the database.

    Attributes:
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
    """

    def __init__(self, username, password):
        """
        Initialize a User instance with a username and a hashed password.

        Args:
            username (str): The username of the user.
            password (str): The raw password that will be hashed.
        """
        self.username = username
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        """
        Hash a password using SHA-256.

        Args:
            password (str): The raw password to hash.

        Returns:
            str: The hashed password as a hexadecimal string.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(username, password, db=None):
        """
        Register a new user by inserting their username and hashed password into the 'users' table.

        Args:
            username (str): The username for the new user.
            password (str): The raw password for the new user.
            db (Database, optional): The database connection object. If not provided, 
                                     a new connection will be created using `get_db()`.

        Returns:
            User: The newly registered user object.
        
        Raises:
            ValueError: If the user already exists in the database.
        """
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
        """
        Log in a user by checking if the provided password matches the stored hashed password.

        Args:
            username (str): The username of the user.
            password (str): The raw password to verify.
            db (Database, optional): The database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            bool: True if the login is successful.
        
        Raises:
            ValueError: If the user is not found or if the password is invalid.
        """
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
        """
        Update the username of an existing user.

        Args:
            current_username (str): The current username of the user.
            new_username (str): The new username to update.
            db (Database, optional): The database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            None
        
        Raises:
            ValueError: If the new username is already taken.
        """
        if db is None:
            db = get_db()
        try:
            db.cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, current_username))
            db.connection.commit()
        except db.connection.IntegrityError:
            raise ValueError('New username is already taken')

    @staticmethod
    def update_password(username, new_password, db=None):
        """
        Update the password of an existing user.

        Args:
            username (str): The username of the user.
            new_password (str): The new password to update.
            db (Database, optional): The database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            None
        """
        if db is None:
            db = get_db()
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        db.cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password_hash, username))
        db.connection.commit()

    @staticmethod
    def delete_account(username, db=None):
        """
        Delete a user account from the database.

        Args:
            username (str): The username of the user to delete.
            db (Database, optional): The database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            None
        """
        if db is None:
            db = get_db()
        db.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        db.connection.commit()

    @staticmethod
    def get_user_id(username, db=None):
        """
        Retrieve the ID of a user based on their username.

        Args:
            username (str): The username of the user.
            db (Database, optional): The database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            int: The ID of the user.
        
        Raises:
            ValueError: If the user is not found.
        """
        if db is None:
            db = get_db()
        db.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = db.cursor.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError('User not found')
