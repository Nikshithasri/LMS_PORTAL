import os
from datetime import timedelta

class Config:
    """Production configuration for Educational Management System"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Geetha@77')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'lms_db')
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'materials')
    PROFILE_PHOTOS_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'profiles')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'avi', 'mov', 'docx', 'pptx'}
    PROFILE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Security
    MIN_PASSWORD_LENGTH = 8
    BCRYPT_LOG_ROUNDS = 12
