"""
Database utility functions for common operations
"""

from app import mysql
from flask import g

def get_db_connection():
    """Get database connection"""
    return mysql.connection

def get_cursor():
    """Get database cursor"""
    return mysql.connection.cursor()

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or list)
        fetch_one: If True, return one row
        fetch_all: If True, return all rows
    
    Returns:
        Query result or None
    """
    try:
        cursor = get_cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            mysql.connection.commit()
            return cursor.rowcount
            
    except Exception as e:
        print(f"Database error: {e}")
        mysql.connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def commit_transaction():
    """Commit database transaction"""
    try:
        mysql.connection.commit()
        return True
    except Exception as e:
        print(f"Commit error: {e}")
        mysql.connection.rollback()
        return False

def rollback_transaction():
    """Rollback database transaction"""
    try:
        mysql.connection.rollback()
        return True
    except Exception as e:
        print(f"Rollback error: {e}")
        return False
