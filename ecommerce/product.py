from ecommerce.db import get_db

class Product:
    """
    A class representing the Product model. Provides methods to create, retrieve, update,
    and delete products in the database.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        description (str): A brief description of the product.
        user_id (int): The ID of the user who created the product.
        db (Database): The database connection object (optional).
    """
    def __init__(self, name, price, description, user_id, db=None):
        """
        Initialize a Product instance.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            description (str): A brief description of the product.
            user_id (int): The ID of the user creating the product.
            db (Database, optional): A database connection object. If not provided, 
                                     a new connection will be created using `get_db()`.
        """
        self.name = name
        self.price = price
        self.description = description
        self.user_id = user_id
        self.db = db or get_db()

    @staticmethod
    def create_product(name, price, description, user_id, db=None):
        """
        Create a new product and insert it into the 'products' table.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            description (str): A brief description of the product.
            user_id (int): The ID of the user creating the product.
            db (Database, optional): A database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            None
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            INSERT INTO products (name, price, description, user_id)
            VALUES (?, ?, ?, ?)
        ''', (name, price, description, user_id))
        db.connection.commit()

    @staticmethod
    def get_all_products(db=None):
        """
        Retrieve all products from the 'products' table.

        Args:
            db (Database, optional): A database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            list: A list of all products as tuples containing product details.
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            SELECT *
            FROM products
        ''')
        
        return cursor.fetchall()

    @staticmethod
    def get_product_by_id(product_id, db=None):
        """
        Retrieve a product by its ID, including the username of the product creator.

        Args:
            product_id (int): The ID of the product to retrieve.
            db (Database, optional): A database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            tuple: A tuple containing product details and the creator's username, 
                   or None if the product does not exist.
        """
        db = db or get_db()
        cursor = db.cursor
        
        cursor.execute('''
            SELECT p.id, p.name, p.price, p.description, u.username, p.user_id
            FROM products p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        ''', (product_id,))
        return cursor.fetchone()

    @staticmethod
    def update_product(product_id, name=None, price=None, description=None, db=None):
        """
        Update product details for a given product ID.

        Args:
            product_id (int): The ID of the product to update.
            name (str, optional): The new name of the product.
            price (float, optional): The new price of the product.
            description (str, optional): The new description of the product.
            db (Database, optional): A database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            None
        """
        db = db or get_db()
        cursor = db.cursor
        updates = []
        values = []
        
        if name:
            updates.append("name = ?")
            values.append(name)
        if price:
            updates.append("price = ?")
            values.append(price)
        if description:
            updates.append("description = ?")
            values.append(description)
        
        if updates:
            query = f'UPDATE products SET {", ".join(updates)} WHERE id = ?'
            values.append(product_id)
            cursor.execute(query, values)
            db.connection.commit()

    @staticmethod
    def delete_product(product_id, db=None):
        """
        Delete a product from the database by its ID.

        Args:
            product_id (int): The ID of the product to delete.
            db (Database, optional): A database connection object. If not provided,
                                     a new connection will be created using `get_db()`.

        Returns:
            None
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.connection.commit()
