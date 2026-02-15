"""
Reset and fix database with correct credentials
"""
import pymysql
from config import Config

def reset_and_fix():
    """Complete reset and fresh data insertion"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("🔄 Clearing old data...")
        # Clear all data
        cursor.execute("DELETE FROM submissions")
        cursor.execute("DELETE FROM enrollments")
        cursor.execute("DELETE FROM materials")
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM courses")
        connection.commit()
        print("✓ Old data cleared")
        
        print("\n📝 Inserting fresh courses...")
        # Insert courses
        courses_data = [
            ('Python Programming', 'CSE101', 'Learn Python from basics to advanced'),
            ('Web Development', 'CSE102', 'HTML, CSS, JavaScript and Web frameworks'),
            ('Database Management', 'CSE103', 'SQL and Database Design'),
        ]
        
        for course_name, course_code, desc in courses_data:
            cursor.execute(
                "INSERT INTO courses (course_name, course_code, description) VALUES (%s, %s, %s)",
                (course_name, course_code, desc)
            )
        connection.commit()
        print("✓ Courses inserted")
        
        # Get course IDs
        cursor.execute("SELECT course_id FROM courses WHERE course_code = 'CSE101'")
        python_course_id = cursor.fetchone()[0]
        
        print("\n👥 Inserting fresh users...")
        # Insert users with exact credentials
        users_data = [
            ('Nikshitha', 'student@lms.com', 'password123', 'student', python_course_id),
            ('John Teacher', 'teacher@lms.com', '12345678', 'teacher', None),
            ('Admin User', 'admin@lms.com', '12345678', 'admin', None),
        ]
        
        for name, email, password, role, course_id in users_data:
            cursor.execute(
                "INSERT INTO users (name, email, password, role, course_id) VALUES (%s, %s, %s, %s, %s)",
                (name, email, password, role, course_id)
            )
        connection.commit()
        print("✓ Users inserted")
        
        # Verify data
        print("\n✅ Verifying inserted data...")
        cursor.execute("SELECT user_id, name, email, password, role FROM users")
        users = cursor.fetchall()
        
        for user in users:
            print(f"   ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Pass: {user[3]}, Role: {user[4]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ DATABASE RESET COMPLETE!")
        print("="*60)
        print("\n🔐 LOGIN CREDENTIALS:\n")
        print("Student:")
        print("  📧 Email: student@lms.com")
        print("  🔒 Password: password123\n")
        print("Teacher:")
        print("  📧 Email: teacher@lms.com")
        print("  🔒 Password: 12345678\n")
        print("Admin:")
        print("  📧 Email: admin@lms.com")
        print("  🔒 Password: 12345678\n")
        print("="*60)
        print("\n✨ You can now login with these credentials!")
        print("🌐 Visit: http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_and_fix()
