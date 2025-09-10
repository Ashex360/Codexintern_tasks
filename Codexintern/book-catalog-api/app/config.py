import os
from dotenv import load_dotenv

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration class with common settings"""
    
    # Secret key for session management and security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Disable track modifications to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Secret Key for authentication (if needed later)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    
    # API settings
    JSON_SORT_KEYS = False  # Keep JSON response order as defined
    JSONIFY_PRETTYPRINT_REGULAR = True  # Pretty print JSON in development


class DevelopmentConfig(Config):
    """Development specific configuration"""
    
    DEBUG = True
    ENV = 'development'
    
    # Development database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app_dev.db')


class TestingConfig(Config):
    """Testing specific configuration"""
    
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF protection in tests
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production specific configuration"""
    
    DEBUG = False
    ENV = 'production'
    
    # Production database - should be set via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app_prod.db')
    
    # Ensure secret keys are set in production
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY must be set in production environment")
    
    if not os.environ.get('JWT_SECRET_KEY'):
        raise ValueError("JWT_SECRET_KEY must be set in production environment")


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get the appropriate configuration based on environment"""
    env = os.environ.get('FLASK_ENV') or 'development'
    return config.get(env, config['default'])