from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog, button_dialog, radiolist_dialog
from prompt_toolkit.styles import Style
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

def view_ascii_art(ascii_art):
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

def display_confirmation_dialog(title, text):
    return yes_no_dialog(
        title=title,
        text=text
    ).run()

def display_message_dialog(title, text):
    button_dialog(
        title=title,
        text=text,
        buttons=[("OK", True)]
    ).run()

def input_prompt(title, text, password=False):
    return input_dialog(
        title=title,
        text=text,
        password=password
    ).run()
