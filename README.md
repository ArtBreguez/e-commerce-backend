# Simple E-commerce Marketplace Application

## Project Description

This project is a command-line based e-commerce marketplace application where users can create, view, and manage products. It supports core features like creating and managing user profiles, adding products to a marketplace, managing a personal product catalog, adding items to a shopping cart, and processing orders. The system is built with Python and uses SQLite for data storage.

The application provides a simple interface for users to interact with a marketplace through a menu-driven command-line interface. Users can register, log in, and perform different actions depending on their role as a consumer or product owner.

### Key Features
- **User registration and login**: Users can create an account, log in, update their profiles, and delete their accounts.
- **Product management**: Logged-in users can create new products, update, delete, and view the details of the products they own.
- **Marketplace browsing**: Users can browse the products listed by all users in the marketplace and view product details.
- **Cart management**: Users can add products to a shopping cart, view the contents of the cart, remove items from the cart, and proceed to checkout.
- **Order processing**: Users can finalize purchases and view their order history. If orders are in "pending" status, the user can cancel them.

## User Actions

### What users can do:

1. **Create an account**: A user can register by providing a valid username and password. The username must be at least 3 characters long, and the password must be at least 6 characters.
2. **Log in to the system**: Registered users can log in using their credentials.
3. **Update profile**: Users can update their username or password. Usernames and passwords are subject to minimum length requirements.
4. **Delete account**: Users can delete their account, and all associated products and data will be removed.
5. **Create a product**: Logged-in users can create products by specifying a product name, price, description, quantity, and optional ASCII art generated from an image link.
6. **View their products**: Users can view a list of the products they have created, along with their details.
7. **Update or delete their products**: Users can edit the name, description, price, quantity, and image of their products. They can also delete products they no longer wish to list.
8. **Browse the marketplace**: All users can view the marketplace and see the products listed by all users. They can view the product details, including price, description, and quantity.
9. **Add products to their cart**: Users can add products from the marketplace to their shopping cart. They can specify the quantity of the product to add, as long as the quantity is available.
10. **Remove products from their cart**: Users can remove items from their cart.
11. **Checkout**: Users can proceed to checkout, which will create an order and empty the cart.
12. **View order history**: Users can view their past orders, including the details of each order and its status.
13. **Cancel pending orders**: Users can cancel orders that are still in a "pending" state.

### What users cannot do:

1. **Purchase unavailable products**: Users cannot add products with a quantity of 0 to their cart.
2. **Modify other users' products**: Users cannot edit or delete products they did not create.
3. **Access marketplace features without logging in**: All actions involving product management, the shopping cart, or order processing require the user to be logged in.

## Setup and Running the Application

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.10 or later
- Pip (Python package installer)

### Steps to Set Up

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ArtBreguez/e-commerce-backend
   cd e-commerce-backend
   ```
2. **Install dependencies**:

   ```bash
   pip -r install requirements.txt
   ```
3. **Set up the database**:

    The application uses SQLite for its database. The database will be automatically initialized when you first run the application.
    
    If you want to populate the database with fake data, just run the command in project root directory:

    ```bash
    python seed.py
    ```
4. **Run the application**:

    To start the application, run:
    ```bash
    python app.py
    ```

## Application Structure

- **ecommerce/**: Contains the core logic for users, products, orders, and the cart system.
- **utils/**: Contains utility functions for user interaction, ASCII art conversion, and downloading images.
- **tests/**: Contains unit tests to ensure the application functions as expected.

## Testing the Application

Unit tests are written using Python’s `unittest` framework and can be executed with the following command:

```bash
python3 -m unittest discover tests/
```

Ensure you are in the root directory of the project before running this command.

## Assumptions Made

### Users:
- A user can create multiple products and view the details of each product.
- Users can only edit or delete the products they have created.

### Products:
- Products have a name, price, description, and quantity.
- A product with a quantity of zero is considered unavailable for purchase.

### Cart and Orders:
- Users can add items to their cart and proceed to checkout to create an order.
- Users can cancel orders that are still in "pending" status.

## Future Improvements

- **Role-based Access**: Introduce more user roles, such as admin or moderator, to manage the marketplace more efficiently.
- **Product Categories**: Allow users to categorize their products, making it easier for others to browse.
- **Search and Filter**: Add search and filter functionality to make product discovery easier for users.