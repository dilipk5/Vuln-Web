from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from app import app, get_db
import os
import hashlib
import time

# ======================
# HOME & BASIC PAGES
# ======================

@app.route('/')
def index():
    return render_template('index.html')

# ======================
# AUTHENTICATION
# ======================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        
        # VULNERABLE: Plain text password storage
        try:
            db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Username or email already exists!', 'error')
        finally:
            db.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        
        # VULNERABLE: SQL Injection via string formatting
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = db.execute(query).fetchone()
        db.close()
        
        if user:
            # VULNERABLE: Session fixation - not regenerating session ID
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            # VULNERABLE: User enumeration
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# ======================
# USER PROFILE (IDOR Vulnerabilities)
# ======================

@app.route('/user/<int:user_id>')
def view_profile(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('profile.html', user=user)

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    # VULNERABLE: No authorization check - anyone can edit any profile (IDOR)
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    db = get_db()
    
    if request.method == 'POST':
        email = request.form['email']
        
        # VULNERABLE: SQL Injection via string formatting
        query = f"UPDATE users SET email = '{email}' WHERE id = {user_id}"
        db.execute(query)
        db.commit()
        flash('Profile updated!', 'success')
    
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    
    return render_template('edit_profile.html', user=user)

# ======================
# BLOG FEATURES
# ======================

@app.route('/blog')
def blog_list():
    db = get_db()
    posts = db.execute('''
        SELECT posts.*, users.username 
        FROM posts 
        JOIN users ON posts.author_id = users.id 
        ORDER BY posts.created_at DESC
    ''').fetchall()
    db.close()
    
    return render_template('blog_list.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    db = get_db()
    post = db.execute('''
        SELECT posts.*, users.username 
        FROM posts 
        JOIN users ON posts.author_id = users.id 
        WHERE posts.id = ?
    ''', (post_id,)).fetchone()
    
    comments = db.execute('''
        SELECT comments.*, users.username 
        FROM comments 
        JOIN users ON comments.user_id = users.id 
        WHERE comments.post_id = ?
        ORDER BY comments.created_at DESC
    ''', (post_id,)).fetchall()
    db.close()
    
    return render_template('blog_post.html', post=post, comments=comments)

@app.route('/blog/create', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        db = get_db()
        # VULNERABLE: Stored XSS - content not sanitized
        db.execute(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            (title, content, session['user_id'])
        )
        db.commit()
        db.close()
        
        flash('Post created!', 'success')
        return redirect(url_for('blog_list'))
    
    return render_template('create_post.html')

@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    content = request.form['content']
    
    db = get_db()
    # VULNERABLE: Stored XSS in comments
    db.execute(
        "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
        (post_id, session['user_id'], content)
    )
    db.commit()
    db.close()
    
    flash('Comment added!', 'success')
    return redirect(url_for('blog_post', post_id=post_id))

@app.route('/blog/search')
def search_posts():
    query = request.args.get('q', '')
    
    db = get_db()
    # VULNERABLE: SQL Injection in search
    sql = f"SELECT * FROM posts WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
    posts = db.execute(sql).fetchall()
    db.close()
    
    # VULNERABLE: Reflected XSS in search results
    return render_template('search_results.html', posts=posts, query=query)

# ======================
# SHOP FEATURES
# ======================

@app.route('/shop')
def shop():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    db.close()
    
    return render_template('shop.html', products=products)

@app.route('/shop/<int:product_id>')
def product_detail(product_id):
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    db.close()
    
    return render_template('product_detail.html', product=product)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    
    # VULNERABLE: Price manipulation - price comes from client
    price = float(request.form['price'])
    total = price * int(quantity)
    
    db = get_db()
    db.execute(
        "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)",
        (session['user_id'], product_id, quantity, total)
    )
    db.commit()
    db.close()
    
    flash(f'Order placed! Total: ${total:.2f}', 'success')
    return redirect(url_for('my_orders'))

@app.route('/orders')
def my_orders():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    db = get_db()
    orders = db.execute('''
        SELECT orders.*, products.name, products.description 
        FROM orders 
        JOIN products ON orders.product_id = products.id 
        WHERE orders.user_id = ?
        ORDER BY orders.created_at DESC
    ''', (session['user_id'],)).fetchall()
    db.close()
    
    return render_template('my_orders.html', orders=orders)

@app.route('/orders/<int:order_id>')
def view_order(order_id):
    # VULNERABLE: IDOR - anyone can view any order
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    db = get_db()
    order = db.execute('''
        SELECT orders.*, products.name, products.description, users.username 
        FROM orders 
        JOIN products ON orders.product_id = products.id 
        JOIN users ON orders.user_id = users.id 
        WHERE orders.id = ?
    ''', (order_id,)).fetchone()
    db.close()
    
    return render_template('view_order.html', order=order)

# ======================
# FILE UPLOAD
# ======================

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(request.url)
        
        # VULNERABLE: No file type validation, no filename sanitization
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Update user's profile picture
        db = get_db()
        db.execute("UPDATE users SET profile_picture = ? WHERE id = ?", 
                  (filename, session['user_id']))
        db.commit()
        db.close()
        
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('view_profile', user_id=session['user_id']))
    
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # VULNERABLE: Path traversal
    return send_from_directory('static/uploads', filename)

# ======================
# ADMIN PANEL
# ======================

@app.route('/admin')
def admin_dashboard():
    # VULNERABLE: Weak access control - only checks session variable
    if not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    user_count = db.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
    post_count = db.execute("SELECT COUNT(*) as count FROM posts").fetchone()['count']
    order_count = db.execute("SELECT COUNT(*) as count FROM orders").fetchone()['count']
    db.close()
    
    return render_template('admin/dashboard.html', 
                         user_count=user_count,
                         post_count=post_count,
                         order_count=order_count)

@app.route('/admin/users')
def admin_users():
    if not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    db.close()
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>')
def admin_delete_user(user_id):
    # VULNERABLE: No CSRF protection, no confirmation
    if not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    db.close()
    
    flash('User deleted!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/backup', methods=['POST'])
def admin_backup():
    if not session.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403
    
    filename = request.form.get('filename', 'backup.sql')
    
    # VULNERABLE: Command Injection
    command = f"sqlite3 vuln_web.db .dump > static/backup/{filename}"
    os.system(command)
    
    return jsonify({'success': True, 'message': 'Backup created!'})

# ======================
# API ENDPOINTS
# ======================

@app.route('/api/users')
def api_users():
    # VULNERABLE: No authentication, exposes passwords
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    db.close()
    
    return jsonify([dict(user) for user in users])

@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    # VULNERABLE: IDOR, exposes sensitive data
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

# ======================
# ERROR HANDLERS
# ======================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_error(e):
    # VULNERABLE: Exposes full stack trace
    import traceback
    return f"<h1>Error</h1><pre>{str(e)}\n\n{traceback.format_exc()}</pre>", 500
