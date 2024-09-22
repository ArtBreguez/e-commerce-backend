from ecommerce.user import User
from ecommerce.db import get_db
from utils.ascii import convert_image_to_ascii, download_image_from_url
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog
from prompt_toolkit.styles import Style
from ecommerce.product import Product 
from ecommerce.cart import Cart
from ecommerce.order import Order
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
            ("market_products", "Market Products"),  
            ("my_products", "My Products"),         
            ("view_cart", "View Cart"),
            ("view_orders", "View Orders"),
            ("manage_profile", "Manage Profile"),
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


def manage_profile(logged_in_user):
    """
    Displays the profile management options: update username, change password, or delete account.

    Args:
        logged_in_user (str): The username of the logged-in user.
    
    Returns:
        None
    """
    options = [
        ("update_username", "Update Username"),
        ("update_password", "Change Password"),
        ("delete_account", "Delete Account"),
    ]

    action = radiolist_dialog(
        title="Manage Profile",
        text="Select an option:",
        values=options
    ).run()

    if action == "update_username":
        update_username(logged_in_user)
    elif action == "update_password":
        update_password(logged_in_user)
    elif action == "delete_account":
        delete_account(logged_in_user)
    elif action == "back":
        return


def register_user():
    """
    Handles user registration by prompting for a username and password.

    Returns:
        None
    """
    while True:
        username = input_dialog(
            title="Register",
            text="Enter a username (min. 3 characters): "
        ).run()

        if username and len(username) < 3:
            button_dialog(
                title="Error",
                text="Username must be at least 3 characters long.",
                buttons=[("OK", True)]
            ).run()
        else:
            break
    
    while True:
        password = input_dialog(
            title="Register",
            text="Enter a password (min. 6 characters): ",
            password=True  
        ).run()

        if password and len(password) < 6:
            button_dialog(
                title="Error",
                text="Password must be at least 6 characters long.",
                buttons=[("OK", True)]
            ).run()
        else:
            break

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
    Allows the logged-in user to create a new product, with price, quantity, and ASCII art validation.
    
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

        while True:
            quantity = input_dialog(
                title="Create Product",
                text="Enter the product quantity available: "
            ).run()

            try:
                quantity = int(quantity)
                break
            except ValueError:
                button_dialog(
                    title="Error",
                    text="Invalid quantity. Please enter a valid integer.",
                    buttons=[("OK", True)]
                ).run()

        image_url = input_dialog(
            title="Product Image",
            text="Enter the image URL to convert to ASCII (leave blank to skip): "
        ).run()

        ascii_art = None
        if image_url:
            try:
                image = download_image_from_url(image_url)
                if image:
                    ascii_art = convert_image_to_ascii(image, new_width=100)
            except Exception as e:
                button_dialog(
                    title="Error",
                    text=f"Failed to convert image: {e}",
                    buttons=[("OK", True)]
                ).run()

        if description:
            try:
                user_id = User.get_user_id(logged_in_user)
                Product.create_product(name, price, description, user_id, quantity=quantity, ascii_art=ascii_art)
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


def view_products(logged_in_user):
    """
    Displays the list of products and allows the user to view details, update, or delete them if they are the creator.
    Also shows an option to add the product to the cart if it's not created by the logged-in user.
    
    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None
    """
    products = Product.get_all_products()
    
    if products:
        product_list = [(str(p[0]), HTML(f'{p[1]} - ${p[2]} (Quantity: {p[6]})')) for p in products]  
        
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
                ascii_art = product[5] if product[5] is not None else "No ASCII art available."
                quantity = product[6]   

                product_details = (f"Name: {product[1]}\n"
                                   f"Price: ${product[2]}\n"
                                   f"Description: {product[3]}\n"
                                   f"Quantity: {quantity}\n"
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
                    if quantity == 0:
                        button_dialog(
                            title="Product Unavailable",
                            text="This product is currently unavailable.",
                            buttons=[("OK", True)]
                        ).run()
                    else:
                        action = button_dialog(
                            title="Product Details",
                            text=f"{product_details}",
                            buttons=[("Add to Cart", "add_to_cart"), ("View Image", "view_image"), ("Back", True)]
                        ).run()

                        if action == "add_to_cart":
                            while True:
                                quantity_to_add = input_dialog(
                                    title="Add to Cart",
                                    text=f"Enter the quantity to add (Available: {quantity}): "
                                ).run()

                                try:
                                    quantity_to_add = int(quantity_to_add)
                                    if 0 < quantity_to_add <= quantity:
                                        user_id = User.get_user_id(logged_in_user)
                                        cart = Cart(user_id)
                                        cart.add_product(int(product_selected), quantity_to_add)
                                        button_dialog(
                                            title="Success",
                                            text=f"Added {quantity_to_add} of {product[1]} to the cart.",
                                            buttons=[("OK", True)]
                                        ).run()
                                        break
                                    else:
                                        button_dialog(
                                            title="Error",
                                            text="Invalid quantity. Please enter a number between 1 and the available quantity.",
                                            buttons=[("OK", True)]
                                        ).run()
                                except ValueError:
                                    button_dialog(
                                        title="Error",
                                        text="Invalid input. Please enter a valid integer.",
                                        buttons=[("OK", True)]
                                    ).run()

                        elif action == "view_image":
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
        ascii_art (str): The ASCII art to display, or a message if no art is available.

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
    Allows the user to update a product's name, price, description, quantity, and ASCII art.
    
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

    while True:
        quantity = input_dialog(
            title="Update Product",
            text="Enter the new quantity available (or leave blank to skip): "
        ).run()

        if quantity == "":
            quantity = None
            break

        try:
            quantity = int(quantity)
            break
        except ValueError:
            button_dialog(
                title="Error",
                text="Invalid quantity. Please enter a valid integer.",
                buttons=[("OK", True)]
            ).run()

    if name or price or description or quantity is not None:
        try:
            Product.update_product(product_id, name=name, price=price, description=description, quantity=quantity)
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

def view_cart(logged_in_user):
    """
    Displays the user's cart.
    Shows a message if the cart is empty and offers checkout if items are in the cart.
    
    Args:
        logged_in_user (str): The username of the logged-in user.
    
    Returns:
        None
    """
    user_id = User.get_user_id(logged_in_user)
    cart = Cart(user_id)
    cart_items = cart.view_cart()

    if cart_items:
        cart_details = "\n".join([f"{item[0]} - ${item[1]} (x{item[2]})" for item in cart_items])
        action = button_dialog(
            title="Cart Items",
            text=f"Your cart:\n\n{cart_details}",
            buttons=[("Checkout", "checkout"), ("Back", True)]
        ).run()

        if action == "checkout":
            checkout(logged_in_user)
    else:
        button_dialog(
            title="Cart is Empty",
            text="Your cart is currently empty.",
            buttons=[("OK", True)]
        ).run()

def checkout(logged_in_user):
    """
    Handles the checkout process and creates a new order.

    Args:
        logged_in_user (str): The username of the logged-in user.
    
    Returns:
        None
    """
    user_id = User.get_user_id(logged_in_user)
    cart = Cart(user_id)
    cart_items = cart.view_cart()

    if cart_items:
        order_details = "\n".join([f"{item[0]} (x{item[2]}) - ${item[1] * item[2]}" for item in cart_items])
        total = sum([item[1] * item[2] for item in cart_items])

        order = Order(user_id)
        order.create_order(order_details, total)  

        cart.clear_cart()

        button_dialog(
            title="Checkout",
            text="Order placed successfully! Your order is now pending.",
            buttons=[("OK", True)]
        ).run()
    else:
        button_dialog(
            title="Error",
            text="Your cart is empty. Please add products before checkout.",
            buttons=[("OK", True)]
        ).run()


def view_orders(logged_in_user):
    """
    Displays a list of the user's orders with the product name and status.
    Allows viewing more details and canceling the order if it's in 'pending' status.

    Args:
        logged_in_user (str): The username of the logged-in user.
    
    Returns:
        None
    """
    user_id = User.get_user_id(logged_in_user)
    order = Order(user_id)  
    orders = order.get_orders_by_user(user_id)  

    if orders:
        order_list = [(str(order[0]), f"Order ID: {order[0]} - Status: {order[3]}") for order in orders]

        order_selected = radiolist_dialog(
            title="Order List",
            text="Select an order to view details:",
            values=order_list,  
            cancel_text="Back" 
        ).run()

        if order_selected is not None:
            selected_order = next(o for o in orders if str(o[0]) == order_selected)
            order_details = (f"Order ID: {selected_order[0]}\n"
                             f"Details: {selected_order[1]}\n"
                             f"Total: ${selected_order[2]}\n"
                             f"Status: {selected_order[3]}")

            buttons = [("Back", True)]
            
            if selected_order[3] == "pending":
                buttons.append(("Cancel Order", "cancel"))

            action = button_dialog(
                title="Order Details",
                text=order_details,
                buttons=buttons
            ).run()

            if action == "cancel":
                confirmation = yes_no_dialog(
                    title="Cancel Order",
                    text="Are you sure you want to cancel this order?"
                ).run()

                if confirmation:
                    order.cancel_order(selected_order[0]) 
                    button_dialog(
                        title="Success",
                        text="Your order has been canceled.",
                        buttons=[("OK", True)]
                    ).run()

    else:
        button_dialog(
            title="No Orders",
            text="You have no orders.",
            buttons=[("OK", True)]
        ).run()


def view_my_products(logged_in_user):
    """
    Displays the list of products created by the logged-in user.
    Allows the user to create, update, or delete their products.

    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None
    """
    user_id = User.get_user_id(logged_in_user)
    products = Product.get_products_by_user_id(user_id)

    options = [("create_product", "Create New Product")]

    if products:
        product_list = [(str(p[0]), HTML(f'{p[1]} - ${p[2]} (Quantity: {p[6]})')) for p in products]
        options.extend(product_list)

    product_selected = radiolist_dialog(
        title="My Products",
        text="Your products:\n\nSelect a product to view details or create a new product:",
        values=options,
        cancel_text="Back"
    ).run()

    if product_selected == "create_product":
        create_product(logged_in_user)
    elif product_selected is not None:
        product = Product.get_product_by_id(int(product_selected))
        if product:
            ascii_art = product[5] if product[5] is not None else "No ASCII art available."
            quantity = product[6]

            product_details = (f"Name: {product[1]}\n"
                               f"Price: ${product[2]}\n"
                               f"Description: {product[3]}\n"
                               f"Quantity: {quantity}\n")

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
        button_dialog(
            title="No Products",
            text="You have not created any products.",
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

        elif action == 'market_products' and logged_in_user:
            view_products(logged_in_user)  

        elif action == 'create_product' and logged_in_user:
            create_product(logged_in_user) 
        
        elif action == 'view_cart' and logged_in_user:
            view_cart(logged_in_user)

        elif action == 'checkout' and logged_in_user:
            checkout(logged_in_user)
        
        elif action == 'view_orders' and logged_in_user:
            view_orders(logged_in_user)
        
        elif action == 'manage_profile' and logged_in_user:
            manage_profile(logged_in_user)

        elif action == 'my_products' and logged_in_user:
            view_my_products(logged_in_user)
        
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
