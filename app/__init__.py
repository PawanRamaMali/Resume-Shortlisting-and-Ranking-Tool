from flask import Flask
from app.config.settings import get_config
from app.extensions import db, migrate, cache
from app.controllers import register_blueprints
from app.utils.error_handlers import register_error_handlers
import logging.config

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    
    # Setup logging
    logging.config.fileConfig(app.config['LOGGING_CONFIG'])
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app