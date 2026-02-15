from flask import Blueprint, request, jsonify

api_nm = Blueprint('api_nm', __name__, url_prefix='/api')

# -----------------------------
# 1) NM → LMS : Student Sync
# -----------------------------
@api_nm.route('/api_nm/student-sync', methods=['POST'])
def student_sync():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    cur = mysql.connection.cursor()

    # Check if user already exists
    cur.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE users
            SET name=%s, email=%s, course_id=%s
            WHERE user_id=%s
        """, (name, email, course_id, user_id))
    else:
        cur.execute("""
            INSERT INTO users (name, email, user_id, password, role, course_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, user_id, 'nm_default', 'student', course_id))

    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "student synced"}), 200


# -----------------------------
# 2) NM → LMS : Course Sync
# -----------------------------
@api_nm.route('/api_nm/course-sync', methods=['POST'])
def course_sync():
    data = request.get_json()

    course_id = data.get('course_id')
    course_name = data.get('course_name')

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM courses WHERE course_id=%s", (course_id,))
    existing = cur.fetchone()

    if existing:
        cur.execute("""
            UPDATE courses
            SET course_name=%s
            WHERE course_id=%s
        """, (course_name, course_id))
    else:
        cur.execute("""
            INSERT INTO courses (course_id, course_name)
            VALUES (%s, %s)
        """, (course_id, course_name))

    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "course synced"}), 200


# ------------------------------------------------
# 3) LMS → NM : Get All Students (TEST API)
# ------------------------------------------------
@api_nm.route('/api_nm/get_students', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT name, email, user_id, course_id
        FROM users
        WHERE role='student'
    """)
    rows = cur.fetchall()
    cur.close()

    students = []
    for row in rows:
        students.append({
            "name": row[0],
            "email": row[1],
            "user_id": row[2],
            "course_id": row[3]
        })

    return jsonify(students), 200


# ------------------------------------------------
# 4) LMS → NM : Get All Courses (TEST API)
# ------------------------------------------------
@api_nm.route('/api_nm/get_courses', methods=['GET'])
def get_courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT course_id, course_name FROM courses")
    rows = cur.fetchall()
    cur.close()

    courses = []
    for row in rows:
        courses.append({
            "course_id": row[0],
            "course_name": row[1]
        })

    return jsonify(courses), 200


# ----------------------------------------------------------------
# 5) LMS → NM : Get Materials for a Course (TEST API)
# ----------------------------------------------------------------
@api_nm.route('/api_nm/get_materials/<course_id>', methods=['GET'])
def get_materials(course_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT title, file_path
        FROM materials
        WHERE course_id=%s
    """, (course_id,))
    rows = cur.fetchall()
    cur.close()

    materials = []
    for row in rows:
        materials.append({
            "title": row[0],
            "file_url": row[1]
        })

    return jsonify(materials), 200
