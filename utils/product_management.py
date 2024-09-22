from ecommerce.product import Product
from ecommerce.cart import Cart
from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog
from ecommerce.user import User
from prompt_toolkit.formatted_text import HTML
from utils.ui import view_ascii_art

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