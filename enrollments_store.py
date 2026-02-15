"""
Simple file-based storage for course enrollments
"""
import json
import os
from datetime import datetime

ENROLLMENTS_FILE = 'enrollments_data.json'

def load_enrollments():
    """Load enrollments from JSON file"""
    if os.path.exists(ENROLLMENTS_FILE):
        try:
            with open(ENROLLMENTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_enrollments(enrollments):
    """Save enrollments to JSON file"""
    with open(ENROLLMENTS_FILE, 'w') as f:
        json.dump(enrollments, f, indent=2)

def add_enrollment(student_id, student_name, course_name, enrollment_date=None):
    """Add a new enrollment"""
    enrollments = load_enrollments()
    
    enrollment = {
        'id': len(enrollments) + 1,
        'student_id': student_id,
        'student_name': student_name,
        'course_name': course_name,
        'enrollment_date': enrollment_date or datetime.now().strftime('%Y-%m-%d'),
        'status': 'Active'
    }
    
    enrollments.append(enrollment)
    save_enrollments(enrollments)
    return enrollment

def get_course_enrollments(course_name):
    """Get all students enrolled in a course"""
    enrollments = load_enrollments()
    return [e for e in enrollments if e['course_name'].lower() == course_name.lower()]

def get_student_enrollments(student_id):
    """Get all courses a student is enrolled in"""
    enrollments = load_enrollments()
    return [e for e in enrollments if e['student_id'] == student_id]

def get_enrollment_count(course_name):
    """Get total students enrolled in a course"""
    return len(get_course_enrollments(course_name))

def get_all_courses():
    """Get all unique courses with enrollment counts"""
    enrollments = load_enrollments()
    courses_dict = {}
    
    for enrollment in enrollments:
        course_name = enrollment['course_name']
        if course_name not in courses_dict:
            courses_dict[course_name] = {
                'name': course_name,
                'students_count': 0
            }
        courses_dict[course_name]['students_count'] += 1
    
    return list(courses_dict.values())

# Initialize sample data
def init_sample_data():
    """Initialize with sample enrollment data"""
    if not os.path.exists(ENROLLMENTS_FILE):
        sample_enrollments = [
            {
                'id': 1,
                'student_id': 'S001',
                'student_name': 'John Doe',
                'course_name': 'Python Programming',
                'enrollment_date': '2024-01-15',
                'status': 'Active'
            },
            {
                'id': 2,
                'student_id': 'S002',
                'student_name': 'Jane Smith',
                'course_name': 'Python Programming',
                'enrollment_date': '2024-01-16',
                'status': 'Active'
            },
            {
                'id': 3,
                'student_id': 'S003',
                'student_name': 'Mike Johnson',
                'course_name': 'Web Development',
                'enrollment_date': '2024-01-17',
                'status': 'Active'
            },
            {
                'id': 4,
                'student_id': 'S004',
                'student_name': 'Sarah Williams',
                'course_name': 'Python Programming',
                'enrollment_date': '2024-01-18',
                'status': 'Active'
            },
            {
                'id': 5,
                'student_id': 'S005',
                'student_name': 'Robert Brown',
                'course_name': 'Data Science',
                'enrollment_date': '2024-01-19',
                'status': 'Active'
            }
        ]
        save_enrollments(sample_enrollments)

# Initialize on import
init_sample_data()
