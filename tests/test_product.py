import unittest
from ecommerce.product import Product
from ecommerce.db import get_db
from utils.ascii import download_image_from_url, convert_image_to_ascii 

class TestProductModel(unittest.TestCase):
    
    def setUp(self):
        """Initial setup before each test."""
        self.db = get_db(":memory:")  
        self.user_id = 1
        self.db.cursor.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)", (self.user_id, "testuser", "hashed_password"))
        self.db.connection.commit()

        image_url = "https://upload.wikimedia.org/wikipedia/commons/f/fb/Small_pict_test.JPG"
        image = download_image_from_url(image_url)
        self.ascii_art = convert_image_to_ascii(image, new_width=100) if image else ""

    def tearDown(self):
        """Tear down and close the database after each test."""
        self.db.close()

    def test_create_product_with_ascii_art(self):
        """Test creating a new product with ASCII art."""
        Product.create_product("Test Product with ASCII", 99.99, "A test product with ASCII art", self.user_id, db=self.db, ascii_art=self.ascii_art)
        self.db.cursor.execute("SELECT * FROM products WHERE name = ?", ("Test Product with ASCII",))
        product = self.db.cursor.fetchone()

        self.assertIsNotNone(product)
        self.assertEqual(product[1], "Test Product with ASCII")
        self.assertEqual(product[2], 99.99)
        self.assertEqual(product[3], "A test product with ASCII art")
        self.assertEqual(product[4], self.user_id)
        self.assertEqual(product[5], self.ascii_art) 

    def test_get_all_products_with_ascii_art(self):
        """Test fetching all products, including ASCII art."""
        Product.create_product("Product 1", 49.99, "Description 1", self.user_id, db=self.db, ascii_art=self.ascii_art)
        Product.create_product("Product 2", 149.99, "Description 2", self.user_id, db=self.db, ascii_art=self.ascii_art)
        
        products = Product.get_all_products(self.db)

        self.assertEqual(len(products), 2)  
        self.assertEqual(products[0][1], "Product 1")
        self.assertEqual(products[1][1], "Product 2")
        self.assertEqual(products[0][5], self.ascii_art)
        self.assertEqual(products[1][5], self.ascii_art)

    def test_get_product_by_id_with_ascii_art(self):
        """Test fetching a product by its ID, including ASCII art."""
        Product.create_product("Product ID Test", 59.99, "Description for ID", self.user_id, db=self.db, ascii_art=self.ascii_art)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Product ID Test",))
        product_id = self.db.cursor.fetchone()[0]
        
        product = Product.get_product_by_id(product_id, self.db)
        
        self.assertIsNotNone(product)
        self.assertEqual(product[1], "Product ID Test")
        self.assertEqual(product[2], 59.99)
        self.assertEqual(product[5], self.ascii_art)  

    def test_update_product_with_ascii_art(self):
        """Test updating an existing product, including the ASCII art."""
        Product.create_product("Update Test", 79.99, "Before update", self.user_id, db=self.db, ascii_art=self.ascii_art)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Update Test",))
        product_id = self.db.cursor.fetchone()[0]

        new_ascii_art = convert_image_to_ascii(download_image_from_url("https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg"), new_width=100)
        Product.update_product(product_id, name="Updated Product", price=89.99, description="After update", ascii_art=new_ascii_art, db=self.db)
        
        product = Product.get_product_by_id(product_id, self.db)
        
        self.assertEqual(product[1], "Updated Product")
        self.assertEqual(product[2], 89.99)
        self.assertEqual(product[3], "After update")
        self.assertEqual(product[5], new_ascii_art)  

    def test_delete_product_with_ascii_art(self):
        """Test deleting an existing product with ASCII art."""
        Product.create_product("Delete Test", 199.99, "Delete this product", self.user_id, db=self.db, ascii_art=self.ascii_art)
        self.db.cursor.execute("SELECT id FROM products WHERE name = ?", ("Delete Test",))
        product_id = self.db.cursor.fetchone()[0]

        Product.delete_product(product_id, self.db)

        self.db.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = self.db.cursor.fetchone()
        
        self.assertIsNone(product)  

if __name__ == '__main__':
    unittest.main()
