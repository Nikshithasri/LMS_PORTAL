"""
Database initialization script - creates all tables for LMS
Run this script once to set up the MySQL database
"""

import pymysql
from config import Config

def init_database():
    """Create all necessary tables for the LMS application"""
    
    # Connect to MySQL server
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset='utf8mb4'
    )
    
    cursor = connection.cursor()
    
    try:
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        print(f"✓ Database '{Config.MYSQL_DB}' created or already exists")
        
        # Select the database
        cursor.execute(f"USE {Config.MYSQL_DB}")
        
        # Create courses table FIRST (no dependencies)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                course_name VARCHAR(255) NOT NULL,
                course_code VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                teacher_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table 'courses' created or already exists")
        
        # Create users table (depends on courses)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'teacher', 'student') NOT NULL,
                course_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
            )
        """)
        print("✓ Table 'users' created or already exists")
        
        # Add teacher_id foreign key to courses
        try:
            cursor.execute("""
                ALTER TABLE courses ADD CONSTRAINT fk_teacher_id
                FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE SET NULL
            """)
        except pymysql.Error:
            pass  # Constraint may already exist
        
        # Create materials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                material_id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                file_path VARCHAR(500),
                file_type VARCHAR(50),
                uploaded_by INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                FOREIGN KEY (uploaded_by) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        print("✓ Table 'materials' created or already exists")
        
        # Create enrollments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                course_id INT NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                UNIQUE KEY unique_enrollment (student_id, course_id)
            )
        """)
        print("✓ Table 'enrollments' created or already exists")
        
        # Create submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                submission_id INT AUTO_INCREMENT PRIMARY KEY,
                material_id INT NOT NULL,
                student_id INT NOT NULL,
                file_path VARCHAR(500),
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (material_id) REFERENCES materials(material_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        print("✓ Table 'submissions' created or already exists")
        
        connection.commit()
        print("\n✓ Database initialization completed successfully!")
        
    except pymysql.Error as e:
        print(f"✗ Database error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    init_database()
