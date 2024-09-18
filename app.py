from ecommerce.models import User
from ecommerce.db import get_db

def main():
    db = get_db()
    
    print("Welcome to the Simple E-commerce Backend!")
    
    while True:
        action = input("Would you like to (register, login, quit)? ").strip().lower()
        
        if action == 'register':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            try:
                User.register(username, password)
                print(f"User {username} registered successfully!")
            except ValueError as e:
                print(e)
        
        elif action == 'login':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            try:
                if User.login(username, password):
                    print(f"User {username} logged in successfully!")
            except ValueError as e:
                print(e)
        
        elif action == 'quit':
            db.close()
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
