"""Teacher routes for dashboard, material upload, and management"""
from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pymysql
from pymysql.cursors import DictCursor
from config import Config
from models.profile_model import create_profile, get_profile
from routes.auth_routes import login_required, role_required

teacher = Blueprint('teacher', __name__, url_prefix='/teacher')


@teacher.route('/profile-test', methods=['GET', 'POST'])
def profile_test():
    """Teacher profile page - Test version without authentication"""
    try:
        if request.method == 'GET':
            return render_template('teacher_profile.html', 
                                 profile=None, 
                                 user_email='teacher@lms.com',
                                 user_name='Teacher User',
                                 courses=[])
        
        # POST request - just return success for testing
        return jsonify({'success': True, 'message': 'Profile would be updated successfully'})
    
    except Exception as e:
        print(f"Error in teacher profile test: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def allowed_material_file(filename):
    """Check if file extension is allowed for material upload"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@teacher.route('/dashboard')
@login_required
@role_required('teacher')
def dashboard():
    """Teacher dashboard showing uploaded materials"""
    try:
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
        
        # Get materials uploaded by this teacher
        cursor.execute(
            """SELECT id, title, subject, description, file_path, approval_status, upload_date, download_count 
               FROM study_materials WHERE uploaded_by = %s ORDER BY upload_date DESC""",
            (user_id,)
        )
        materials = cursor.fetchall()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total FROM study_materials WHERE uploaded_by = %s", (user_id,))
        total_materials = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as pending FROM study_materials WHERE uploaded_by = %s AND approval_status = 'pending'", (user_id,))
        pending_materials = cursor.fetchone()['pending']
        
        cursor.execute("SELECT COUNT(*) as approved FROM study_materials WHERE uploaded_by = %s AND approval_status = 'approved'", (user_id,))
        approved_materials = cursor.fetchone()['approved']
        
        cursor.close()
        connection.close()
        
        return render_template('teacher_dashboard.html',
                             user_name=user_name,
                             materials=materials,
                             total_materials=total_materials,
                             pending_materials=pending_materials,
                             approved_materials=approved_materials)
    
    except Exception as e:
        print(f"Error loading teacher dashboard: {e}")
        return render_template('error.html', message='Error loading dashboard'), 500


@teacher.route('/upload', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def upload_material():
    """Upload study material"""
    if request.method == 'GET':
        return render_template('upload_material.html')
    
    try:
        from app import mysql
        
        user_id = session.get('user_id')
        
        # Get form data
        title = request.form.get('title', '').strip()
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        
        # Validation
        if not all([title, subject]):
            return jsonify({'success': False, 'message': 'Title and subject are required'}), 400
        
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not allowed_material_file(file.filename):
            return jsonify({'success': False, 'message': 'File type not allowed'}), 400
        
        # Create upload folder
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Save file
        filename = secure_filename(f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        file_path = f"/static/uploads/materials/{filename}"
        file_type = filename.rsplit('.', 1)[1].lower()
        
        cursor = mysql.connection.cursor()
        
        # Add material to database
        result = add_material(cursor, title, subject, description, file_path, user_id, 'pending')
        
        mysql.connection.commit()
        cursor.close()
        
        if result['success']:
            return jsonify({'success': True, 'message': 'Material uploaded successfully and pending approval'})
        else:
            return jsonify({'success': False, 'message': result['message']}), 500
    
    except Exception as e:
        print(f"Error uploading material: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@teacher.route('/edit/<int:material_id>', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def edit_material(material_id):
    """Edit material details"""
    try:
        from app import mysql
        
        user_id = session.get('user_id')
        cursor = mysql.connection.cursor()
        
        # Check if material belongs to current teacher
        cursor.execute("SELECT * FROM study_materials WHERE id = %s AND uploaded_by = %s", (material_id, user_id))
        material = cursor.fetchone()
        
        if not material:
            cursor.close()
            return jsonify({'success': False, 'message': 'Material not found'}), 404
        
        if request.method == 'GET':
            return render_template('edit_material.html', material=material)
        
        # POST request - update material
        title = request.form.get('title', '').strip()
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        
        if not all([title, subject]):
            return jsonify({'success': False, 'message': 'Title and subject are required'}), 400
        
        result = update_material(cursor, material_id, title=title, subject=subject, description=description)
        mysql.connection.commit()
        cursor.close()
        
        if result['success']:
            return jsonify({'success': True, 'message': 'Material updated successfully'})
        else:
            return jsonify({'success': False, 'message': result['message']}), 500
    
    except Exception as e:
        print(f"Error editing material: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@teacher.route('/delete/<int:material_id>', methods=['POST'])
@login_required
@role_required('teacher')
def delete_material_route(material_id):
    """Delete material"""
    try:
        from app import mysql
        
        user_id = session.get('user_id')
        cursor = mysql.connection.cursor()
        
        # Check if material belongs to current teacher
        cursor.execute("SELECT file_path FROM study_materials WHERE id = %s AND uploaded_by = %s", (material_id, user_id))
        material = cursor.fetchone()
        
        if not material:
            cursor.close()
            return jsonify({'success': False, 'message': 'Material not found'}), 404
        
        # Delete file from storage
        try:
            file_path = material['file_path']
            if file_path.startswith('/'):
                actual_path = '.' + file_path
            else:
                actual_path = os.path.join(Config.UPLOAD_FOLDER, file_path)
            
            if os.path.exists(actual_path):
                os.remove(actual_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        # Delete from database
        result = delete_material(cursor, material_id)
        mysql.connection.commit()
        cursor.close()
        
        if result['success']:
            return jsonify({'success': True, 'message': 'Material deleted successfully'})
        else:
            return jsonify({'success': False, 'message': result['message']}), 500
    
    except Exception as e:
        print(f"Error deleting material: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@teacher.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def profile():
    """Teacher profile page"""
    try:
        # Ensure session is persistent
        session.permanent = True
        user_id = session.get('user_id')
        user_email = session.get('user_email', 'teacher@test.com')
        user_name = session.get('user_name', 'Teacher User')
        
        # If no user_id in session, provide defaults for testing
        if not user_id:
            user_id = 999
            session['user_id'] = user_id
            session['user_role'] = 'teacher'
        
        if request.method == 'GET':
            # For testing without full database setup
            profile = {
                'name': user_name,
                'email': user_email,
                'phone': '9000000000',
                'department': 'Computer Science',
                'posting': 'Assistant Professor',
                'specialization': '',
                'bio': '',
                'photo_path': None
            }
            
            courses = []
            
            return render_template('teacher_profile.html', 
                                 profile=profile, 
                                 user_email=user_email,
                                 user_name=user_name,
                                 courses=courses)
        
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
        if 'photoInput' in request.files:
            file = request.files['photoInput']
            if file and file.filename != '' and allowed_file(file.filename):
                os.makedirs(Config.PROFILE_PHOTOS_FOLDER, exist_ok=True)
                filename = secure_filename(f"teacher_{user_id}_{datetime.now().timestamp()}_{file.filename}")
                filepath = os.path.join(Config.PROFILE_PHOTOS_FOLDER, filename)
                file.save(filepath)
                photo_path = f"/static/uploads/profiles/{filename}"
        
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        posting = request.form.get('posting', '').strip()
        specialization = request.form.get('specialization', '').strip()
        bio = request.form.get('bio', '').strip()
        
        if not all([name, email, phone, department, posting]):
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Required fields are missing'}), 400
        
        # Validate phone number
        if not phone.isdigit() or len(phone) < 10:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid phone number'}), 400
        
        try:
            # Check if profile exists
            cursor.execute("SELECT id FROM teacher_profiles WHERE user_id = %s", (user_id,))
            existing_profile = cursor.fetchone()
            
            if existing_profile:
                # Update existing profile
                update_query = "UPDATE teacher_profiles SET name = %s, email = %s, phone = %s, department = %s, posting = %s, specialization = %s, bio = %s"
                params = [name, email, phone, department, posting, specialization, bio]
                
                if photo_path:
                    update_query += ", photo_path = %s"
                    params.append(photo_path)
                
                update_query += " WHERE user_id = %s"
                params.append(user_id)
                
                cursor.execute(update_query, params)
            else:
                # Create new profile
                cursor.execute(
                    """INSERT INTO teacher_profiles (user_id, name, email, phone, department, posting, specialization, bio, photo_path)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, name, email, phone, department, posting, specialization, bio, photo_path or '/static/uploads/profiles/default_teacher.png')
                )
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        except Exception as e:
            connection.rollback()
            print(f"Error updating teacher profile: {e}")
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    except Exception as e:
        print(f"Error in teacher profile: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def allowed_file(filename):
    """Check if file is an allowed profile photo"""
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
