from flask import Flask 
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
app.config,from_objects('config.Config')


def get_db():
    db = sqlite3.connect('vulnweb.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            profile_picture TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    ''')
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    try:
        db.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ('admin', 'admin@vulnweb.com', 'admin123', 1)
        )
        print("✓ Default admin created: admin/admin123")
    except sqlite3.IntegrityError:
        print("✓ Admin already exists")
    
    try:
        products = [
            ('Laptop', 'High performance laptop', 999.99, 'laptop.jpg', 10),
            ('Mouse', 'Wireless mouse', 29.99, 'mouse.jpg', 50),
            ('Keyboard', 'Mechanical keyboard', 79.99, 'keyboard.jpg', 30),
        ]
        db.executemany(
            "INSERT INTO products (name, description, price, image_url, stock) VALUES (?, ?, ?, ?, ?)",
            products
        )
        print("✓ Demo products added")
    except sqlite3.IntegrityError:
        print("✓ Products already exist")
    
    db.commit()
    db.close()
    print("✓ Database initialized!")

from app import routes
