"""User model for database operations"""
from datetime import datetime
from models.auth_utils import hash_password, verify_password


def create_user(cursor, email: str, password: str, name: str, role: str) -> dict:
    """
    Create a new user in the database
    
    Args:
        cursor: MySQL cursor
        email: User email (unique)
        password: Plain text password (will be hashed)
        name: User's full name
        role: User role (student/teacher/admin)
        
    Returns:
        Dictionary with user data or error
    """
    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return {"success": False, "message": "Email already registered"}
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Insert user
        cursor.execute(
            "INSERT INTO users (email, password, name, role, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (email, hashed_password, name, role, datetime.now(), datetime.now())
        )
        
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id, "message": "User created successfully"}
    
    except Exception as e:
        print(f"Error creating user: {e}")
        return {"success": False, "message": str(e)}


def authenticate_user(cursor, email: str, password: str) -> dict:
    """
    Authenticate user with email and password
    
    Args:
        cursor: MySQL cursor
        email: User email
        password: Plain text password
        
    Returns:
        Dictionary with user data if successful, error otherwise
    """
    try:
        cursor.execute(
            "SELECT id, email, password, name, role FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        
        if not user:
            return {"success": False, "message": "Invalid email or password"}
        
        if not verify_password(password, user['password']):
            return {"success": False, "message": "Invalid email or password"}
        
        return {
            "success": True,
            "user_id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "role": user['role']
        }
    
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return {"success": False, "message": "Authentication failed"}


def get_user(cursor, user_id: int) -> dict:
    """Get user by ID"""
    try:
        cursor.execute(
            "SELECT id, email, name, role, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def get_users_by_role(cursor, role: str, limit: int = None) -> list:
    """Get all users by role"""
    try:
        if limit:
            cursor.execute(
                "SELECT id, email, name, role, created_at FROM users WHERE role = %s LIMIT %s",
                (role, limit)
            )
        else:
            cursor.execute(
                "SELECT id, email, name, role, created_at FROM users WHERE role = %s",
                (role,)
            )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting users by role: {e}")
        return []


def get_user(cursor, user_id: int) -> dict:
    """Get user by ID"""
    try:
        cursor.execute(
            "SELECT id, email, name, role, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def update_user(cursor, user_id: int, name: str = None, email: str = None) -> dict:
    """Update user information"""
    try:
        if name:
            cursor.execute(
                "UPDATE users SET name = %s, updated_at = %s WHERE id = %s",
                (name, datetime.now(), user_id)
            )
        
        if email:
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))
            if cursor.fetchone():
                return {"success": False, "message": "Email already in use"}
            
            cursor.execute(
                "UPDATE users SET email = %s, updated_at = %s WHERE id = %s",
                (email, datetime.now(), user_id)
            )
        
        return {"success": True, "message": "User updated successfully"}
    
    except Exception as e:
        print(f"Error updating user: {e}")
        return {"success": False, "message": str(e)}


def delete_user(cursor, user_id: int) -> dict:
    """Delete user from database"""
    try:
        # Delete related records first
        cursor.execute("DELETE FROM study_materials WHERE uploaded_by = %s", (user_id,))
        cursor.execute("DELETE FROM student_profiles WHERE user_id = %s AND role = %s", (user_id, 'student'))
        cursor.execute("DELETE FROM teacher_profiles WHERE user_id = %s AND role = %s", (user_id, 'teacher'))
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        return {"success": True, "message": "User deleted successfully"}
    
    except Exception as e:
        print(f"Error deleting user: {e}")
        return {"success": False, "message": str(e)}
