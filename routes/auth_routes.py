"""Authentication routes for login, logout, and role-based access"""
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from datetime import datetime
from functools import wraps
from models.user_model import authenticate_user, create_user
from models.auth_utils import validate_password
from config import Config

auth = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.role_selection'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.role_selection'))
            if session.get('user_role') != role and session.get('user_role') != 'admin':
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth.route('/')
def role_selection():
    """Role selection page - shows three login options"""
    if 'user_id' in session:
        # Redirect to appropriate dashboard based on role
        role = session.get('user_role')
        if role == 'student':
            return redirect(url_for('student.dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin.dashboard'))
    
    return render_template('role_selection.html')


@auth.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    """
    Login route for specific role
    
    Args:
        role: student, teacher, or admin
    """
    if role not in ['student', 'teacher', 'admin']:
        return redirect(url_for('auth.role_selection'))
    
    if request.method == 'GET':
        return render_template('login.html', role=role)
    
    # POST request - handle login
    try:
        from app import mysql
        
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            return render_template('login.html', 
                                 role=role, 
                                 error='Email and password are required'), 400
        
        cursor = mysql.connection.cursor()
        
        # Authenticate user
        result = authenticate_user(cursor, email, password)
        cursor.close()
        
        if not result['success']:
            return render_template('login.html', 
                                 role=role, 
                                 error=result['message']), 401
        
        # Check if user has correct role
        if result['role'] != role and role != 'admin':
            # Allow admin to login from any role
            if not (role == 'admin' and result['role'] == 'admin'):
                return render_template('login.html', 
                                     role=role, 
                                     error=f'This account is not a {role} account'), 403
        
        # Set session data
        session.permanent = True
        session['user_id'] = result['user_id']
        session['user_email'] = result['email']
        session['user_name'] = result['name']
        session['user_role'] = result['role']
        session['login_time'] = datetime.now()
        
        # Redirect to appropriate dashboard
        if result['role'] == 'student':
            return redirect(url_for('student.dashboard'))
        elif result['role'] == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif result['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
    
    except Exception as e:
        print(f"Login error: {e}")
        return render_template('login.html', 
                             role=role, 
                             error='Login failed. Please try again'), 500


@auth.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    """
    Registration route for specific role
    
    Args:
        role: student or teacher (admin accounts created separately)
    """
    if role not in ['student', 'teacher']:
        return redirect(url_for('auth.role_selection'))
    
    if request.method == 'GET':
        return render_template('register.html', role=role)
    
    # POST request - handle registration
    try:
        from app import mysql
        
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        name = request.form.get('name', '').strip()
        
        # Validation
        if not all([email, password, confirm_password, name]):
            return render_template('register.html', 
                                 role=role, 
                                 error='All fields are required'), 400
        
        if password != confirm_password:
            return render_template('register.html', 
                                 role=role, 
                                 error='Passwords do not match'), 400
        
        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            return render_template('register.html', 
                                 role=role, 
                                 error=message), 400
        
        cursor = mysql.connection.cursor()
        
        # Create user
        result = create_user(cursor, email, password, name, role)
        
        if not result['success']:
            cursor.close()
            return render_template('register.html', 
                                 role=role, 
                                 error=result['message']), 400
        
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to login page
        return redirect(url_for('auth.login', role=role))
    
    except Exception as e:
        print(f"Registration error: {e}")
        return render_template('register.html', 
                             role=role, 
                             error='Registration failed. Please try again'), 500


@auth.route('/logout')
def logout():
    """Logout user and clear session"""
    try:
        # Get user information before clearing session
        user_name = session.get('user_name', 'User')
        user_role = session.get('user_role', 'Unknown')
        login_time = session.get('login_time', datetime.now())
        
        # Calculate session duration
        logout_time = datetime.now()
        if isinstance(login_time, datetime):
            session_duration = str(logout_time - login_time)
        else:
            session_duration = 'Unknown'
        
        # Format times
        logout_time_str = logout_time.strftime('%I:%M %p on %B %d, %Y')
        
        # Clear session data
        session.clear()
        
        # Render logout page with information
        return render_template('logout.html', 
                              user_name=user_name,
                              logout_time=logout_time_str,
                              session_duration=session_duration,
                              user_role=user_role)
    
    except Exception as e:
        print(f"Logout error: {e}")
        session.clear()
        return redirect(url_for('home'))
