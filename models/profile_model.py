"""Profile Model for Student, Teacher, and Admin profiles"""

def create_profile(cursor, user_id, role, name, phone=None, email=None, photo_path=None, **kwargs):
    """
    Create or update profile based on role
    Additional kwargs:
    - Student: register_number, department, course_details
    - Teacher: department, posting
    - Admin: department, designation
    """
    if role == 'student':
        cursor.execute("""
            INSERT INTO student_profiles (user_id, name, phone, email, register_number, department, course_details, photo_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            name=%s, phone=%s, email=%s, register_number=%s, department=%s, course_details=%s, photo_path=%s
        """, (user_id, name, phone, email, kwargs.get('register_number'), kwargs.get('department'), 
              kwargs.get('course_details'), photo_path, name, phone, email, 
              kwargs.get('register_number'), kwargs.get('department'), kwargs.get('course_details'), photo_path))
    
    elif role == 'teacher':
        cursor.execute("""
            INSERT INTO teacher_profiles (user_id, name, phone, email, department, posting, photo_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            name=%s, phone=%s, email=%s, department=%s, posting=%s, photo_path=%s
        """, (user_id, name, phone, email, kwargs.get('department'), kwargs.get('posting'), photo_path,
              name, phone, email, kwargs.get('department'), kwargs.get('posting'), photo_path))
    
    elif role == 'admin':
        cursor.execute("""
            INSERT INTO admin_profiles (user_id, name, phone, email, department, designation, photo_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            name=%s, phone=%s, email=%s, department=%s, designation=%s, photo_path=%s
        """, (user_id, name, phone, email, kwargs.get('department'), kwargs.get('designation'), photo_path,
              name, phone, email, kwargs.get('department'), kwargs.get('designation'), photo_path))


def get_profile(cursor, user_id, role):
    """Retrieve profile details based on role"""
    if role == 'student':
        cursor.execute("SELECT * FROM student_profiles WHERE user_id=%s", (user_id,))
    elif role == 'teacher':
        cursor.execute("SELECT * FROM teacher_profiles WHERE user_id=%s", (user_id,))
    elif role == 'admin':
        cursor.execute("SELECT * FROM admin_profiles WHERE user_id=%s", (user_id,))
    
    return cursor.fetchone()


def update_profile_photo(cursor, user_id, role, photo_path):
    """Update profile photo path"""
    if role == 'student':
        cursor.execute("UPDATE student_profiles SET photo_path=%s WHERE user_id=%s", (photo_path, user_id))
    elif role == 'teacher':
        cursor.execute("UPDATE teacher_profiles SET photo_path=%s WHERE user_id=%s", (photo_path, user_id))
    elif role == 'admin':
        cursor.execute("UPDATE admin_profiles SET photo_path=%s WHERE user_id=%s", (photo_path, user_id))
