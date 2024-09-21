import unittest
from ecommerce.db import get_db
from ecommerce.user import User
from ecommerce.product import Product
from ecommerce.order import Order


class TestOrderModel(unittest.TestCase):

    def setUp(self):
        """Initial setup before each test."""
        self.db = get_db(":memory:")
        self.user_id = 1
        self.db.cursor.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", 
                               (self.user_id, "testuser", "hashed_password"))
        self.db.connection.commit()

        # Create a product and get its ID
        Product.create_product("Test Product", 50.00, "A test product description", self.user_id, db=self.db, quantity=10)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Test Product",))
        self.product_id = self.db.cursor.fetchone()[0]

    def tearDown(self):
        """Tear down and close the database after each test."""
        self.db.close()

    def test_create_order(self):
        """Test creating a new order and verify that it is stored in the database."""
        order_details = "Test Product - $50 (x2)"
        total = 100.00
        order = Order(self.user_id, db=self.db)
        order.create_order(order_details, total)

        self.db.cursor.execute("SELECT * FROM orders WHERE user_id = ?", (self.user_id,))
        saved_order = self.db.cursor.fetchone()

        self.assertIsNotNone(saved_order)
        self.assertEqual(saved_order[1], self.user_id)
        self.assertEqual(saved_order[2], order_details)
        self.assertEqual(saved_order[3], total)
        self.assertEqual(saved_order[4], "pending")

    def test_get_orders_by_user(self):
        """Test retrieving all orders for a specific user."""
        order_details = "Test Product - $50 (x2)"
        total = 100.00
        order = Order(self.user_id, db=self.db)
        order.create_order(order_details, total)

        orders = Order.get_orders_by_user(self.user_id, db=self.db)

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0][1], order_details)
        self.assertEqual(orders[0][2], total)

    def test_get_order_by_id(self):
        """Test retrieving an order by its ID."""
        order_details = "Test Product - $50 (x2)"
        total = 100.00
        order = Order(self.user_id, db=self.db)
        order.create_order(order_details, total)

        self.db.cursor.execute("SELECT id FROM orders WHERE user_id = ?", (self.user_id,))
        order_id = self.db.cursor.fetchone()[0]

        retrieved_order = Order.get_order_by_id(order_id, db=self.db)
        self.assertIsNotNone(retrieved_order)
        self.assertEqual(retrieved_order[0], self.user_id)
        self.assertEqual(retrieved_order[1], order_details)
        self.assertEqual(retrieved_order[2], total)
        self.assertEqual(retrieved_order[3], "pending")

    def test_update_order_status(self):
        """Test updating the status of an existing order."""
        order_details = "Test Product - $50 (x2)"
        total = 100.00
        order = Order(self.user_id, db=self.db)
        order.create_order(order_details, total)

        self.db.cursor.execute("SELECT id FROM orders WHERE user_id = ?", (self.user_id,))
        order_id = self.db.cursor.fetchone()[0]

        order.update_order_status(self, order_id, "shipped")

        updated_order = Order.get_order_by_id(order_id, db=self.db)
        self.assertEqual(updated_order[3], "shipped")


if __name__ == '__main__':
    unittest.main()
