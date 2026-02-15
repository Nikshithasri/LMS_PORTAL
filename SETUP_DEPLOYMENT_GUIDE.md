# Educational Management System - Setup & Deployment Guide

## Project: Aishwarya Vignan Educational Society
**Technology Partner:** Ensafe Technologies Pvt Ltd

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Features Overview](#features-overview)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)
9. [Deployment](#deployment)

---

## Prerequisites

### Required Software
- **Python 3.8+**
- **MySQL Server 5.7+**
- **Git** (optional, for version control)
- **pip** (Python package manager)

### System Requirements
- **OS:** Windows, macOS, or Linux
- **Memory:** Minimum 2GB RAM
- **Storage:** Minimum 1GB free space
- **Browser:** Chrome, Firefox, Safari, or Edge (latest versions)

---

## Installation

### Step 1: Clone/Download the Project

```bash
cd "c:\Users\Admin\OneDrive\Desktop\PROJECTS\LMS"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies Included:**
- Flask 3.0.0 - Web framework
- PyMySQL 1.1.0 - MySQL connector
- Werkzeug 3.0.0 - WSGI utilities
- bcrypt 4.1.1 - Password hashing
- Flask-Bcrypt 1.0.1 - Flask bcrypt integration
- Flask-Session 0.5.0 - Session management
- Jinja2 3.1.2 - Template engine

### Step 4: Update Configuration

Edit `config.py` with your MySQL credentials:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'lms_db'
```

---

## Database Setup

### Step 1: Start MySQL Server

```bash
# Windows
mysql -u root -p

# macOS
mysql -u root -p

# Linux
sudo mysql -u root -p
```

### Step 2: Run Database Setup Script

```bash
python setup_database.py
```

This will:
- ✓ Create the `lms_db` database
- ✓ Create all necessary tables
- ✓ Insert default admin user

**Default Admin Credentials:**
- Email: `admin@aves.edu`
- Password: `Admin@123456`
- ⚠️ **Change immediately after first login!**

### Step 3: Verify Database Connection

```bash
python test_connection.py
```

---

## Configuration

### Environment Variables (Optional)

Create a `.env` file for production:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=lms_db
```

### Security Settings in config.py

```python
# Password requirements
MIN_PASSWORD_LENGTH = 8

# Password hashing
BCRYPT_LOG_ROUNDS = 12

# Session settings
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_SECURE = True  # HTTPS only (production)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start at: `http://localhost:5000`

### Production Mode

For production deployment, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Features Overview

### 🎓 Student Features
- View all approved study materials
- Filter materials by subject
- Download materials
- View material metadata (uploader, upload date)
- Manage personal profile with photo
- Secure account

### 👩‍🏫 Teacher Features
- Upload study materials (PDF, video, documents)
- Add subject and description
- Edit material details
- Delete own materials
- View upload statistics
- Material approval status tracking
- Manage professional profile

### 🛡️ Admin Features
- **User Management**
  - View all users by role
  - Create new users
  - Delete users (except admins)
  - Manage permissions

- **Material Management**
  - View all materials
  - Approve/Reject materials
  - Delete any material
  - Track downloads

- **Analytics**
  - User growth statistics
  - Material status overview
  - Top subjects by material count
  - System activity logs

- **System Control**
  - Full database access
  - Audit logs
  - Material approval workflow

---

## Security Considerations

### Password Security
✓ **bcrypt hashing** with 12 rounds
✓ **Strong password requirements:**
  - Minimum 8 characters
  - Must contain uppercase, lowercase, numbers, special characters
  - Maximum 128 characters

### Session Management
✓ **HTTP-only cookies** (prevents XSS attacks)
✓ **HTTPS in production** (SESSION_COOKIE_SECURE=True)
✓ **24-hour session timeout**
✓ **SameSite cookie policy** (prevents CSRF)

### File Upload Security
✓ **Secure filename validation**
✓ **File type whitelist**
  - Materials: pdf, mp4, avi, mov, docx, pptx
  - Profiles: png, jpg, jpeg, gif
✓ **Max file size: 50MB**
✓ **Separate upload directories**

### Database Security
✓ **Parameterized queries** (prevents SQL injection)
✓ **Role-based access control**
✓ **Audit logging** for admin actions

### Route Protection
✓ **Login-required decorators**
✓ **Role-based route protection**
✓ **Redirect unauthorized access**

---

## Database Schema

### Users Table
```sql
- id (Primary Key)
- email (Unique)
- password (Hashed)
- name
- role (student/teacher/admin)
- is_active
- created_at, updated_at
```

### Student Profiles Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- register_number (Unique)
- department
- course_details
- phone, profile_photo
- bio, created_at, updated_at
```

### Teacher Profiles Table
```sql
- id (Primary Key)
- user_id (Foreign Key)
- department, specialization
- phone, profile_photo
- bio, experience_years
- created_at, updated_at
```

### Study Materials Table
```sql
- id (Primary Key)
- title, subject, description
- file_path, file_type
- uploaded_by (Foreign Key to Users)
- approval_status (pending/approved/rejected)
- download_count
- upload_date, updated_date
- approved_by, approval_date
```

### Audit Logs Table
```sql
- id (Primary Key)
- user_id, action
- entity_type, entity_id
- old_value, new_value
- ip_address, user_agent
- created_at
```

---

## Project Structure

```
LMS/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── setup_database.py               # Database initialization
├── requirements.txt                # Python dependencies
│
├── models/
│   ├── auth_utils.py              # Password hashing & validation
│   ├── user_model.py              # User CRUD operations
│   ├── material_model.py           # Material CRUD operations
│   └── profile_model.py            # Profile management
│
├── routes/
│   ├── auth_routes.py             # Login, register, logout
│   ├── student_routes.py           # Student dashboard & features
│   ├── teacher_routes.py           # Teacher dashboard & features
│   └── admin_routes.py             # Admin dashboard & features
│
├── static/
│   └── uploads/
│       ├── materials/              # Study material uploads
│       └── profiles/               # Profile photos
│
├── templates/
│   ├── index.html                 # Home page
│   ├── role_selection.html        # Role selection
│   ├── login.html                 # Login form
│   ├── register.html              # Registration form
│   ├── student_dashboard.html     # Student dashboard
│   ├── teacher_dashboard.html     # Teacher dashboard
│   ├── admin_dashboard.html       # Admin dashboard
│   ├── student_profile.html       # Student profile
│   ├── teacher_profile.html       # Teacher profile
│   ├── upload_material.html       # Material upload
│   ├── error.html                 # Error pages
│   └── logout.html                # Logout page
│
└── docs/
    ├── DATABASE_SETUP.md           # Database documentation
    └── SETUP_GUIDE.md              # This file
```

---

## Troubleshooting

### Issue: "MySQL connection refused"
**Solution:**
```bash
# Check MySQL is running
# Windows: Services > MySQL
# macOS: System Preferences > MySQL
# Linux: sudo service mysql status
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Database 'lms_db' already exists"
**Solution:**
```bash
# Drop existing database first
python -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='root', password='Geetha@77'); cursor = conn.cursor(); cursor.execute('DROP DATABASE IF EXISTS lms_db'); conn.commit()"

# Then run setup again
python setup_database.py
```

### Issue: "Cannot find static/uploads directory"
**Solution:**
The directories are created automatically on first run. If not:
```bash
mkdir -p static/uploads/materials
mkdir -p static/uploads/profiles
```

### Issue: "Session expires too quickly"
**Check in config.py:**
```python
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)  # Increase if needed
```

---

## Deployment

### Option 1: Heroku Deployment

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.11.4" > runtime.txt

# Deploy
git push heroku main
```

### Option 2: AWS EC2 Deployment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip mysql-server -y

# Clone project
git clone <repository>
cd LMS

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Setup database
python setup_database.py

# Run with Gunicorn & Nginx
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Docker Deployment

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Security Checklist for Production

- [ ] Change all default credentials
- [ ] Set `FLASK_ENV=production`
- [ ] Update `SECRET_KEY` to a secure random string
- [ ] Enable HTTPS with SSL certificate
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Update MySQL password
- [ ] Configure firewall rules
- [ ] Set up daily backups
- [ ] Enable audit logging
- [ ] Configure email alerts for admin actions
- [ ] Use environment variables for sensitive data
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging

---

## Support & Maintenance

### Regular Maintenance Tasks
1. **Daily:** Monitor server logs
2. **Weekly:** Check user registrations
3. **Monthly:** Review audit logs
4. **Quarterly:** Update dependencies

### Backup Strategy
```bash
# Backup database weekly
mysqldump -u root -p lms_db > backup_$(date +%Y%m%d).sql

# Backup files
tar -czf lms_backup_$(date +%Y%m%d).tar.gz ~/LMS
```

### Performance Optimization
- Enable database query caching
- Implement pagination for large datasets
- Use CDN for static files
- Compress uploaded materials
- Monitor and optimize slow queries

---

## Contact & Support

**Organization:** Aishwarya Vignan Educational Society  
**Technology Partner:** Ensafe Technologies Pvt Ltd  
**Support:** contact@ensafe.tech

---

**Last Updated:** February 12, 2024  
**Version:** 1.0.0
