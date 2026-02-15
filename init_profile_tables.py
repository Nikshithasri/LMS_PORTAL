"""
Database initialization script to create profile tables
Run this script to set up the profile tables in your MySQL/PostgreSQL database
"""

import pymysql
from config import Config

def init_profile_tables():
    """Create profile tables for student, teacher, and admin"""
    
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    cursor = connection.cursor()
    
    try:
        # Student Profile Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                register_number VARCHAR(50),
                department VARCHAR(100),
                course_details VARCHAR(255),
                phone VARCHAR(20),
                email VARCHAR(100),
                photo_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Student profiles table created")
        
        # Teacher Profile Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                posting VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                photo_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Teacher profiles table created")
        
        # Admin Profile Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                designation VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                photo_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Admin profiles table created")
        
        connection.commit()
        print("\n✅ All profile tables initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    init_profile_tables()
