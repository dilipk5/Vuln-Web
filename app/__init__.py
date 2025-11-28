from flask import Flask, request
import sqlite3
import os
import logging

# Get the parent directory (vuln-web root)
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
            template_folder='templates',
            static_folder=os.path.join(basedir, 'static'))
app.config.from_object('config.Config')

# ------------------------------
# POST BODY LOGGING
# ------------------------------

# Ensure log directory exists
log_dir = os.path.join(basedir, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configure logger
logging.basicConfig(level=logging.INFO)
post_logger = logging.getLogger("vulnweb_post_logger")
post_logger.setLevel(logging.INFO)

# Create file handler
log_file = os.path.join(log_dir, 'post.log')
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - IP: %(client_ip)s - PATH: %(path)s - BODY: %(body)s')
handler.setFormatter(formatter)

# Add handler to logger
post_logger.addHandler(handler)

print(f"✓ POST logging enabled: {log_file}")

# Middleware hook to log POST request bodies
@app.before_request
def log_post_body():
    if request.method == 'POST':
        # Get form data
        form_data = dict(request.form)
        
        # Get raw body if no form data
        if not form_data:
            body_data = request.get_data(as_text=True)
        else:
            body_data = str(form_data)
        
        # Log it
        post_logger.info(
            f"POST request received",
            extra={
                "client_ip": request.remote_addr,
                "path": request.path,
                "body": body_data
            }
        )
        
        # Also print to console for debugging
        print(f"[POST] {request.remote_addr} -> {request.path} | Body: {body_data}")

# ------------------------------
# DATABASE FUNCTIONS
# ------------------------------

# Database connection helper
def get_db():
    db = sqlite3.connect('vuln_web.db')
    db.row_factory = sqlite3.Row
    return db

# Initialize database
def init_db():
    db = get_db()
    
    # Create users table
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
    
    # Create posts table
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
    
    # Create comments table
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
    
    # Create products table
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
    
    # Create orders table
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
    
    # VULNERABLE: Create default admin with plain text password
    try:
        db.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ('admin', 'admin@vulnweb.com', 'admin123', 1)
        )
        print("✓ Default admin created: admin/admin123")
    except sqlite3.IntegrityError:
        print("✓ Admin already exists")
    
    # Add fake users
    try:
        fake_users = [
            ('alice', 'alice@example.com', 'password123', 0),
            ('bob', 'bob@example.com', 'qwerty', 0),
            ('charlie', 'charlie@example.com', '123456', 0),
            ('diana', 'diana@example.com', 'letmein', 0),
        ]
        db.executemany(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            fake_users
        )
        print("✓ Fake users created (alice, bob, charlie, diana)")
    except sqlite3.IntegrityError:
        print("✓ Fake users already exist")
    
    # Add fake blog posts
    try:
        fake_posts = [
            ('Welcome to Vuln-Web!', 
             '<h2>Hello World!</h2><p>This is our first blog post. Welcome to our intentionally vulnerable web application!</p><p>Feel free to explore and learn about web security.</p>',
             1),  # Posted by admin
            
            ('SQL Injection Tips',
             '<p>Did you know you can use SQL injection to bypass login? Try using <code>\' OR \'1\'=\'1</code> in the username field!</p><p><strong>Remember:</strong> Always sanitize your inputs!</p>',
             2),  # Posted by alice
            
            ('XSS is Fun!',
             '<p>Cross-Site Scripting is everywhere! Try posting <script>alert("XSS")</script> in the comments below!</p><img src=x onerror="alert(\'Image XSS\')">',
             3),  # Posted by bob
            
            ('My Favorite Products',
             '<p>I just bought a laptop from the shop! The price was amazing... maybe too amazing? 😉</p><p>Pro tip: Check the browser console when purchasing!</p>',
             4),  # Posted by charlie
        ]
        db.executemany(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            fake_posts
        )
        print("✓ Fake blog posts created")
    except sqlite3.IntegrityError:
        print("✓ Fake posts already exist")
    
    # Add fake comments
    try:
        fake_comments = [
            (1, 2, 'Great post! This site is really helpful for learning security.'),
            (1, 3, '<script>alert("XSS in comments!")</script> Nice introduction!'),
            (2, 1, 'Thanks for the tip! SQL injection is a critical vulnerability.'),
            (2, 4, 'I tried it and it worked! This is crazy 😱'),
            (3, 2, '<img src=x onerror=alert("Comment XSS")> Interesting topic!'),
            (4, 1, 'Remember to validate prices on the server side, not client side!'),
        ]
        db.executemany(
            "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
            fake_comments
        )
        print("✓ Fake comments created")
    except sqlite3.IntegrityError:
        print("✓ Fake comments already exist")
    
    # Add some demo products
    try:
        products = [
            ('Laptop', 'High performance laptop', 999.99, 'laptop.jpg', 10),
            ('Mouse', 'Wireless mouse', 29.99, 'mouse.jpg', 50),
            ('Keyboard', 'Mechanical keyboard', 79.99, 'keyboard.jpg', 30),
            ('Monitor', '4K Ultra HD monitor', 399.99, 'monitor.jpg', 15),
            ('Headphones', 'Noise cancelling headphones', 149.99, 'headphones.jpg', 25),
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

# Import routes after app is created
from app import routes

