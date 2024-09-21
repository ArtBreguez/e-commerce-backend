from ecommerce.db import get_db

class Order:
    def __init__(self, user_id, db=None):
        """
        Initialize the order with a user ID and optional database connection.

        Args:
            user_id (int): The ID of the user associated with the order.
            db (Database): Optional database connection. If not provided, a new connection will be created.
        """
        self.user_id = user_id
        self.db = db or get_db()

    def create_order(self, order_details, total, status='pending'):
        """
        Create a new order with the given details and total amount.

        Args:
            order_details (str): The details of the order (e.g., products and quantities).
            total (float): The total amount of the order.
            status (str): The status of the order (default is 'pending').

        Returns:
            None
        """
        cursor = self.db.cursor
        cursor.execute('''
            INSERT INTO orders (user_id, order_details, total, status)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, order_details, total, status))
        self.db.connection.commit()

    @staticmethod
    def get_orders_by_user(user_id, db=None):
        """
        Retrieve all orders for a specific user, including product details and seller names.

        Args:
            user_id (int): The ID of the user.
            db (Database): Optional database connection. If not provided, a new connection will be created.

        Returns:
            list: A list of tuples containing order information.
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            SELECT o.id, o.order_details, o.total, o.status, p.name AS product_name, u.username AS seller_name
            FROM orders o
            JOIN products p ON p.id = o.user_id
            JOIN users u ON u.id = p.user_id
            WHERE o.user_id = ?
        ''', (user_id,))
        return cursor.fetchall()

    @staticmethod
    def update_order_status(self, order_id, new_status):
        """
        Update the status of a specific order.

        Args:
            order_id (int): The ID of the order to update.
            new_status (str): The new status for the order.

        Returns:
            None
        """
        cursor = self.db.cursor
        cursor.execute('''
            UPDATE orders
            SET status = ?
            WHERE id = ? AND user_id = ?
        ''', (new_status, order_id, self.user_id))
        self.db.connection.commit()

    @staticmethod
    def get_order_by_id(order_id, db=None):
        """
        Retrieve a specific order by its ID, including product details and seller names.

        Args:
            order_id (int): The ID of the order.
            db (Database): Optional database connection. If not provided, a new connection will be created.

        Returns:
            tuple: A tuple containing order information, or None if the order is not found.
        """
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            SELECT o.id, o.order_details, o.total, o.status, p.name AS product_name, u.username AS seller_name
            FROM orders o
            JOIN products p ON p.id = o.user_id
            JOIN users u ON u.id = p.user_id
            WHERE o.id = ?
        ''', (order_id,))
        return cursor.fetchone()
