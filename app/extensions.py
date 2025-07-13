"""
Flask Extensions

This module initializes and configures all Flask extensions used by the application.
Extensions are initialized here but configured in the application factory.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

# Initialize extensions
# These will be configured in the application factory (create_app)
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def init_extensions(app):
    """
    Initialize all Flask extensions with the application instance.
    
    Args:
        app: Flask application instance
    """
    # Initialize SQLAlchemy
    try:
        db.init_app(app)
        app.logger.info("Database initialized successfully")
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
        # In development, fall back to SQLite if PostgreSQL fails
        if app.config.get('FLASK_ENV') == 'development':
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fallback.db'
            db.init_app(app)
            app.logger.warning("Fell back to SQLite database")
        else:
            raise
    
    # Initialize Flask-Migrate
    migrate.init_app(app, db)
    
    # Initialize Flask-Caching
    try:
        cache.init_app(app)
        app.logger.info("Cache initialized successfully")
    except Exception as e:
        app.logger.warning(f"Cache initialization failed, using simple cache: {e}")
        app.config['CACHE_TYPE'] = 'simple'
        cache.init_app(app)
    
    # Configure cache with app context
    with app.app_context():
        try:
            cache.clear()  # Clear any existing cache on startup
        except Exception as e:
            app.logger.warning(f"Could not clear cache on startup: {e}")