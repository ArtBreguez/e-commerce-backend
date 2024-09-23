from ecommerce.cart import Cart
from ecommerce.order import Order
from ecommerce.user import User
from prompt_toolkit.shortcuts import yes_no_dialog, button_dialog, radiolist_dialog

def view_cart(logged_in_user):
    """
    Displays the user's cart.
    Shows a message if the cart is empty and offers checkout or removing items from the cart.
    
    Args:
        logged_in_user (str): The username of the logged-in user.
    
    Returns:
        None
    """
    user_id = User.get_user_id(logged_in_user)
    cart = Cart(user_id)
    cart_items = cart.view_cart()

    if cart_items:
        product_list = [(str(item[3]), f"{item[0]} - ${item[1]} (x{item[2]})") for item in cart_items]
        product_list.append(("checkout", "Proceed to Checkout"))

        action = radiolist_dialog(
            title="Cart Items",
            text="Select an item to remove or proceed to checkout:",
            values=product_list,
            cancel_text="Back"
        ).run()

        if action == "checkout":
            checkout(logged_in_user)
        elif action is not None:
            selected_product_id = int(action)

            selected_item = next(item for item in cart_items if item[3] == selected_product_id)

            confirmation = yes_no_dialog(
                title="Confirm Removal",
                text=f"Are you sure you want to remove {selected_item[0]} from your cart?"
            ).run()

            if confirmation:
                cart.remove_product(selected_product_id) 
                button_dialog(
                    title="Success",
                    text=f"{selected_item[0]} removed from your cart.",
                    buttons=[("OK", True)]
                ).run()

                view_cart(logged_in_user)
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
