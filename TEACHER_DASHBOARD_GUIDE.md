# Teacher Dashboard with Course Management - Setup Guide

## 🎓 What's Been Implemented

### Teacher Dashboard Features:

#### 1. **Course Details Display**
- Shows assigned course name and code
- Displays material count
- Shows active status
- Quick stats dashboard

#### 2. **File Upload Functionality**
- Drag & drop or click to upload
- Support for multiple file types:
  - Documents: PDF, DOC, DOCX
  - Presentations: PPT, PPTX
  - Spreadsheets: XLS, XLSX
  - Archives: ZIP
  - Images: JPG, PNG, GIF
  - Text: TXT
- Maximum file size: 16MB
- Required: Title (Optional: Description)

#### 3. **Material Management**
- View all uploaded materials in a table
- Download materials
- Delete materials
- See upload date and description
- Material count display

---

## 🚀 How to Use

### For Teachers:

1. **Login** with teacher credentials
   - Email: teacher@lms.com
   - Password: password123

2. **Go to Dashboard**
   - View your assigned course details
   - See material count and status

3. **Upload Materials**
   - Click "Upload Course Material"
   - Enter title (required)
   - Add description (optional)
   - Select file
   - Click "Upload Material"

4. **Manage Materials**
   - View all uploaded materials
   - Download anytime
   - Delete if needed

---

## 📁 Course Details Section

```
📖 Course Name
- Course Code: CS-101
- Materials Uploaded: 5
- Status: Active
```

Shows:
- Course name in large, clear text
- Course code for reference
- Number of materials uploaded
- Current status (Active/Inactive)

---

## 📤 Upload Section

**Features:**
- Drag & drop interface
- File type validation
- Size validation (max 16MB)
- Title field (required)
- Description field (optional)
- Progress indicator during upload
- Success/error notifications

**Supported File Types:**
- PDF (*.pdf)
- Word Documents (*.doc, *.docx)
- PowerPoint (*.ppt, *.pptx)
- Excel (*.xls, *.xlsx)
- ZIP Archives (*.zip)
- Text (*.txt)
- Images (*.jpg, *.png, *.gif)

---

## 📚 Materials Management

### View Materials:
- Table showing all uploaded materials
- Columns:
  - 📄 Title (name of material)
  - 📝 Description (if provided)
  - 📅 Upload Date (when uploaded)
  - ⚙️ Actions (Download/Delete)

### Actions:
- **Download** (📥) - Download the file to your computer
- **Delete** (🗑️) - Remove the material (requires confirmation)

---

## 🛠️ Backend Routes

### Upload Material:
```
POST /teacher/upload-material
Body: FormData {
  file: File,
  title: string,
  description: string
}
Response: { success: boolean, message: string }
```

### Delete Material:
```
POST /teacher/delete-material/<material_id>
Response: { success: boolean, message: string }
```

### Load Dashboard:
```
GET /teacher/dashboard
Query: Loads user's course and materials
```

---

## 💾 Database Integration

### Materials Stored With:
- Material ID
- Title
- Description (optional)
- File path (stored in `/static/uploads/`)
- Course ID
- Uploaded by (teacher)
- Upload date and time
- Update date and time

### Course Information:
- Linked to course table
- Shows course name and code
- Displays to assigned teacher only

---

## ✨ Features

✅ **Course Context** - Shows which course teacher is managing
✅ **File Upload** - Easy drag & drop upload
✅ **File Management** - Download and delete materials
✅ **Progress Indication** - Shows upload progress
✅ **Validation** - File type and size validation
✅ **Error Handling** - Clear error messages
✅ **Responsive Design** - Works on desktop and mobile
✅ **Material Organization** - Table view of all materials
✅ **Quick Stats** - Material count and status

---

## 🔒 File Storage

**Location:** `/static/uploads/`

**File Naming Convention:**
```
course_{course_id}_{user_id}_{original_filename}
Example: course_13_5_chapter1.pdf
```

**File Path in Database:**
```
/static/uploads/course_13_5_chapter1.pdf
```

---

## 🧪 Testing the System

1. **Start Flask Server**
   - Already running on `http://localhost:5000`

2. **Login as Teacher**
   - Email: teacher@lms.com
   - Password: password123

3. **Access Dashboard**
   - URL: `http://localhost:5000/teacher-dashboard`
   - View course details

4. **Upload a File**
   - Click upload area
   - Select a file (PDF, DOC, etc.)
   - Enter title and optional description
   - Click "Upload Material"
   - See confirmation message
   - Material appears in table

5. **Manage Materials**
   - Download by clicking download button
   - Delete by clicking delete button (confirm deletion)

---

## 📊 Material Count

- Automatically counts all materials for the course
- Updates on page load
- Displayed in dashboard header
- Updates after upload/delete

---

## 🎨 UI/UX Features

- **Gradient Headers** - Professional gradient backgrounds
- **Icons** - Visual icons for better UX
- **Color-coded Actions** - Green for download, Red for delete
- **Hover Effects** - Interactive elements respond to hover
- **Loading States** - Shows during upload
- **Success/Error Messages** - Clear feedback to user
- **Responsive Layout** - Works on all screen sizes

---

## 🔗 Navigation

From Dashboard:
- 🏠 Dashboard - Current page
- 📤 Upload Materials - Same page (scroll)
- 👤 My Profile - `/teacher/profile`
- 🚪 Logout - `/auth/logout`

---

## ✅ Complete Teacher Workflow

1. Teacher logs in
2. Redirected to `/teacher-dashboard`
3. Sees their assigned course details
4. Can upload new materials
5. Can view all uploaded materials
6. Can download any material
7. Can delete materials
8. Can access profile and logout

All data is automatically stored in the MySQL database!

---

**Setup Complete!** 🎉

Your teacher dashboard is now fully functional with:
- ✅ Course details display
- ✅ File upload capability
- ✅ Material management
- ✅ Database integration
- ✅ Professional UI

Teachers can now manage their course materials efficiently!
