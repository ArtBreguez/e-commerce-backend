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
    def create_product(name, price, description, user_id, db=None, ascii_art=None, quantity=0):
        """
        Create a new product and save it in the database.
        
        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            description (str): The description of the product.
            user_id (int): The ID of the user creating the product.
            db (Database): The database connection (default: None).
            ascii_art (str): The ASCII art for the product image (default: None).
            quantity (int): The quantity available for the product (default: 0).
        
        Returns:
            None
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            INSERT INTO products (name, price, description, user_id, ascii_art, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, description, user_id, ascii_art, quantity))
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
            SELECT p.id, p.name, p.price, p.description, u.username, p.ascii_art, p.quantity, p.user_id
            FROM products p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        ''', (product_id,))
        return cursor.fetchone()

    @staticmethod
    def update_product(product_id, name=None, price=None, description=None, ascii_art=None, quantity=None, db=None):
        """
        Update an existing product in the database.
        
        Args:
            product_id (int): The ID of the product to update.
            name (str): The new name of the product (default: None).
            price (float): The new price of the product (default: None).
            description (str): The new description of the product (default: None).
            ascii_art (str): The updated ASCII art for the product image (default: None).
            quantity (int): The new quantity available for the product (default: None).
            db (Database): The database connection (default: None).
        
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
        if ascii_art:
            updates.append("ascii_art = ?")
            values.append(ascii_art)
        if quantity is not None:
            updates.append("quantity = ?")
            values.append(quantity)
        
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

    @staticmethod
    def get_products_by_user_id(user_id, db=None):
        """
        Retrieve all products created by the current user.

        Returns:
            list: A list of tuples containing product details.
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            SELECT *
            FROM products
            WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchall()
    
    @staticmethod
    def delete_products_by_user(user_id, db=None):
        """
        Delete all products created by the current user.

        Returns:
            None
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('DELETE FROM products WHERE user_id = ?', (user_id,))
        db.connection.commit()