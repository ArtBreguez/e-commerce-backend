from ecommerce.user import User
from ecommerce.product import Product
from ecommerce.cart import Cart
from ecommerce.order import Order
from utils.ui import display_message_dialog, input_prompt, display_confirmation_dialog, input_dialog, radiolist_dialog, yes_no_dialog, button_dialog

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
        str: The new username after the update, or the current username if no update is made.
    """
    while True:
        new_username = input_dialog(
            title="Update Username",
            text="Enter a new username (min. 3 characters): "
        ).run()

        if new_username is None: 
            button_dialog(
                title="Canceled",
                text="Username update canceled.",
                buttons=[("OK", True)]
            ).run()
            return logged_in_user

        if len(new_username) < 3:
            button_dialog(
                title="Error",
                text="Username must be at least 3 characters long.",
                buttons=[("OK", True)]
            ).run()
            continue

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
    """
    Allows the logged-in user to update their password.

    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None
    """
    while True:
        current_password = input_dialog(
            title="Update Password",
            text="Enter your current password:",
            password=True
        ).run()

        if current_password is None:  
            button_dialog(
                title="Canceled",
                text="Password update canceled.",
                buttons=[("OK", True)]
            ).run()
            return

        if not current_password:
            button_dialog(
                title="Error",
                text="Current password cannot be empty.",
                buttons=[("OK", True)]
            ).run()
            continue

        new_password = input_dialog(
            title="Update Password",
            text="Enter your new password (min. 6 characters):",
            password=True
        ).run()

        if new_password is None:  
            button_dialog(
                title="Canceled",
                text="Password update canceled.",
                buttons=[("OK", True)]
            ).run()
            return

        if len(new_password) < 6:
            button_dialog(
                title="Error",
                text="Password must be at least 6 characters long.",
                buttons=[("OK", True)]
            ).run()
            continue

        confirm_password = input_dialog(
            title="Update Password",
            text="Confirm your new password:",
            password=True
        ).run()

        if confirm_password is None:  
            button_dialog(
                title="Canceled",
                text="Password update canceled.",
                buttons=[("OK", True)]
            ).run()
            return

        if new_password != confirm_password:
            button_dialog(
                title="Error",
                text="New password and confirmation do not match.",
                buttons=[("OK", True)]
            ).run()
        else:
            try:
                User.update_password(logged_in_user, current_password, new_password)
                button_dialog(
                    title="Success",
                    text="Password updated successfully!",
                    buttons=[("OK", True)]
                ).run()
                break
            except ValueError as e:
                button_dialog(
                    title="Error",
                    text=str(e),
                    buttons=[("OK", True)]
                ).run()
                break

def delete_account(logged_in_user):
    """
    Allows the logged-in user to delete their account after confirmation, and deletes all associated data.

    Args:
        logged_in_user (str): The username of the logged-in user.

    Returns:
        None: Always returns None as the user account is deleted.
    """
    confirmation = yes_no_dialog(
        title="Confirm Deletion",
        text="Are you sure you want to delete your account? All products, carts, and orders will be removed."
    ).run()

    if confirmation:
        user_id = User.get_user_id(logged_in_user)
        Product.delete_products_by_user(user_id)  

        Cart.clear_cart_by_user(user_id)  

        Order.delete_orders_by_user(user_id)  

        User.delete_account(logged_in_user)  

        button_dialog(
            title="Success",
            text=f"Account {logged_in_user} and all associated data deleted successfully!",
            buttons=[("OK", True)]
        ).run()

        raise SystemExit  
    return logged_in_user
