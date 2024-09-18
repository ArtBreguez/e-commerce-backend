from ecommerce.models import User
from ecommerce.db import get_db

def main():
    db = get_db()
    logged_in_user = None
    
    print("Welcome to the Simple E-commerce Backend!")
    
    while True:
        if logged_in_user:
            action = input("Would you like to (update_username, update_password, delete_account, logout)? ").strip().lower()
        else:
            action = input("Would you like to (register, login, quit)? ").strip().lower()
        
        if action == 'register' and not logged_in_user:
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            try:
                User.register(username, password)
                print(f"User {username} registered successfully!")
            except ValueError as e:
                print(e)

        elif action == 'login' and not logged_in_user:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            try:
                if User.login(username, password):
                    logged_in_user = username
                    print(f"User {username} logged in successfully!")
            except ValueError as e:
                print(e)

        elif action == 'update_username' and logged_in_user:
            new_username = input("Enter a new username: ")
            try:
                User.update_username(logged_in_user, new_username)
                logged_in_user = new_username  
                print(f"Username updated successfully to {new_username}!")
            except ValueError as e:
                print(e)

        elif action == 'update_password' and logged_in_user:
            new_password = input("Enter a new password: ")
            User.update_password(logged_in_user, new_password)
            print(f"Password updated successfully!")

        elif action == 'delete_account' and logged_in_user:
            confirmation = input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                User.delete_account(logged_in_user)
                print(f"Account {logged_in_user} deleted successfully!")
                logged_in_user = None  

        elif action == 'logout' and logged_in_user:
            logged_in_user = None
            print("Logged out successfully!")

        elif action == 'quit':
            db.close()
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
