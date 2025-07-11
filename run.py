import os
from app import create_app
from app.extensions import db

# Get environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(config_name)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = config_name == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    )
# This script initializes the Flask application and creates the necessary database tables.
# It also sets the application to run on a specified port and in debug mode if in development.