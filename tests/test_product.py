import unittest
from ecommerce.product import Product
from ecommerce.db import get_db

class TestProductModel(unittest.TestCase):
    
    def setUp(self):
        """ Initial setup before each test. """
        self.db = get_db(":memory:")  
        self.user_id = 1
        self.db.cursor.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", (self.user_id, "testuser", "hashed_password"))
        self.db.connection.commit()

    def tearDown(self):
        """ Tear down and close the database after each test. """
        self.db.close()

    def test_create_product(self):
        """ Test creating a new product. """
        Product.create_product("Test Product", 99.99, "A test product", self.user_id, self.db)
        self.db.cursor.execute("SELECT * FROM products WHERE name = ?", ("Test Product",))
        product = self.db.cursor.fetchone()

        self.assertIsNotNone(product)
        self.assertEqual(product[1], "Test Product")
        self.assertEqual(product[2], 99.99)
        self.assertEqual(product[3], "A test product")
        self.assertEqual(product[4], self.user_id)

    def test_get_all_products(self):
        """ Test fetching all products. """
        Product.create_product("Product 1", 49.99, "Description 1", self.user_id, self.db)
        Product.create_product("Product 2", 149.99, "Description 2", self.user_id, self.db)
        
        products = Product.get_all_products(self.db)

        self.assertEqual(len(products), 2)  
        self.assertEqual(products[0][1], "Product 1")
        self.assertEqual(products[1][1], "Product 2")

    def test_get_product_by_id(self):
        """ Test fetching a product by its ID. """
        Product.create_product("Product ID Test", 59.99, "Description for ID", self.user_id, self.db)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Product ID Test",))
        product_id = self.db.cursor.fetchone()[0]
        
        product = Product.get_product_by_id(product_id, self.db)
        
        self.assertIsNotNone(product)
        self.assertEqual(product[1], "Product ID Test")
        self.assertEqual(product[2], 59.99)

    def test_update_product(self):
        """ Test updating an existing product. """
        Product.create_product("Update Test", 79.99, "Before update", self.user_id, self.db)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Update Test",))
        product_id = self.db.cursor.fetchone()[0]

        Product.update_product(product_id, name="Updated Product", price=89.99, description="After update", db=self.db)
        
        product = Product.get_product_by_id(product_id, self.db)
        
        self.assertEqual(product[1], "Updated Product")
        self.assertEqual(product[2], 89.99)
        self.assertEqual(product[3], "After update")

    def test_delete_product(self):
        """ Test deleting an existing product. """
        Product.create_product("Delete Test", 199.99, "Delete this product", self.user_id, self.db)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Delete Test",))
        product_id = self.db.cursor.fetchone()[0]

        Product.delete_product(product_id, self.db)

        self.db.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = self.db.cursor.fetchone()
        
        self.assertIsNone(product)  
