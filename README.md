<<<<<<< HEAD
# Educational Management System (LMS)

**Aishwarya Vignan Educational Society**  
**Technology Partner: Ensafe Technologies Pvt Ltd**

## 🎓 Professional Educational Management Solution

A complete, production-ready Learning Management System designed for educational institutions. This system provides separate, role-based dashboards for Students, Teachers, and Administrators to manage educational content efficiently.

---

## ✨ Key Features

### 🎓 **Student Dashboard**
- View all approved study materials
- Filter materials by subject
- Download educational resources
- Manage personal profile with photo upload
- View material metadata (uploader, date, statistics)

### 👩‍🏫 **Teacher Dashboard**
- Upload study materials (PDF, video, documents)
- Manage content (edit/delete)
- Track upload statistics
- Monitor material approval status
- Maintain professional profile

### 🛡️ **Admin Dashboard**
- Manage all user accounts (create/delete)
- Approve or reject uploaded materials
- View comprehensive analytics
- Monitor system usage
- Audit logging for all actions

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | HTML5, CSS3, Bootstrap | 5.3.0 |
| Backend | Python, Flask | 3.8+ / 3.0 |
| Database | MySQL | 5.7+ |
| Security | bcrypt | 4.1.1 |
| JavaScript | Vanilla JS | ES6+ |

---

## 📋 Quick Start

### Prerequisites
```
Python 3.8+
MySQL Server 5.7+
2GB RAM
Modern Web Browser
```

### Installation (3 Steps)

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Setup Database**
```bash
python setup_database.py
```

**3. Run Application**
```bash
python app.py
```

Navigate to: `http://localhost:5000`

---

## 👤 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@aves.edu | Admin@123456 |

⚠️ **Change immediately after first login!**

---

## 📁 Project Structure

```
LMS/
├── app.py                          # Main Flask application
├── config.py                       # Configuration
├── setup_database.py               # Database initialization
├── setup.bat                       # Windows setup script
│
├── models/                         # Database models
│   ├── auth_utils.py              # Password security
│   ├── user_model.py              # User management
│   ├── material_model.py           # Content management
│   └── profile_model.py            # User profiles
│
├── routes/                         # URL routing
│   ├── auth_routes.py             # Authentication
│   ├── student_routes.py           # Student features
│   ├── teacher_routes.py           # Teacher features
│   └── admin_routes.py             # Admin features
│
├── templates/                      # HTML templates
│   ├── index.html                 # Home page
│   ├── login.html                 # Login form
│   ├── student_dashboard.html
│   ├── teacher_dashboard.html
│   ├── admin_dashboard.html
│   └── [15+ more templates]
│
├── static/uploads/                # File storage
│   ├── materials/                 # Study materials
│   └── profiles/                  # Profile photos
│
└── documentation/
    ├── PROJECT_DOCUMENTATION.md
    └── SETUP_DEPLOYMENT_GUIDE.md
```

---

## 🔐 Security Features

### Authentication & Authorization
✅ **bcrypt password hashing** (12 rounds)  
✅ **Role-based access control (RBAC)**  
✅ **Secure session management** (24-hour timeout)  
✅ **HTTP-only cookies** (XSS prevention)  
✅ **HTTPS support** (production)  

### Database Security
✅ **Parameterized queries** (SQL injection prevention)  
✅ **Hashed passwords** in database  
✅ **Audit logging** for sensitive operations  
✅ **Automatic backups** support  

### File Upload Security
✅ **Filename sanitization**  
✅ **File type validation**  
✅ **Max file size: 50MB**  
✅ **Separate storage directories**  

### Password Requirements
```
Minimum 8 characters
Must include: Uppercase, Lowercase, Numbers, Special characters
Examples: Admin@123456, Teacher#2024Pass
```

---

## 📊 API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /about` - About page
- `GET /contact` - Contact page

### Authentication
- `GET/POST /auth/` - Role selection
- `GET/POST /auth/login/<role>` - Login
- `GET/POST /auth/register/<role>` - Registration
- `GET /auth/logout` - Logout

### Student Routes
- `GET /student/dashboard` - Dashboard
- `GET /student/profile` - User profile
- `GET /student/materials/filter` - Filter materials

### Teacher Routes
- `GET /teacher/dashboard` - Dashboard
- `POST /teacher/upload` - Upload material
- `POST /teacher/edit/<id>` - Edit material
- `POST /teacher/delete/<id>` - Delete material

### Admin Routes
- `GET /admin/dashboard` - Dashboard
- `GET /admin/users` - Manage users
- `GET /admin/materials` - Manage materials
- `GET /admin/analytics` - View analytics

---

## 💾 Database Schema

### Users Table
```sql
id, email (unique), password (hashed), name, role, is_active, created_at
```

### Study Materials Table
```sql
id, title, subject, description, file_path, uploaded_by (FK),
approval_status, upload_date, download_count, approved_by, approval_date
```

### Profiles Tables (Student/Teacher)
```sql
id, user_id (FK), department, phone, profile_photo, bio, created_at
```

---

## 🚀 Deployment Options

### Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker build -t lms .
docker run -p 5000:5000 lms
```

### Cloud Platforms
- **Heroku:** Deploy via Git
- **AWS EC2:** Ubuntu + Gunicorn + Nginx
- **DigitalOcean:** App Platform or Droplet
- **Azure:** App Service or VM

---

## 📖 Documentation

### Complete Guides Available
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete system documentation
- **[SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md)** - Detailed setup instructions

### Topics Covered
- Installation & configuration
- Database schema & initialization
- Security best practices
- API reference
- Troubleshooting
- Performance optimization
- Deployment strategies
- Backup & maintenance

---

## 🐛 Troubleshooting

### MySQL Connection Error
```bash
# Verify MySQL is running and restart if needed
# Update credentials in config.py
python test_connection.py
```

### Python Dependencies
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
# Use different port in app.py
app.run(port=5001)
```

### File Upload Issues
```bash
# Ensure upload directories exist
mkdir -p static/uploads/materials
mkdir -p static/uploads/profiles
```

---

## 📈 Performance & Scalability

### Optimization Techniques
- Database query optimization with indexes
- Pagination for large datasets
- File compression support
- Caching strategies
- Connection pooling

### Recommended Hardware
- **Development:** 2GB RAM, 1GB Storage
- **Production:** 4GB RAM, 10GB Storage, SSD
- **Large Scale:** Load balancer + multiple app servers

---

## 🔄 User Workflows

### Student Workflow
```
Register → Login → View Dashboard → Filter Materials → Download
```

### Teacher Workflow
```
Register → Login → Upload Material → Monitor Status → Manage Content
```

### Admin Workflow
```
Login → Approve Materials → Manage Users → View Analytics
```

---

## 📞 Support & Contact

### Organization
**Aishwarya Vignan Educational Society**
- Email: info@aves.edu
- Phone: +91-XXXX-XXXXXX

### Technology Partner
**Ensafe Technologies Pvt Ltd**
- Email: support@ensafe.tech
- Website: www.ensafe.tech

---

## 📋 Version Information

| Item | Details |
|------|---------|
| Version | 1.0.0 |
| Release Date | February 12, 2024 |
| Python | 3.8+ |
| Flask | 3.0.0 |
| MySQL | 5.7+ |
| Bootstrap | 5.3.0 |

---

## 📜 License & Copyright

© 2024 Aishwarya Vignan Educational Society. All rights reserved.

Technology provided by Ensafe Technologies Pvt Ltd.

---

## 🎯 Future Enhancements

- [ ] Video streaming with adaptive bitrate
- [ ] Real-time discussion forums
- [ ] Assignment management system
- [ ] Grade tracking & reporting
- [ ] Email notifications
- [ ] Mobile applications (iOS/Android)
- [ ] Advanced analytics with ML insights
- [ ] Third-party integrations (Zoom, Google Meet)

---

## ✅ Features Checklist

### Completed
- ✅ Role-based authentication (Student/Teacher/Admin)
- ✅ Material upload & management
- ✅ Material approval workflow
- ✅ User profile management
- ✅ Analytics dashboard
- ✅ Responsive UI
- ✅ Security best practices
- ✅ Database schema

### In Development
- 🔄 Advanced notification system
- 🔄 Mobile responsive optimization
- 🔄 API documentation

---

## 🎉 Getting Started Today

1. **Clone/Download** the project
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Setup database:** `python setup_database.py`
4. **Start application:** `python app.py`
5. **Login:** Open `http://localhost:5000`

---

## 📚 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Bootstrap Docs: https://getbootstrap.com/docs/
- MySQL Docs: https://dev.mysql.com/doc/
- Bcrypt Security: https://cheatsheetseries.owasp.org/

---

**Made with ❤️ by Ensafe Technologies Pvt Ltd**

For questions or support, contact support@ensafe.tech
=======
# LMS_PORTAL
Integrated Student–Teacher Learning Portal is a centralized web application designed to streamline academic interaction between students and teachers. It enables lesson sharing, assignment management, resource uploads, progress tracking, and seamless communication through a unified platform, and learning efficiency within educational institutions.
>>>>>>> eb67b3ca924cd6634e82793fe1015c7513b402e4
