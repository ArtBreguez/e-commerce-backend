from ecommerce.db import get_db
from utils.ui import (
    show_main_menu
)
from utils.user_management import (
    register_user,
    login_user,
    manage_profile,
    update_username,
    update_password,
    delete_account
)
from utils.product_management import (
    create_product,
    view_products,
    view_my_products
)
from utils.cart_and_order import (
    view_cart,
    checkout,
    view_orders
)
import prompt_toolkit.shortcuts as shortcuts
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog

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
            shortcuts.button_dialog(
                title="Logout",
                text="Logged out successfully!",
                buttons=[("OK", True)]
            ).run()
            logged_in_user = None

        elif action == 'quit':
            db.close()
            shortcuts.button_dialog(
                title="Goodbye",
                text="Goodbye!",
                buttons=[("OK", True)]
            ).run()
            break

if __name__ == "__main__":
    main()