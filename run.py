from app import app, init_db

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # VULNERABLE: Debug mode and accessible to all
    app.run(host='0.0.0.0', port=5000, debug=True)
