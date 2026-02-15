# LMS Quick Reference & Cheat Sheet

**Aishwarya Vignan Educational Society**

---

## ⚡ Quick Commands

### Setup & Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Activate virtual environment (Windows)
venv\Scripts\activate

# 3. Setup database (creates tables and admin user)
python setup_database.py

# 4. Run application
python app.py

# 5. Access application
http://localhost:5000
```

### Database Operations
```bash
# Backup database
mysqldump -u root -p lms_db > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u root -p lms_db < backup_20240212.sql

# Connect to MySQL
mysql -u root -p

# Show all databases
SHOW DATABASES;

# Use specific database
USE lms_db;

# Show all tables
SHOW TABLES;
```

---

## 🔐 Default Credentials

```
Admin Email: admin@aves.edu
Admin Password: Admin@123456

⚠️ IMPORTANT: Change password after first login!
```

---

## 📍 URL Routes

### Public Pages
```
http://localhost:5000/              (Home)
http://localhost:5000/about         (About)
http://localhost:5000/contact       (Contact)
```

### Authentication
```
http://localhost:5000/auth/                    (Role selection)
http://localhost:5000/auth/login/student       (Student login)
http://localhost:5000/auth/login/teacher       (Teacher login)
http://localhost:5000/auth/login/admin         (Admin login)
http://localhost:5000/auth/register/student    (Student register)
http://localhost:5000/auth/register/teacher    (Teacher register)
http://localhost:5000/auth/logout              (Logout)
```

### Student Routes
```
http://localhost:5000/student/dashboard        (Dashboard)
http://localhost:5000/student/profile          (Profile)
http://localhost:5000/student/materials/filter (Filter materials)
```

### Teacher Routes
```
http://localhost:5000/teacher/dashboard        (Dashboard)
http://localhost:5000/teacher/upload           (Upload material)
http://localhost:5000/teacher/profile          (Profile)
```

### Admin Routes
```
http://localhost:5000/admin/dashboard          (Dashboard)
http://localhost:5000/admin/users              (Manage users)
http://localhost:5000/admin/materials          (Manage materials)
http://localhost:5000/admin/analytics          (Analytics)
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `config.py` | Database credentials & settings |
| `app.py` | Main application entry point |
| `setup_database.py` | Database initialization script |
| `requirements.txt` | Python dependencies |
| `setup.bat` | Windows setup script |

---

## 🔧 Configuration Tips

### Update Database Credentials
Edit `config.py`:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'lms_db'
```

### Change Application Port
Edit `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Enable HTTPS (Production)
In `config.py`:
```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

---

## 📊 Database Tables Overview

### Users
- Stores login credentials (email, hashed password)
- Role: student, teacher, admin
- Timestamps: created_at, updated_at

### Study Materials
- Title, subject, description
- File path and type
- Uploaded by (teacher ID)
- Approval status (pending/approved/rejected)
- Download count

### Student Profiles
- Register number, department
- Course details, phone
- Profile photo, bio

### Teacher Profiles
- Department, specialization
- Phone, profile photo
- Bio, experience years

### Audit Logs
- User actions tracking
- Entity changes (old_value, new_value)
- IP address, user agent

---

## 🛡️ Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in config.py
- [ ] Ensure MySQL password is strong
- [ ] Enable HTTPS for production
- [ ] Set up regular database backups
- [ ] Configure firewall rules
- [ ] Enable audit logging
- [ ] Review user permissions
- [ ] Monitor upload folder
- [ ] Set up monitoring & alerts

---

## 🚀 Performance Tips

1. **Database**
   - Add indexes on frequently searched columns
   - Use LIMIT clause for pagination
   - Archive old data periodically

2. **Application**
   - Enable caching for static files
   - Use CDN for large files
   - Implement pagination (default 20 items/page)
   - Compress uploads

3. **Frontend**
   - Minify CSS/JavaScript
   - Lazy load images
   - Use Bootstrap grid system
   - Cache browser resources

---

## 🐛 Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| MySQL not connecting | Check MySQL is running, verify credentials in config.py |
| Module not found | Run `pip install -r requirements.txt` |
| Port 5000 in use | Change port in app.py or kill process: `lsof -i :5000` |
| Upload folder missing | Run `mkdir -p static/uploads/{materials,profiles}` |
| Permission denied | Check file/folder permissions, run with elevated privileges |
| Slow queries | Add database indexes, implement pagination |

---

## 📋 User Role Permissions

### Student
✓ View own profile  
✓ View approved materials  
✓ Download materials  
✓ Edit own profile  
✗ Cannot approve materials  
✗ Cannot upload materials  

### Teacher
✓ View own profile  
✓ Upload materials  
✓ Edit own materials  
✓ Delete own materials  
✓ View upload statistics  
✗ Cannot delete others' materials  
✗ Cannot approve materials  

### Admin
✓ Full access to all features  
✓ Manage all users  
✓ Approve/reject materials  
✓ Delete any content  
✓ View analytics  
✓ Audit logs access  

---

## 📱 Responsive Design

- **Mobile (< 768px):** Single column, mobile navigation
- **Tablet (768px - 1024px):** Two columns, optimized touch
- **Desktop (> 1024px):** Full layout with sidebar navigation

---

## 🔄 Data Flow Diagram

```
User Login
    ↓
Session Created
    ↓
Role Checked
    ↓
Dashboard Loaded
    ↓
Appropriate Content Displayed
    ↓
User Interactions (Upload/Download/Edit)
    ↓
Database Updated
    ↓
Audit Log Entry Created
```

---

## 📞 Getting Help

1. **Check Logs**
   ```bash
   # Flask debug mode shows errors in console
   python app.py
   ```

2. **Test Database**
   ```bash
   python test_connection.py
   ```

3. **Review Documentation**
   - See `PROJECT_DOCUMENTATION.md`
   - See `SETUP_DEPLOYMENT_GUIDE.md`

4. **Contact Support**
   - Email: support@ensafe.tech
   - Phone: +91-XXXX-XXXXXX

---

## 🎯 Common Tasks

### Create a New User (Admin)
1. Login as admin
2. Go to `/admin/users/create`
3. Fill in form (Email, Password, Name, Role)
4. Click "Create Account"

### Approve Material (Admin)
1. Login as admin
2. Go to `/admin/materials`
3. Find pending material
4. Click "Approve"

### Upload Material (Teacher)
1. Login as teacher
2. Click "Upload Material"
3. Fill in (Title, Subject, Description)
4. Select file
5. Click "Upload"

### Download Material (Student)
1. Login as student
2. Go to dashboard
3. Find material
4. Click "Download" button

---

## 🔑 Password Requirements

✓ Minimum 8 characters  
✓ Include uppercase (A-Z)  
✓ Include lowercase (a-z)  
✓ Include numbers (0-9)  
✓ Include special chars (!@#$%^&*)  

**Example:** Admin@123456, Teacher#2024Pass

---

## 📦 Deployment Checklist

- [ ] Update credentials (username, password)
- [ ] Set production environment variables
- [ ] Enable HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Set up CDN for static files
- [ ] Implement rate limiting
- [ ] Configure firewall
- [ ] Test disaster recovery
- [ ] Document credentials (secure storage)
- [ ] Set up alerts for errors

---

## 🚢 Production Deployment Steps

```bash
# 1. Update environment
export FLASK_ENV=production

# 2. Update SECRET_KEY
# Edit config.py with secure random string

# 3. Install production server
pip install gunicorn

# 4. Run application
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 5. Setup reverse proxy (Nginx)
# Create Nginx config pointing to localhost:5000

# 6. Setup SSL/TLS
# Use Let's Encrypt or similar

# 7. Enable automatic restart
# Use systemd or supervisor
```

---

## 📊 Monitoring Commands

```bash
# Monitor active connections
lsof -i :5000

# Check database size
SELECT table_schema "Database", SUM(data_length + index_length) "Size" 
FROM information_schema.tables WHERE table_schema = "lms_db" 
GROUP BY table_schema;

# Count users by role
SELECT role, COUNT(*) FROM users GROUP BY role;

# Check upload folder size
du -sh static/uploads/
```

---

## 🎓 Learning Path

1. **Basics** → Understand project structure
2. **Setup** → Install and run locally
3. **Navigation** → Explore all features
4. **Security** → Review security implementation
5. **Customization** → Modify for your needs
6. **Deployment** → Deploy to production
7. **Maintenance** → Setup monitoring & backups

---

## 📚 Useful Links

- Flask: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/
- MySQL: https://dev.mysql.com/
- Python: https://www.python.org/
- bcrypt: https://pypi.org/project/bcrypt/

---

## 💡 Tips & Best Practices

✓ Always use HTTPS in production  
✓ Keep dependencies updated  
✓ Regular database backups  
✓ Monitor error logs  
✓ Test before deploying  
✓ Use strong passwords  
✓ Implement rate limiting  
✓ Regular security audits  
✓ Document changes  
✓ Version control with Git  

---

**Last Updated:** February 12, 2024  
**Version:** 1.0.0

For more help, visit the full documentation or contact support@ensafe.tech
