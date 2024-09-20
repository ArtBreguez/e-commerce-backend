from faker import Faker
import random
from ecommerce.db import get_db
from ecommerce.user import User
from ecommerce.product import Product
from utils.ascii import download_image_from_url, convert_image_to_ascii

fake = Faker()

def seed_users_and_products(user_count=5, product_count_per_user=3):
    """
    Generates random users and products to populate the database.

    Args:
        user_count (int): Number of users to be created.
        product_count_per_user (int): Number of products to be created for each user.
    
    Returns:
        None
    """
    db = get_db()
    
    for _ in range(user_count):
        username = fake.user_name()
        password = fake.password()
        
        User.register(username, password, db)

        user_id = User.get_user_id(username, db)
        
        for _ in range(product_count_per_user):
            name = fake.word().capitalize() + " " + fake.word().capitalize()
            price = round(random.uniform(10.0, 100.0), 2)
            description = fake.text(max_nb_chars=200)
            quantity = random.randint(1, 20)

            image_url = "https://upload.wikimedia.org/wikipedia/commons/f/fb/Small_pict_test.JPG"
            image = download_image_from_url(image_url)
            ascii_art = convert_image_to_ascii(image, new_width=100) if image else None

            Product.create_product(name, price, description, user_id, db=db, ascii_art=ascii_art, quantity=quantity)
    
    db.close()
    print(f"Seeded {user_count} users and {user_count * product_count_per_user} products.")

if __name__ == "__main__":
    seed_users_and_products(user_count=5, product_count_per_user=3)
