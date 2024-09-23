from ecommerce.db import get_db
from utils.ui import show_main_menu
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


def main():
    """
    The core function that handles the flow of the e-commerce CLI application, 
    guiding users through registration, login, product management, and order processing.
    """
    db = get_db()
    logged_in_user = None

    while True:
        action = show_main_menu(logged_in_user)

        if action == 'register' and not logged_in_user:
            logged_in_user = register_user()

        elif action == 'login' and not logged_in_user:
            logged_in_user = login_user()

        elif action == 'market_products' and logged_in_user:
            view_products(logged_in_user)

        elif action == 'view_cart' and logged_in_user:
            view_cart(logged_in_user)

        elif action == 'view_orders' and logged_in_user:
            view_orders(logged_in_user)

        elif action == 'manage_profile' and logged_in_user:
            logged_in_user = manage_profile(logged_in_user)
            if logged_in_user is None:
                continue

        elif action == 'my_products' and logged_in_user:
            view_my_products(logged_in_user)

        elif action == 'logout' and logged_in_user:
            shortcuts.button_dialog(
                title="Logout",
                text="You have logged out successfully!",
                buttons=[("OK", True)]
            ).run()
            logged_in_user = None

        elif action == 'quit':
            db.close()
            shortcuts.button_dialog(
                title="Goodbye",
                text="Thank you for using the Marketplace! Goodbye!",
                buttons=[("OK", True)]
            ).run()
            break


if __name__ == "__main__":
    main()
