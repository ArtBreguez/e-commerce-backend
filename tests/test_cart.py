import unittest
from ecommerce.db import get_db
from ecommerce.user import User
from ecommerce.product import Product
from ecommerce.cart import Cart


class TestCartModel(unittest.TestCase):

    def setUp(self):
        """Initial setup before each test."""
        self.db = get_db(":memory:")
        self.user_id = 1
        self.db.cursor.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", 
                               (self.user_id, "testuser", "hashed_password"))
        self.db.connection.commit()

        Product.create_product("Test Product", 50.00, "A test product description", self.user_id, db=self.db, quantity=10)

        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Test Product",))
        self.product_id = self.db.cursor.fetchone()[0]

    def tearDown(self):
        """Tear down and close the database after each test."""
        self.db.close()

    def test_add_product_to_cart(self):
        """Test adding a product to the cart."""
        cart = Cart(self.user_id, db=self.db)
        cart.add_product(self.product_id, 2)
        
        self.db.cursor.execute("SELECT * FROM carts WHERE user_id = ? AND product_id = ?", (self.user_id, self.product_id))
        cart_item = self.db.cursor.fetchone()

        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item[2], self.product_id)
        self.assertEqual(cart_item[3], 2) 

    def test_add_existing_product_increments_quantity(self):
        """Test adding an existing product increments its quantity."""
        cart = Cart(self.user_id, db=self.db)
        cart.add_product(self.product_id, 1)
        cart.add_product(self.product_id, 3)

        self.db.cursor.execute("SELECT quantity FROM carts WHERE user_id = ? AND product_id = ?", 
                               (self.user_id, self.product_id))
        updated_quantity = self.db.cursor.fetchone()[0]

        self.assertEqual(updated_quantity, 4)

    def test_view_cart(self):
        """Test viewing the cart."""
        cart = Cart(self.user_id, db=self.db)
        cart.add_product(self.product_id, 3)

        cart_items = cart.view_cart()

        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0][0], "Test Product")
        self.assertEqual(cart_items[0][1], 50.00)
        self.assertEqual(cart_items[0][2], 3)

    def test_checkout_empty_cart(self):
        """Test checking out an empty cart raises an exception."""
        cart = Cart(self.user_id, db=self.db)
        with self.assertRaises(ValueError) as e:
            cart.checkout()
        self.assertEqual(str(e.exception), "Your cart is empty. Please add products before checkout.")

    def test_checkout_cart(self):
        """Test successfully checking out a cart."""
        cart = Cart(self.user_id, db=self.db)
        cart.add_product(self.product_id, 2)

        cart.checkout()

        self.db.cursor.execute("SELECT * FROM carts WHERE user_id = ?", (self.user_id,))
        remaining_items = self.db.cursor.fetchall()

        self.assertEqual(len(remaining_items), 0)


if __name__ == '__main__':
    unittest.main()
