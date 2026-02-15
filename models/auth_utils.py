"""Authentication utilities for secure password handling"""
import bcrypt
from config import Config


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    if not password or len(password) < Config.MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {Config.MIN_PASSWORD_LENGTH} characters long")
    
    salt = bcrypt.gensalt(rounds=Config.BCRYPT_LOG_ROUNDS)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < Config.MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {Config.MIN_PASSWORD_LENGTH} characters long"
    
    if len(password) > 128:
        return False, "Password is too long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    # Strong password check
    strength_score = sum([has_upper, has_lower, has_digit, has_special])
    
    if strength_score < 3:
        return False, "Password must contain uppercase, lowercase, numbers, and special characters"
    
    return True, ""
