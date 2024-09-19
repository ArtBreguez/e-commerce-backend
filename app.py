from ecommerce.user import User
from ecommerce.db import get_db
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog
from prompt_toolkit.styles import Style
from ecommerce.product import Product 
import requests
from io import BytesIO
from PIL import Image

style = Style.from_dict({
    'dialog': 'bg:#5f819d #ffffff',
    'input': 'bg:#ffcc00 #000000',
})

def show_main_menu(logged_in_user):
    if logged_in_user:
        options = [
            ("update_username", "Update Username"),
            ("update_password", "Change Password"),
            ("delete_account", "Delete Account"),
            ("view_products", "View Products"),  
            ("create_product", "Create Product"),
            ("logout", "Logout"),
        ]
    else:
        options = [
            ("login", "Login"),
            ("register", "Register"),
        ]
    
    result = radiolist_dialog(
        title="Main Menu",
        text="Please choose an option:",
        values=[(opt[0], opt[1]) for opt in options],  
        cancel_text="Quit"  
    ).run()

    if result is None:
        exit()

    return result

def register_user():
    username = input_dialog(
        title="Register",
        text="Enter a username: "
    ).run()
    
    if username:
        password = input_dialog(
            title="Register",
            text="Enter a password: ",
            password=True  
        ).run()
        
        if password:
            try:
                User.register(username, password)
                button_dialog(
                    title="Success",
                    text=f"User {username} registered successfully!",
                    buttons=[("OK", True)]
                ).run()
            except ValueError as e:
                button_dialog(
                    title="Error",
                    text=str(e),
                    buttons=[("OK", True)]
                ).run()

def login_user():
    username = input_dialog(
        title="Login",
        text="Enter your username: "
    ).run()
    
    if username:
        password = input_dialog(
            title="Login",
            text="Enter your password: ",
            password=True  
        ).run()
        
        if password:
            try:
                if User.login(username, password):
                    button_dialog(
                        title="Success",
                        text=f"User {username} logged in successfully!",
                        buttons=[("OK", True)]
                    ).run()
                    return username
            except ValueError as e:
                button_dialog(
                    title="Error",
                    text=str(e),
                    buttons=[("OK", True)]
                ).run()
    return None

def update_username(logged_in_user):
    new_username = input_dialog(
        title="Update Username",
        text="Enter a new username: "
    ).run()
    
    if new_username:
        try:
            User.update_username(logged_in_user, new_username)
            button_dialog(
                title="Success",
                text=f"Username updated successfully to {new_username}!",
                buttons=[("OK", True)]
            ).run()
            return new_username
        except ValueError as e:
            button_dialog(
                title="Error",
                text=str(e),
                buttons=[("OK", True)]
            ).run()
    return logged_in_user

def update_password(logged_in_user):
    new_password = input_dialog(
        title="Update Password",
        text="Enter a new password: ",
        password=True  
    ).run()
    
    if new_password:
        User.update_password(logged_in_user, new_password)
        button_dialog(
            title="Success",
            text="Password updated successfully!",
            buttons=[("OK", True)]
        ).run()

def delete_account(logged_in_user):
    confirmation = yes_no_dialog(
        title="Confirm Deletion",
        text="Are you sure you want to delete your account?"
    ).run()
    
    if confirmation:
        User.delete_account(logged_in_user)
        button_dialog(
            title="Success",
            text=f"Account {logged_in_user} deleted successfully!",
            buttons=[("OK", True)]
        ).run()
        return None
    return logged_in_user

def create_product(logged_in_user):
    name = input_dialog(
        title="Create Product",
        text="Enter the product name: "
    ).run()
    
    if name:
        price = input_dialog(
            title="Create Product",
            text="Enter the product price: "
        ).run()
        description = input_dialog(
            title="Create Product",
            text="Enter the product description: "
        ).run()

        if price and description:
            try:
                user_id = User.get_user_id(logged_in_user)
                Product.create_product(name, float(price), description, user_id)
                button_dialog(
                    title="Success",
                    text=f"Product {name} created successfully!",
                    buttons=[("OK", True)]
                ).run()
            except Exception as e:
                button_dialog(
                    title="Error",
                    text=str(e),
                    buttons=[("OK", True)]
                ).run()
from prompt_toolkit.formatted_text import HTML

def view_products(logged_in_user):
    products = Product.get_all_products()
    
    if products:
        product_list = [(str(p[0]), HTML(f'{p[1]} - ${p[2]}')) for p in products]  
        
        product_selected = radiolist_dialog(
            title="Product List",
            text="Available products:\n\nSelect a product to view details:",
            values=product_list, 
            cancel_text="Back"  
        ).run()

        if product_selected is not None:  
            product = Product.get_product_by_id(int(product_selected))
            if product:
                creator = product[4]  
                product_details = (f"Name: {product[1]}\n"
                                   f"Price: ${product[2]}\n"
                                   f"Description: {product[3]}\n"
                                   f"Created by: {creator}")

                if product[5] == logged_in_user:
                    action = button_dialog(
                        title="Product Details",
                        text=f"{product_details}\n\nWhat would you like to do?",
                        buttons=[("Update", "update"), ("Delete", "delete"), ("Back", None)]
                    ).run()

                    if action == "update":
                        update_product(int(product_selected))
                    elif action == "delete":
                        delete_product(int(product_selected))
                else:
                    button_dialog(
                        title="Product Details",
                        text=product_details,
                        buttons=[("Back", True)]
                    ).run()
    else:
        button_dialog(
            title="No Products",
            text="No products found!",
            buttons=[("OK", True)]
        ).run()


def update_product(product_id):
    name = input_dialog(
        title="Update Product",
        text="Enter the new name (or leave blank to skip): "
    ).run()
    price = input_dialog(
        title="Update Product",
        text="Enter the new price (or leave blank to skip): "
    ).run()
    description = input_dialog(
        title="Update Product",
        text="Enter the new description (or leave blank to skip): "
    ).run()

    if name or price or description:
        try:
            Product.update_product(product_id, name=name, price=float(price) if price else None, 
                                   description=description)
            button_dialog(
                title="Success",
                text="Product updated successfully!",
                buttons=[("OK", True)]
            ).run()
        except Exception as e:
            button_dialog(
                title="Error",
                text=str(e),
                buttons=[("OK", True)]
            ).run()

def delete_product(product_id):
    confirmation = yes_no_dialog(
        title="Confirm Deletion",
        text="Are you sure you want to delete this product?"
    ).run()

    if confirmation:
        try:
            Product.delete_product(product_id)
            button_dialog(
                title="Success",
                text="Product deleted successfully!",
                buttons=[("OK", True)]
            ).run()
        except Exception as e:
            button_dialog(
                title="Error",
                text=str(e),
                buttons=[("OK", True)]
            ).run()

def main():
    db = get_db()
    logged_in_user = None

    while True:
        action = show_main_menu(logged_in_user)

        if action == 'register' and not logged_in_user:
            register_user()

        elif action == 'login' and not logged_in_user:
            logged_in_user = login_user()

        elif action == 'update_username' and logged_in_user:
            logged_in_user = update_username(logged_in_user)

        elif action == 'update_password' and logged_in_user:
            update_password(logged_in_user)

        elif action == 'delete_account' and logged_in_user:
            logged_in_user = delete_account(logged_in_user)

        elif action == 'view_products' and logged_in_user:
            view_products(logged_in_user)  

        elif action == 'create_product' and logged_in_user:
            create_product(logged_in_user) 

        elif action == 'logout' and logged_in_user:
            button_dialog(
                title="Logout",
                text="Logged out successfully!",
                buttons=[("OK", True)]
            ).run()
            logged_in_user = None

        elif action == 'quit':
            db.close()
            button_dialog(
                title="Goodbye",
                text="Goodbye!",
                buttons=[("OK", True)]
            ).run()
            break


if __name__ == "__main__":
    main()
