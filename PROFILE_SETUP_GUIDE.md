# LMS Profile Management System - Setup & Usage Guide

## Overview
Complete profile management system for Students, Teachers, and Admins with photo upload and database storage.

---

## ✅ What's Been Set Up

### 1. **Database Tables Created**
- ✅ `student_profiles` - Stores student profile information
- ✅ `teacher_profiles` - Stores teacher profile information  
- ✅ `admin_profiles` - Stores admin profile information

### 2. **Profile Pages Created**
- ✅ Student Profile: `/student/profile`
- ✅ Teacher Profile: `/teacher/profile`
- ✅ Admin Profile: `/admin/profile`

### 3. **Backend Routes**
- ✅ `/student/profile` - GET/POST for student profile management
- ✅ `/teacher/profile` - GET/POST for teacher profile management
- ✅ `/admin/profile` - GET/POST for admin profile management

### 4. **Features Implemented**
- 📸 Photo upload with preview
- 💾 Save profile to database
- 📋 Role-specific fields
- ✔️ Form validation
- 🎯 Database storage of all information

---

## 📋 Student Profile Fields

```
- Full Name *
- Register Number *
- Email ID * (pre-filled)
- Phone Number *
- Department *
- Course Details *
- Profile Photo (optional)
- Bio (optional)
```

**Database Table**: `student_profiles`
**Fields stored**: user_id, name, register_number, department, course_details, phone, email, photo_path

---

## 👨‍🏫 Teacher Profile Fields

```
- Full Name *
- Email ID * (pre-filled)
- Phone Number *
- Department *
- Designation / Posting *
- Profile Photo (optional)
- Specialization (optional)
- Professional Bio (optional)
```

**Database Table**: `teacher_profiles`
**Fields stored**: user_id, name, department, posting, phone, email, photo_path

---

## 👨‍💼 Admin Profile Fields

```
- Full Name *
- Email ID * (pre-filled)
- Phone Number *
- Department *
- Designation / Position *
- Profile Photo (optional)
- Key Responsibilities (optional)
- Professional Bio (optional)
```

**Database Table**: `admin_profiles`
**Fields stored**: user_id, name, department, designation, phone, email, photo_path

---

## 🚀 How to Access Profile Pages

### For Students:
1. Login as student (email: student@lms.com)
2. Go to: `http://localhost:5000/student/profile`
3. Fill in your information
4. Upload a photo (PNG, JPG, JPEG, GIF)
5. Click "Save Profile"

### For Teachers:
1. Login as teacher (email: teacher@lms.com)
2. Go to: `http://localhost:5000/teacher/profile`
3. Fill in your information
4. Upload a photo
5. Click "Save Profile"

### For Admins:
1. Login as admin (email: admin@lms.com)
2. Go to: `http://localhost:5000/admin/profile`
3. Fill in your information
4. Upload a photo
5. Click "Save Profile"

---

## 📁 Project File Structure

```
templates/
├── student_profile.html      ← Student profile page
├── teacher_profile.html      ← Teacher profile page
└── admin_profile.html        ← Admin profile page

models/
├── profile_model.py          ← Profile database functions

routes/
├── student_routes.py         ← Student profile routes
├── teacher_routes.py         ← Teacher profile routes
└── admin_routes.py           ← Admin profile routes

static/uploads/
└── profiles/                 ← Profile photos stored here

init_profile_tables.py        ← Script to create profile tables
```

---

## 🖼️ Photo Upload Details

- **Allowed Formats**: PNG, JPG, JPEG, GIF
- **Max File Size**: 16MB
- **Storage Location**: `/static/uploads/profiles/`
- **Naming Convention**: `{role}_{user_id}_{filename}`
- **Example**: `student_13_profile.jpg`

---

## 🔄 Database Queries

### View Student Profile:
```sql
SELECT * FROM student_profiles WHERE user_id = 13;
```

### View All Teacher Profiles:
```sql
SELECT * FROM teacher_profiles;
```

### View Admin Profile:
```sql
SELECT * FROM admin_profiles WHERE user_id = user_id;
```

### Update Photo:
```sql
UPDATE student_profiles SET photo_path = '/path/to/photo' WHERE user_id = 13;
```

---

## 💡 Key Features

✅ **Photo Upload**: Users can upload and update profile photos
✅ **Database Storage**: All data persisted in MySQL database
✅ **Validation**: Client-side and server-side form validation
✅ **Error Handling**: Comprehensive error messages
✅ **Responsive Design**: Works on desktop, tablet, and mobile
✅ **Role-Specific Fields**: Each role has tailored profile fields
✅ **Auto-fill**: Email pre-filled from login session
✅ **Dashboard Links**: Quick access to user dashboard from profile

---

## 🔗 Integration with Dashboard

### Student Dashboard:
Add link to profile page:
```html
<a href="/student/profile">Edit Profile</a>
```

### Teacher Dashboard:
Add link to profile page:
```html
<a href="/teacher/profile">Edit Profile</a>
```

### Admin Dashboard:
Add link to profile page:
```html
<a href="/admin/profile">Edit Profile</a>
```

---

## 📊 Database Schema

### student_profiles Table:
```sql
CREATE TABLE student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    register_number VARCHAR(50),
    department VARCHAR(100),
    course_details VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

### teacher_profiles Table:
```sql
CREATE TABLE teacher_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    posting VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

### admin_profiles Table:
```sql
CREATE TABLE admin_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    designation VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

---

## 🌐 Using Online PostgreSQL (Optional)

If you want to use **free online PostgreSQL** instead of local MySQL:

### Recommended Services:
1. **Supabase** (https://supabase.com) - FREE tier
2. **Railway** (https://railway.app) - $5 credit/month free
3. **Render** (https://render.com) - Free PostgreSQL

### Steps:
1. Create account on any of the above
2. Create a new PostgreSQL database
3. Get your connection string
4. Update `config.py`:
```python
POSTGRESQL_URL = "postgresql://user:password@host:port/database"
```

5. Update database connection in `app.py` to use PostgreSQL instead of MySQL

---

## ✨ Test the System

1. **Start Flask server**: Already running on `http://localhost:5000`
2. **Login** as any user (student, teacher, or admin)
3. **Navigate** to their respective profile page
4. **Fill** in the profile form
5. **Upload** a profile photo
6. **Save** and verify data is stored in database

---

## 🐛 Troubleshooting

### Issue: Photo not uploading
- Check file format (must be PNG, JPG, JPEG, or GIF)
- Check file size (max 16MB)
- Ensure `/static/uploads/profiles/` folder exists

### Issue: Profile not saving
- Ensure all required fields (*) are filled
- Check browser console for error messages
- Check terminal for server errors

### Issue: Photo not displaying
- Clear browser cache
- Check if file exists in `/static/uploads/profiles/`
- Verify file permissions

---

## 📞 Support Information

For issues or questions:
1. Check database tables are created: `SHOW TABLES;`
2. Verify user is logged in: Check session data
3. Check server logs for detailed error messages
4. Ensure profile folders exist and are writable

---

**Setup Completed!** ✅

Profile pages are now fully integrated with your LMS system.
All data is automatically stored in your MySQL database.

Visit the profile pages in your browser to start updating user profiles!
