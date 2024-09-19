from ecommerce.db import get_db

class Product:
    def __init__(self, name, price, description, user_id, db=None):
        self.name = name
        self.price = price
        self.description = description
        self.user_id = user_id
        self.db = db or get_db()

    @staticmethod
    def create_product(name, price, description, user_id, db=None):
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            INSERT INTO products (name, price, description, user_id)
            VALUES (?, ?, ?, ?)
        ''', (name, price, description, user_id))
        db.connection.commit()

    @staticmethod
    def get_all_products(db=None):
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('''
            SELECT *
            FROM products
        ''')
        
        return cursor.fetchall()

    @staticmethod
    def get_product_by_id(product_id, db=None):
        db = db or get_db()
        cursor = db.cursor
        
        cursor.execute('''
            SELECT p.id, p.name, p.price, p.description, u.username, p.user_id
            FROM products p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        ''', (product_id,))
        return cursor.fetchone()


    @staticmethod
    def update_product(product_id, name=None, price=None, description=None, db=None):
        db = db or get_db()
        cursor = db.cursor
        updates = []
        values = []
        if name:
            updates.append("name = ?")
            values.append(name)
        if price:
            updates.append("price = ?")
            values.append(price)
        if description:
            updates.append("description = ?")
            values.append(description)
        
        if updates:
            query = f'UPDATE products SET {", ".join(updates)} WHERE id = ?'
            values.append(product_id)
            cursor.execute(query, values)
            db.connection.commit()

    @staticmethod
    def delete_product(product_id, db=None):
        db = db or get_db()
        cursor = db.cursor
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.connection.commit()
