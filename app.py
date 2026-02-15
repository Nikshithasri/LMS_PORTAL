"""
Educational Management System
Main Flask Application - Frontend Only

Aishwarya Vignan Educational Society
Technology Partner: Ensafe Technologies Pvt Ltd
"""

from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_file
import os
from datetime import timedelta
from werkzeug.utils import secure_filename
from materials_store import add_material, get_all_materials, delete_material, get_material, increment_downloads
from enrollments_store import get_all_courses, get_student_enrollments
from config import Config
from routes.teacher_routes import teacher
from routes.student_routes import student
from routes.auth_routes import auth
from routes.admin_routes import admin

# Initialize Flask app
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = False  # Allow JavaScript access for debugging
app.config['SESSION_COOKIE_SECURE'] = False  # Allow HTTP for development
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# MySQL Configuration stored in app config for access by routes
app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB

# Ensure sessions are maintained
@app.before_request
def before_request():
    """Refresh session if user is logged in"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=24)

# Register blueprints
app.register_blueprint(teacher)
app.register_blueprint(student)
app.register_blueprint(auth)
app.register_blueprint(admin)

# Upload configuration
UPLOAD_FOLDER = 'static/uploads/materials'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'zip', 'txt', 'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@app.route('/')
def home():
    """Home page - Role selection"""
    return render_template('role_selection.html')


@app.route('/admin-login')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')


@app.route('/teacher-login')
def teacher_login():
    """Teacher login page"""
    return render_template('teacher_login.html')


@app.route('/student-login')
def student_login():
    """Student login page"""
    return render_template('student_login.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')


@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')


@app.route('/register')
def register():
    """Register page"""
    return render_template('register.html')


@app.route('/student-dashboard')
def student_dashboard():
    """Student dashboard - Test route with session setup"""
    # Set up session for testing
    session.permanent = True
    session['user_id'] = 999
    session['user_email'] = 'student@test.com'
    session['user_name'] = 'Student User'
    session['user_role'] = 'student'
    
    materials = get_all_materials()
    return render_template('student_dashboard.html', user_name='Student User', materials=materials, material_count=len(materials))


@app.route('/teacher-dashboard')
def teacher_dashboard():
    """Teacher dashboard - Test route with session setup"""
    # Set up session for testing
    session.permanent = True
    session['user_id'] = 999
    session['user_email'] = 'teacher@test.com'
    session['user_name'] = 'Teacher User'
    session['user_role'] = 'teacher'
    
    materials = get_all_materials()
    return render_template('teacher_dashboard.html', user_name='Teacher User', materials=materials, material_count=len(materials))


@app.route('/admin-dashboard')
def admin_dashboard():
    """Admin dashboard - Test route with session setup"""
    # Set up session for testing
    session.permanent = True
    session['user_id'] = 999
    session['user_email'] = 'admin@test.com'
    session['user_name'] = 'Admin User'
    session['user_role'] = 'admin'
    
    return render_template('admin_dashboard.html', user_name='Admin User')


@app.route('/admin-profile')
def admin_profile():
    """Admin profile page"""
    return render_template('admin_profile.html', 
                         user_name='Admin User',
                         user_email='admin@lms.com')


@app.route('/teacher-profile')
def teacher_profile():
    """Teacher profile page"""
    courses = get_all_courses()
    return render_template('teacher_profile.html',
                         user_name='Teacher User',
                         user_email='teacher@lms.com',
                         profile=None,
                         courses=courses)


@app.route('/student-profile')
def student_profile():
    """Student profile page"""
    # Get enrollments for the current student (using S001 as default)
    enrollments = get_student_enrollments('S001')
    return render_template('student_profile.html',
                         user_name='Student User',
                         user_email='student@lms.com',
                         profile=None,
                         enrollments=enrollments)


@app.route('/upload')
def upload():
    """Upload page"""
    return render_template('upload.html')


@app.route('/logout')
def logout():
    """Logout page"""
    session.clear()
    return render_template('logout.html')


@app.route('/admin-logout')
def admin_logout():
    """Admin logout page"""
    session.clear()
    return render_template('admin_logout.html')


@app.route('/teacher-logout')
def teacher_logout():
    """Teacher logout page"""
    session.clear()
    return render_template('teacher_logout.html')


@app.route('/student-logout')
def student_logout():
    """Student logout page"""
    session.clear()
    return render_template('student_logout.html')


@app.route('/teacher/upload-material', methods=['POST'])
def teacher_upload_material():
    """Handle teacher material upload"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'File type not allowed. Allowed: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, ZIP, TXT, JPG, PNG, GIF'}), 400

        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if not title:
            return jsonify({'success': False, 'message': 'Title is required'}), 400

        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file with secure filename
        original_filename = file.filename
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        
        # Generate unique filename
        import uuid
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)

        # Add to materials database
        material = add_material(
            title=title,
            description=description,
            filename=unique_filename,
            original_name=original_filename,
            file_path=f'/static/uploads/materials/{unique_filename}',
            teacher_name='Teacher User'
        )

        # Return success response
        return jsonify({
            'success': True,
            'message': f'File "{original_filename}" uploaded successfully!',
            'material': material
        }), 200

    except Exception as e:
        print(f"Upload error: {str(e)}")
        return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'}), 500


@app.route('/teacher/delete-material/<int:material_id>', methods=['POST'])
def teacher_delete_material(material_id):
    """Handle material deletion"""
    try:
        material = get_material(material_id)
        
        if not material:
            return jsonify({'success': False, 'message': 'Material not found'}), 404
        
        # Delete file from disk
        file_path = material['filename']
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], file_path)
        
        if os.path.exists(full_path):
            os.remove(full_path)
        
        # Delete from database
        delete_material(material_id)
        
        return jsonify({
            'success': True,
            'message': 'Material deleted successfully!'
        }), 200
    except Exception as e:
        print(f"Delete error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/materials/view/<int:material_id>')
def view_material(material_id):
    """View material details"""
    material = get_material(material_id)
    
    if not material:
        return render_template('error.html', message='Material not found'), 404
    
    return render_template('view_material.html', material=material)


@app.route('/materials/download/<int:material_id>')
def download_material(material_id):
    """Download material file"""
    try:
        material = get_material(material_id)
        
        if not material:
            return 'Material not found', 404
        
        # Increment download count
        increment_downloads(material_id)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], material['filename'])
        
        if not os.path.exists(file_path):
            return 'File not found', 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=material['original_name']
        )
    except Exception as e:
        print(f"Download error: {str(e)}")
        return f'Download failed: {str(e)}', 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', message='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', message='Internal server error'), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return render_template('error.html', message='Access forbidden'), 403


@app.context_processor
def inject_org_info():
    """Inject organization info into all templates"""
    return dict(
        org_name='Aishwarya Vignan Educational Society',
        tech_partner='Ensafe Technologies Pvt Ltd'
    )


if __name__ == '__main__':
    # Create upload folders if they don't exist
    os.makedirs('static/uploads/materials', exist_ok=True)
    os.makedirs('static/uploads/profiles', exist_ok=True)
    
    # Run app
    app.run(debug=True, host='0.0.0.0', port=5000)
