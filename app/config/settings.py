import os
from pathlib import Path

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # File handling
    UPLOAD_FOLDER = Path('data/uploaded_resumes')
    JOB_DESCRIPTIONS_FOLDER = Path('data/job_descriptions')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///rsart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 3600
    
    # Logging
    LOGGING_CONFIG = Path('app/config/logging.conf')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = Path('logs/rsart.log')
    
    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Resume processing
    TOP_CANDIDATES_COUNT = 10
    SIMILARITY_THRESHOLD = 0.1

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

def get_config(config_name):
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return config_map.get(config_name, DevelopmentConfig)