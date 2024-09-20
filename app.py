from ecommerce.user import User
from ecommerce.db import get_db
from utils.ascii import convert_image_to_ascii, download_image_from_url
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog
from prompt_toolkit.styles import Style
from ecommerce.product import Product 
import requests
from io import BytesIO
from PIL import Image
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Button, Dialog, TextArea
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.application import get_app  


# Define a custom style for the dialogs and inputs
style = Style.from_dict({
    'dialog': 'bg:#5f819d #ffffff',
    'input': 'bg:#ffcc00 #000000',
})

def show_main_menu(logged_in_user):
    """
    Displays the main menu to the user, either logged-in or logged-out state.

    Args:
        logged_in_user (str or None): The username of the logged-in user, or None if no user is logged in.

    Returns:
        str: The selected action from the menu.
    """
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
    """
    Handles user registration by prompting for a username and password.

    Returns:
        None
    """
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
    """
    Handles user login by prompting for a username and password.

    Returns:
        str or None: The logged-in username if successful, or None if login fails.
    """
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
    """
    Allows the logged-in user to update their username.

    Args:
        logged_in_user (str): The current username of the logged-in user.

    Returns:
        str: The new username after the update.
    """
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

def delete_account(logged_in_user):
    """
    Allows the logged-in user to delete their account after confirmation.

    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None or str: None if the account is deleted, or the logged-in username if the action is canceled.
    """
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
    """
    Allows the logged-in user to create a new product, with price validation and image URL for ASCII art.

    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None
    """
    name = input_dialog(
        title="Create Product",
        text="Enter the product name: "
    ).run()
    
    if name:
        while True:  
            price = input_dialog(
                title="Create Product",
                text="Enter the product price (USD): "
            ).run()
            
            try:
                price = float(price)
                break  
            except ValueError:
                button_dialog(
                    title="Error",
                    text="Invalid price. Please enter a valid number.",
                    buttons=[("OK", True)]
                ).run()

        description = input_dialog(
            title="Create Product",
            text="Enter the product description: "
        ).run()

        image_url = input_dialog(
            title="Create Product",
            text="Enter the image URL (optional, for ASCII art): "
        ).run()

        # Download and convert the image to ASCII art
        ascii_art = ""
        if image_url:
            image = download_image_from_url(image_url)
            if image:
                ascii_art = convert_image_to_ascii(image)
            else:
                ascii_art = "Image not available"

        if description:
            try:
                user_id = User.get_user_id(logged_in_user)
                Product.create_product(name, price, description, user_id, ascii_art)
                button_dialog(
                    title="Success",
                    text=f"Product {name} created successfully with ASCII art!",
                    buttons=[("OK", True)]
                ).run()
            except Exception as e:
                button_dialog(
                    title="Error",
                    text=str(e),
                    buttons=[("OK", True)]
                ).run()

def view_products(logged_in_user):
    """
    Displays the list of products and allows the user to view details, update, or delete them if they are the creator.
    Shows an option to view the ASCII art in detail with scroll functionality.

    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None
    """
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
                ascii_art = product[5] 

                product_details = (f"Name: {product[1]}\n"
                                   f"Price: ${product[2]}\n"
                                   f"Description: {product[3]}\n"
                                   f"Created by: {creator}")

                if creator == logged_in_user:
                    action = button_dialog(
                        title="Product Details",
                        text=f"{product_details}\n\nWhat would you like to do?",
                        buttons=[("Update", "update"), ("Delete", "delete"), ("View Image", "view_image"), ("Back", None)]
                    ).run()

                    if action == "update":
                        update_product(int(product_selected)) 
                    elif action == "delete":
                        delete_product(int(product_selected))
                    elif action == "view_image":
                        view_ascii_art(ascii_art)
                else:
                    action = button_dialog(
                        title="Product Details",
                        text=f"{product_details}",
                        buttons=[("View Image", "view_image"), ("Back", True)]
                    ).run()

                    if action == "view_image":
                        view_ascii_art(ascii_art)
    else:
        button_dialog(
            title="No Products",
            text="No products found!",
            buttons=[("OK", True)]
        ).run()

def view_ascii_art(ascii_art):
    """
    Displays the ASCII art in a scrollable window using TextArea.

    Args:
        ascii_art (str): The ASCII art to display.

    Returns:
        None
    """
    text_area = TextArea(text=ascii_art, scrollbar=True, focusable=True, wrap_lines=False)

    dialog = Dialog(
        title="ASCII Art (Scroll to view)",
        body=HSplit([text_area]),  
        buttons=[Button(text="Back", handler=lambda: get_app().exit())] 
    )

    kb = KeyBindings()
    
    @kb.add("q") 
    def exit_(event):
        event.app.exit()

    layout = Layout(dialog)
    app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True)

    app.run()

def update_product(product_id):
    """
    Allows the user to update a product's name, price, description, or ASCII art, with validation.

    Args:
        product_id (int): The ID of the product to update.

    Returns:
        None
    """
    name = input_dialog(
        title="Update Product",
        text="Enter the new name (or leave blank to skip): "
    ).run()
    
    while True:
        price = input_dialog(
            title="Update Product",
            text="Enter the new price (or leave blank to skip): "
        ).run()

        if price == "":
            price = None
            break

        try:
            price = float(price)
            break  
        except ValueError:
            button_dialog(
                title="Error",
                text="Invalid price. Please enter a valid number.",
                buttons=[("OK", True)]
            ).run()

    description = input_dialog(
        title="Update Product",
        text="Enter the new description (or leave blank to skip): "
    ).run()

    image_url = input_dialog(
        title="Update Product",
        text="Enter the new image URL (for ASCII art) or leave blank to skip: "
    ).run()

    # Download and convert the image to ASCII art if a new URL is provided
    ascii_art = None
    if image_url:
        image = download_image_from_url(image_url)
        if image:
            ascii_art = convert_image_to_ascii(image)
        else:
            ascii_art = "Image not available"

    if name or price or description or ascii_art:
        try:
            Product.update_product(product_id, name=name, price=price, description=description, ascii_art=ascii_art)
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
    """
    Allows the user to delete a product after confirmation.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        None
    """
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
    """
    Main function that controls the application flow, including user login, product creation,
    product management, and logout.

    Returns:
        None
    """
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
