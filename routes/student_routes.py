"""Student routes for dashboard, material viewing, and profile"""
from flask import Blueprint, render_template, session, request, jsonify, url_for, send_file
from werkzeug.utils import secure_filename
import os
import pymysql
from pymysql.cursors import DictCursor
from config import Config
from models.material_model import get_all_materials
from routes.auth_routes import login_required, role_required
from datetime import datetime

student = Blueprint('student', __name__, url_prefix='/student')


@student.route('/profile-test', methods=['GET', 'POST'])
def profile_test():
    """Student profile page - Test version without authentication"""
    try:
        if request.method == 'GET':
            return render_template('student_profile.html', 
                                 profile=None, 
                                 user_email='student@lms.com',
                                 user_name='Student User',
                                 enrollments=[])
        
        # POST request - just return success for testing
        return jsonify({'success': True, 'message': 'Profile would be updated successfully'})
    
    except Exception as e:
        print(f"Error in student profile test: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def allowed_file(filename):
    """Check if file is an allowed profile photo"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.PROFILE_ALLOWED_EXTENSIONS


@student.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    """Student dashboard showing approved study materials"""
    try:
        # Ensure session is persistent
        session.permanent = True
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        cursor = connection.cursor()
        
        # Get all approved materials
        cursor.execute(
            """SELECT id, title, subject, description, file_path, upload_date, download_count, 
                      CONCAT(u.name) as uploader_name
               FROM study_materials m
               JOIN users u ON m.uploaded_by = u.id
               WHERE m.approval_status = 'approved' 
               ORDER BY m.upload_date DESC""",
            ()
        )
        materials = cursor.fetchall()
        
        # Get subjects for filtering
        cursor.execute(
            "SELECT DISTINCT subject FROM study_materials WHERE approval_status = 'approved' ORDER BY subject"
        )
        subjects = cursor.fetchall()
        
        # Get statistics
        cursor.execute(
            "SELECT COUNT(*) as total FROM study_materials WHERE approval_status = 'approved'"
        )
        total_materials = cursor.fetchone()['total']
        
        cursor.execute(
            "SELECT COUNT(DISTINCT subject) as total FROM study_materials WHERE approval_status = 'approved'"
        )
        total_subjects = cursor.fetchone()['total']
        
        cursor.close()
        connection.close()
        
        return render_template('student_dashboard.html',
                             user_name=user_name,
                             materials=materials,
                             subjects=subjects,
                             total_materials=total_materials,
                             total_subjects=total_subjects)
    
    except Exception as e:
        print(f"Error loading student dashboard: {e}")
        return render_template('error.html', message='Error loading dashboard'), 500


@student.route('/materials/filter')
@login_required
@role_required('student')
def filter_materials():
    """Filter materials by subject"""
    try:
        subject = request.args.get('subject', '').strip()
        
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        cursor = connection.cursor()
        
        if subject:
            cursor.execute(
                """SELECT id, title, subject, description, file_path, upload_date, download_count, 
                          CONCAT(u.name) as uploader_name
                   FROM study_materials m
                   JOIN users u ON m.uploaded_by = u.id
                   WHERE m.approval_status = 'approved' AND m.subject = %s
                   ORDER BY m.upload_date DESC""",
                (subject,)
            )
        else:
            cursor.execute(
                """SELECT id, title, subject, description, file_path, upload_date, download_count,
                          CONCAT(u.name) as uploader_name
                   FROM study_materials m
                   JOIN users u ON m.uploaded_by = u.id
                   WHERE m.approval_status = 'approved'
                   ORDER BY m.upload_date DESC"""
            )
        
        materials = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return render_template('student_materials_list.html', materials=materials, selected_subject=subject)
    
    except Exception as e:
        print(f"Error filtering materials: {e}")
        return render_template('error.html', message='Error filtering materials'), 500


@student.route('/materials/<int:material_id>/download')
@login_required
@role_required('student')
def download_material(material_id):
    """Download material"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        cursor = connection.cursor()
        
        # Get material info
        cursor.execute(
            "SELECT file_path, title FROM study_materials WHERE id = %s AND approval_status = 'approved'",
            (material_id,)
        )
        material = cursor.fetchone()
        
        if not material:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Material not found'}), 404
        
        # Increment download count
        cursor.execute(
            "UPDATE study_materials SET download_count = download_count + 1 WHERE id = %s",
            (material_id,)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        # Send file
        file_path = material['file_path']
        if file_path.startswith('/'):
            actual_path = '.' + file_path
        else:
            actual_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
        
        if not os.path.exists(actual_path):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        return send_file(actual_path, as_attachment=True, download_name=material['title'])
    
    except Exception as e:
        print(f"Error downloading material: {e}")
        return jsonify({'success': False, 'message': 'Download failed'}), 500


@student.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('student')
def profile():
    """Student profile page"""
    try:
        # Ensure session is persistent
        session.permanent = True
        user_id = session.get('user_id')
        user_email = session.get('user_email', 'student@test.com')
        user_name = session.get('user_name', 'Student User')
        
        # If no user_id in session, provide defaults for testing
        if not user_id:
            user_id = 999
            session['user_id'] = user_id
            session['user_role'] = 'student'
        
        if request.method == 'GET':
            # For testing without full database setup
            profile = {
                'name': user_name,
                'email': user_email,
                'phone': '9000000000',
                'register_number': 'STU001',
                'department': 'Computer Science',
                'course_details': 'B.Tech CSE',
                'photo_path': None
            }
            
            enrollments = []
            
            return render_template('student_profile.html', 
                                 profile=profile, 
                                 user_email=user_email,
                                 user_name=user_name,
                                 enrollments=enrollments)
        
        # POST request - update profile
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        cursor = connection.cursor()
        
        # Handle photo upload
        photo_path = None
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and file.filename != '' and allowed_file(file.filename):
                os.makedirs(Config.PROFILE_PHOTOS_FOLDER, exist_ok=True)
                filename = secure_filename(f"student_{user_id}_{file.filename}")
                filepath = os.path.join(Config.PROFILE_PHOTOS_FOLDER, filename)
                file.save(filepath)
                photo_path = f"/static/uploads/profiles/{filename}"
        
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        register_number = request.form.get('register_number', '').strip()
        department = request.form.get('department', '').strip()
        course_details = request.form.get('course_details', '').strip()
        
        if not all([name, email, phone, register_number, department, course_details]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Check if profile exists
        cursor.execute("SELECT id FROM student_profiles WHERE user_id = %s", (user_id,))
        existing_profile = cursor.fetchone()
        
        try:
            if existing_profile:
                # Update existing profile
                query = """UPDATE student_profiles SET name = %s, email = %s, phone = %s, 
                           register_number = %s, department = %s, course_details = %s"""
                params = [name, email, phone, register_number, department, course_details]
                
                if photo_path:
                    query += ", profile_photo = %s"
                    params.append(photo_path)
                
                query += " WHERE user_id = %s"
                params.append(user_id)
                
                cursor.execute(query, params)
            else:
                # Create new profile
                cursor.execute(
                    """INSERT INTO student_profiles (user_id, role, name, email, phone, register_number, 
                       department, course_details, profile_photo)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, 'student', name, email, phone, register_number, department, course_details, photo_path)
                )
            
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        except Exception as e:
            connection.rollback()
            print(f"Error updating student profile: {e}")
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': str(e)}), 500
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    except Exception as e:
        print(f"Error in student profile: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
