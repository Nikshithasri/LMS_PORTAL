"""
Database schema setup script for Educational Management System
This creates all necessary tables for the LMS application
"""

import mysql.connector
from config import Config
from datetime import datetime

def create_database():
    """Create the main database"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        
        # Drop existing database if it exists
        cursor.execute(f"DROP DATABASE IF EXISTS {Config.MYSQL_DB}")
        
        # Create database
        cursor.execute(f"CREATE DATABASE {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ Database '{Config.MYSQL_DB}' created successfully")
        
        cursor.close()
        connection.close()
    
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        raise


def create_tables():
    """Create all tables in the database"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                role ENUM('student', 'teacher', 'admin') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                INDEX idx_email (email),
                INDEX idx_role (role)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Users table created")
        
        # Student Profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                role VARCHAR(50) DEFAULT 'student',
                register_number VARCHAR(100) UNIQUE,
                department VARCHAR(255),
                course_details VARCHAR(255),
                phone VARCHAR(20),
                profile_photo VARCHAR(500),
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_register_number (register_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Student Profiles table created")
        
        # Teacher Profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                role VARCHAR(50) DEFAULT 'teacher',
                department VARCHAR(255),
                specialization VARCHAR(255),
                phone VARCHAR(20),
                profile_photo VARCHAR(500),
                bio TEXT,
                experience_years INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Teacher Profiles table created")
        
        # Study Materials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_materials (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                subject VARCHAR(255) NOT NULL,
                description TEXT,
                file_path VARCHAR(500) NOT NULL,
                file_type VARCHAR(50),
                uploaded_by INT NOT NULL,
                approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                download_count INT DEFAULT 0,
                approved_by INT,
                approval_date TIMESTAMP NULL,
                FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_subject (subject),
                INDEX idx_uploaded_by (uploaded_by),
                INDEX idx_approval_status (approval_status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Study Materials table created")
        
        # Audit Log table (for admin tracking)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                action VARCHAR(255) NOT NULL,
                entity_type VARCHAR(100),
                entity_id INT,
                old_value TEXT,
                new_value TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_user_id (user_id),
                INDEX idx_action (action),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Audit Logs table created")
        
        # Statistics table (for analytics)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                metric_name VARCHAR(255) NOT NULL,
                metric_value INT DEFAULT 0,
                metric_date DATE,
                UNIQUE KEY unique_metric_date (metric_name, metric_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Statistics table created")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✓ All tables created successfully!")
    
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        raise


def insert_admin_user():
    """Insert default admin user"""
    try:
        from models.auth_utils import hash_password
        
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = connection.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", ('admin@aves.edu',))
        if cursor.fetchone():
            print("Admin user already exists")
            cursor.close()
            connection.close()
            return
        
        # Insert admin user
        admin_password = hash_password('Admin@123456')
        cursor.execute(
            """INSERT INTO users (email, password, name, role, created_at, updated_at) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            ('admin@aves.edu', admin_password, 'System Administrator', 'admin', datetime.now(), datetime.now())
        )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✓ Default admin user created (Email: admin@aves.edu, Password: Admin@123456)")
        print("  ⚠️  IMPORTANT: Change this password on first login!")
    
    except Exception as e:
        print(f"✗ Error inserting admin user: {e}")
        raise


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Educational Management System - Database Setup")
    print("="*60 + "\n")
    
    print("Step 1: Creating database...")
    create_database()
    
    print("\nStep 2: Creating tables...")
    create_tables()
    
    print("\nStep 3: Inserting default admin user...")
    insert_admin_user()
    
    print("\n" + "="*60)
    print("  Database setup completed successfully!")
    print("="*60 + "\n")
