"""
Configuration Module
Contains all configuration settings for the application
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Model settings
    MODEL_FOLDER = os.path.join(os.path.dirname(__file__), 'models')
    RANDOM_FOREST_MODEL = os.path.join(MODEL_FOLDER, 'random_forest_model.pkl')
    SVM_MODEL = os.path.join(MODEL_FOLDER, 'svm_model.pkl')
    DEFAULT_MODEL = 'random_forest'
    
    # ML settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    RISK_THRESHOLD = 50  # Marks threshold for at-risk classification
    
    # OpenAI settings (for GenAI chatbot)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
