from ecommerce.db import get_db

class Cart:
    def __init__(self, user_id, db=None):
        """
        Initialize the cart with a user ID and database connection.

        Args:
            user_id (int): The ID of the user associated with the cart.
            db (Database): Optional database connection. If not provided, a new connection will be created.
        """
        self.user_id = user_id
        self.db = db or get_db()

    def add_product(self, product_id, quantity=1):
        """
        Add a product to the cart.

        Args:
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add. Default is 1.
        """
        cursor = self.db.cursor
        cursor.execute('''
            INSERT INTO carts (user_id, product_id, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(product_id, user_id) DO UPDATE SET quantity = quantity + excluded.quantity
        ''', (self.user_id, product_id, quantity))
        self.db.connection.commit()

    def remove_product(self, product_id):
        """
        Remove a product from the cart.

        Args:
            product_id (int): The ID of the product to remove.
        """
        cursor = self.db.cursor
        cursor.execute('DELETE FROM carts WHERE user_id = ? AND product_id = ?', (self.user_id, product_id))
        self.db.connection.commit()

    def view_cart(self):
        """
        View all the items in the cart for the current user.

        Returns:
            list: A list of tuples containing product information and quantity.
        """
        cursor = self.db.cursor
        cursor.execute('''
            SELECT p.name, p.price, c.quantity
            FROM carts c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (self.user_id,))
        return cursor.fetchall()

    def checkout(self):
        """
        Checkout the cart and create an order.

        Returns:
            None
        """
        cursor = self.db.cursor
        cart_items = self.view_cart()

        if not cart_items:
            raise ValueError("Your cart is empty. Please add products before checkout.")

        order_details = ', '.join([f"{item[0]} (x{item[2]})" for item in cart_items])
        total = sum(item[1] * item[2] for item in cart_items)

        cursor.execute('''
            INSERT INTO orders (user_id, order_details, total)
            VALUES (?, ?, ?)
        ''', (self.user_id, order_details, total))

        cursor.execute('DELETE FROM carts WHERE user_id = ?', (self.user_id,))
        self.db.connection.commit()

    def clear_cart(self):
        """
        Clear all items from the cart.

        Returns:
            None
        """
        cursor = self.db.cursor
        cursor.execute('DELETE FROM carts WHERE user_id = ?', (self.user_id,))
        self.db.connection.commit()
