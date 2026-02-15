# MySQL Database Setup Guide for LMS Project

## Prerequisites
- MySQL Server installed and running
- Python 3.7+
- pip (Python package manager)

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database
Make sure MySQL is running. The database will be created automatically, but you can verify:

```bash
mysql -u root -p
# Enter password: Geetha@77
```

Then in MySQL console:
```sql
CREATE DATABASE IF NOT EXISTS lms_db;
```

### 3. Initialize Database Tables
Run the initialization script to create all tables:

```bash
python init_db.py
```

This will create:
- `users` - Store user accounts (admin, teacher, student)
- `courses` - Store course information
- `materials` - Store course materials/uploads
- `enrollments` - Store student-course enrollments
- `submissions` - Store student submissions

### 4. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Database Schema

### Users Table
- user_id (PK)
- name
- email (unique)
- password
- role (admin, teacher, student)
- course_id (FK)
- created_at, updated_at

### Courses Table
- course_id (PK)
- course_name
- course_code (unique)
- description
- teacher_id (FK)
- created_at, updated_at

### Materials Table
- material_id (PK)
- course_id (FK)
- title
- description
- file_path
- file_type
- uploaded_by (FK)
- created_at, updated_at

### Enrollments Table
- enrollment_id (PK)
- student_id (FK)
- course_id (FK)
- enrolled_at

### Submissions Table
- submission_id (PK)
- material_id (FK)
- student_id (FK)
- file_path
- submitted_at

## Troubleshooting

### Connection Issues
- Ensure MySQL is running: `mysql -u root -p`
- Check credentials in `config.py` match your MySQL setup
- Verify MYSQL_PASSWORD is correct

### Database Not Found
- Run `python init_db.py` to create the database and tables

### Module Import Errors
- Reinstall MySQLdb: `pip install --force-reinstall MySQLdb==2.1.1`

## Configuration
Database configuration is in `config.py`. Update if needed:
- MYSQL_HOST: localhost
- MYSQL_USER: root
- MYSQL_PASSWORD: Geetha@77
- MYSQL_DB: lms_db

## Next Steps
1. Update models in `/models/` to use the database
2. Update routes to query the database
3. Implement authentication and session management
4. Create forms for user input validation
