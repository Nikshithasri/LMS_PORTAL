"""
Insert test data into LMS database
"""
import pymysql
from config import Config

def insert_test_data():
    """Insert sample users and courses"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Insert courses
        courses = [
            ('Python Programming', 'CSE101'),
            ('Web Development', 'CSE102'),
            ('Database Management', 'CSE103'),
        ]
        
        for course_name, course_code in courses:
            cursor.execute(
                "INSERT IGNORE INTO courses (course_name, course_code) VALUES (%s, %s)",
                (course_name, course_code)
            )
        
        # Get course IDs
        cursor.execute("SELECT course_id FROM courses WHERE course_code = 'CSE101'")
        python_course_id = cursor.fetchone()[0]
        
        # Insert users
        users = [
            ('Nikshitha', 'student@lms.com', 'password123', 'student', python_course_id),
            ('John Teacher', 'teacher@lms.com', '12345678', 'teacher', None),
            ('Admin User', 'admin@lms.com', '12345678', 'admin', None),
        ]
        
        for name, email, password, role, course_id in users:
            cursor.execute(
                "INSERT IGNORE INTO users (name, email, password, role, course_id) VALUES (%s, %s, %s, %s, %s)",
                (name, email, password, role, course_id)
            )
        
        connection.commit()
        print("✓ Test data inserted successfully!")
        print("\nTest Credentials:")
        print("=" * 50)
        print("Student Login:")
        print("  Email: student@lms.com")
        print("  Password: password123")
        print("\nTeacher Login:")
        print("  Email: teacher@lms.com")
        print("  Password: 12345678")
        print("\nAdmin Login:")
        print("  Email: admin@lms.com")
        print("  Password: 12345678")
        print("=" * 50)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"✗ Error inserting data: {e}")

if __name__ == "__main__":
    insert_test_data()
