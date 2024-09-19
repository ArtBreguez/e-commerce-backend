from ecommerce.models import User
from ecommerce.db import get_db
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog
from prompt_toolkit.styles import Style

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
            ("logout", "Logout"),
        ]
    else:
        options = [
            ("register", "Register"),
            ("login", "Login"),
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
