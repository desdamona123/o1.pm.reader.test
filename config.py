# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback_secret_key')
    DEEPINFRA_API_KEY = os.environ.get('DEEPINFRA_API_KEY', '')
    STORAGE_MODE = os.environ.get('STORAGE_MODE', 'JSON')
    JSON_DATA_FILE = 'data.json'
    DISALLOWED_WORDS_FILE = 'disallowed_words.txt'
    MAX_STORY_WORDS = 300  # Hard limit to comply with PM-Level specification

    # Rate limiting
    RATELIMIT_DEFAULT = "5 per minute"  # Example default limit

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

def get_config():
    flask_env = os.environ.get('FLASK_ENV', 'development')
    if flask_env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()