"""Admin routes for system management, approval, and analytics"""
from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import pymysql
from pymysql.cursors import DictCursor
from config import Config
from models.user_model import get_users_by_role, delete_user, create_user
from models.material_model import get_all_materials, get_pending_materials, update_material, delete_material
from models.profile_model import create_profile, get_profile
from routes.auth_routes import login_required, role_required
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/profile-test', methods=['GET', 'POST'])
def profile_test():
    """Admin profile page - Test version without authentication"""
    try:
        if request.method == 'GET':
            return render_template('admin_profile.html', 
                                 profile=None, 
                                 user_email='admin@lms.com',
                                 user_name='Admin User')
        
        # POST request - just return success for testing
        return jsonify({'success': True, 'message': 'Profile would be updated successfully'})
    
    except Exception as e:
        print(f"Error in admin profile test: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def allowed_file(filename):
    """Check if file is an allowed profile photo"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.PROFILE_ALLOWED_EXTENSIONS


@admin.route('/users')
@login_required
@role_required('admin')
def users():
    """Admin user management page"""
    try:
        session.permanent = True
        return render_template('admin_users.html')
    except Exception as e:
        print(f"Error loading users page: {e}")
        return render_template('error.html', message="Failed to load users page"), 500


@admin.route('/settings')
@login_required
@role_required('admin')
def settings():
    """Admin settings page"""
    try:
        session.permanent = True
        return render_template('admin_settings.html')
    except Exception as e:
        print(f"Error loading settings: {e}")
        return render_template('error.html', message="Failed to load settings page"), 500


@admin.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    """Admin dashboard with system statistics"""
    try:
        # Ensure session is persistent
        session.permanent = True
        
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        
        cursor = connection.cursor()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM users WHERE role = 'student'")
        total_students = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM users WHERE role = 'teacher'")
        total_teachers = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM study_materials")
        total_materials = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM study_materials WHERE approval_status = 'pending'")
        pending_materials = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM study_materials WHERE approval_status = 'approved'")
        approved_materials = cursor.fetchone()['total']
        
        cursor.close()
        connection.close()
        
        return render_template('admin_dashboard.html',
                             total_users=total_users,
                             total_students=total_students,
                             total_teachers=total_teachers,
                             total_materials=total_materials,
                             pending_materials=pending_materials,
                             approved_materials=approved_materials)
    
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        return render_template('error.html', message='Error loading dashboard'), 500


@admin.route('/users')
@login_required
@role_required('admin')
def manage_users():
    """View and manage all users"""
    try:
        from app import mysql
        
        role_filter = request.args.get('role', 'all')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        cursor = mysql.connection.cursor()
        
        if role_filter in ['student', 'teacher', 'admin']:
            cursor.execute(
                "SELECT id, email, name, role, created_at FROM users WHERE role = %s ORDER BY created_at DESC",
                (role_filter,)
            )
        else:
            cursor.execute(
                "SELECT id, email, name, role, created_at FROM users ORDER BY created_at DESC"
            )
        
        all_users = cursor.fetchall()
        total_users = len(all_users)
        
        # Paginate
        start = (page - 1) * per_page
        end = start + per_page
        users = all_users[start:end]
        total_pages = (total_users + per_page - 1) // per_page
        
        cursor.close()
        
        return render_template('admin_manage_users.html',
                             users=users,
                             page=page,
                             total_pages=total_pages,
                             role_filter=role_filter)
    
    except Exception as e:
        print(f"Error loading users: {e}")
        return render_template('error.html', message='Error loading users'), 500


@admin.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user_route(user_id):
    """Delete a user"""
    try:
        from app import mysql
        
        # Prevent deleting admin accounts
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if user['role'] == 'admin':
            return jsonify({'success': False, 'message': 'Cannot delete admin accounts'}), 403
        
        result = delete_user(cursor, user_id)
        mysql.connection.commit()
        cursor.close()
        
        if result['success']:
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        else:
            return jsonify({'success': False, 'message': result['message']}), 500
    
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/users/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_user_admin():
    """Create a new user (admin only)"""
    if request.method == 'GET':
        return render_template('admin_create_user.html')
    
    try:
        from app import mysql
        
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        
        if not all([email, password, name, role]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if role not in ['student', 'teacher', 'admin']:
            return jsonify({'success': False, 'message': 'Invalid role'}), 400
        
        cursor = mysql.connection.cursor()
        result = create_user(cursor, email, password, name, role)
        mysql.connection.commit()
        cursor.close()
        
        if result['success']:
            return jsonify({'success': True, 'message': f'User created successfully (ID: {result["user_id"]})'})
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/materials')
@login_required
@role_required('admin')
def manage_materials():
    """View and manage study materials"""
    try:
        from app import mysql
        
        status_filter = request.args.get('status', 'all')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        cursor = mysql.connection.cursor()
        
        if status_filter in ['pending', 'approved', 'rejected']:
            cursor.execute(
                """SELECT m.*, u.name as uploader_name 
                   FROM study_materials m 
                   JOIN users u ON m.uploaded_by = u.id 
                   WHERE m.approval_status = %s 
                   ORDER BY m.upload_date DESC""",
                (status_filter,)
            )
        else:
            cursor.execute(
                """SELECT m.*, u.name as uploader_name 
                   FROM study_materials m 
                   JOIN users u ON m.uploaded_by = u.id 
                   ORDER BY m.upload_date DESC"""
            )
        
        all_materials = cursor.fetchall()
        total_materials = len(all_materials)
        
        # Paginate
        start = (page - 1) * per_page
        end = start + per_page
        materials = all_materials[start:end]
        total_pages = (total_materials + per_page - 1) // per_page
        
        cursor.close()
        
        return render_template('admin_manage_materials.html',
                             materials=materials,
                             page=page,
                             total_pages=total_pages,
                             status_filter=status_filter)
    
    except Exception as e:
        print(f"Error loading materials: {e}")
        return render_template('error.html', message='Error loading materials'), 500


@admin.route('/materials/approve/<int:material_id>', methods=['POST'])
@login_required
@role_required('admin')
def approve_material(material_id):
    """Approve a material"""
    try:
        from app import mysql
        
        admin_id = session.get('user_id')
        cursor = mysql.connection.cursor()
        
        # Update material
        cursor.execute(
            """UPDATE study_materials SET approval_status = %s, approved_by = %s, approval_date = %s 
               WHERE id = %s""",
            ('approved', admin_id, datetime.now(), material_id)
        )
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Material approved successfully'})
    
    except Exception as e:
        print(f"Error approving material: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/materials/reject/<int:material_id>', methods=['POST'])
@login_required
@role_required('admin')
def reject_material(material_id):
    """Reject a material"""
    try:
        from app import mysql
        
        reason = request.form.get('reason', 'No reason provided').strip()
        admin_id = session.get('user_id')
        cursor = mysql.connection.cursor()
        
        # Update material
        cursor.execute(
            """UPDATE study_materials SET approval_status = %s, approved_by = %s, approval_date = %s 
               WHERE id = %s""",
            ('rejected', admin_id, datetime.now(), material_id)
        )
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Material rejected successfully'})
    
    except Exception as e:
        print(f"Error rejecting material: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/materials/delete/<int:material_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_material_admin(material_id):
    """Delete material as admin"""
    try:
        from app import mysql
        
        cursor = mysql.connection.cursor()
        
        # Get file path
        cursor.execute("SELECT file_path FROM study_materials WHERE id = %s", (material_id,))
        material = cursor.fetchone()
        
        if not material:
            cursor.close()
            return jsonify({'success': False, 'message': 'Material not found'}), 404
        
        # Delete file
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


@admin.route('/analytics')
@login_required
@role_required('admin')
def analytics():
    """Analytics and reporting"""
    try:
        from app import mysql
        
        cursor = mysql.connection.cursor()
        
        # Get various statistics
        cursor.execute(
            """SELECT COUNT(*) as count, DATE(created_at) as date 
               FROM users GROUP BY DATE(created_at) ORDER BY date DESC LIMIT 30"""
        )
        user_growth = cursor.fetchall()
        
        cursor.execute(
            """SELECT COUNT(*) as count, approval_status 
               FROM study_materials GROUP BY approval_status"""
        )
        material_status = cursor.fetchall()
        
        cursor.execute(
            """SELECT subject, COUNT(*) as count 
               FROM study_materials GROUP BY subject ORDER BY count DESC LIMIT 10"""
        )
        top_subjects = cursor.fetchall()
        
        cursor.close()
        
        return render_template('admin_analytics.html',
                             user_growth=user_growth,
                             material_status=material_status,
                             top_subjects=top_subjects)
    
    except Exception as e:
        print(f"Error loading analytics: {e}")
        return render_template('error.html', message='Error loading analytics'), 500

        return "Uploaded Successfully"

    return render_template('upload.html')


@admin.route('/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


@admin.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def profile():
    """Admin profile page"""
    try:
        # Ensure session is persistent
        session.permanent = True
        user_id = session.get('user_id')
        user_email = session.get('user_email', 'admin@test.com')
        user_name = session.get('user_name', 'Admin User')
        
        # If no user_id in session, provide defaults for testing
        if not user_id:
            user_id = 999
            session['user_id'] = user_id
            session['user_role'] = 'admin'
        
        if request.method == 'GET':
            # For testing without full database setup
            profile = {
                'name': user_name,
                'email': user_email,
                'phone': '9000000000',
                'department': 'Administration',
                'designation': 'System Administrator',
                'photo_path': None
            }
            
            return render_template('admin_profile.html', 
                                 profile=profile, 
                                 user_email=user_email,
                                 user_name=user_name)
        
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
        if 'photo_path' in request.files:
            file = request.files['photo_path']
            if file and file.filename != '' and allowed_file(file.filename):
                os.makedirs(Config.PROFILE_PHOTOS_FOLDER, exist_ok=True)
                filename = secure_filename(f"admin_{user_id}_{file.filename}")
                filepath = os.path.join(Config.PROFILE_PHOTOS_FOLDER, filename)
                file.save(filepath)
                photo_path = f"/static/uploads/profiles/{filename}"
        
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        designation = request.form.get('designation', '').strip()
        
        if not all([name, email, phone, department, designation]):
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Create or update profile
        try:
            create_profile(
                cursor, user_id, 'admin', name, phone, email, photo_path,
                department=department,
                designation=designation
            )
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        except Exception as e:
            connection.rollback()
            print(f"Error updating admin profile: {e}")
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    except Exception as e:
        print(f"Error in admin profile: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
