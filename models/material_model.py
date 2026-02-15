"""Study materials model for database operations"""
from datetime import datetime


def add_material(cursor, title: str, subject: str, description: str, file_path: str, uploaded_by: int, approval_status: str = 'pending') -> dict:
    """
    Add a new study material
    
    Args:
        cursor: MySQL cursor
        title: Material title
        subject: Subject name
        description: Material description
        file_path: File path/URL
        uploaded_by: User ID of uploader
        approval_status: Initial approval status (pending/approved/rejected)
        
    Returns:
        Dictionary with result
    """
    try:
        cursor.execute(
            """INSERT INTO study_materials 
               (title, subject, description, file_path, uploaded_by, approval_status, upload_date, updated_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (title, subject, description, file_path, uploaded_by, approval_status, datetime.now(), datetime.now())
        )
        
        material_id = cursor.lastrowid
        return {"success": True, "material_id": material_id, "message": "Material uploaded successfully"}
    
    except Exception as e:
        print(f"Error adding material: {e}")
        return {"success": False, "message": str(e)}


def get_material(cursor, material_id: int) -> dict:
    """Get material by ID"""
    try:
        cursor.execute(
            "SELECT * FROM study_materials WHERE id = %s",
            (material_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting material: {e}")
        return None


def get_materials_by_subject(cursor, subject: str, approval_status: str = 'approved', limit: int = None) -> list:
    """Get materials by subject"""
    try:
        if limit:
            cursor.execute(
                "SELECT * FROM study_materials WHERE subject = %s AND approval_status = %s ORDER BY upload_date DESC LIMIT %s",
                (subject, approval_status, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM study_materials WHERE subject = %s AND approval_status = %s ORDER BY upload_date DESC",
                (subject, approval_status)
            )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting materials by subject: {e}")
        return []


def get_materials_by_uploader(cursor, uploaded_by: int) -> list:
    """Get all materials uploaded by a specific user"""
    try:
        cursor.execute(
            "SELECT * FROM study_materials WHERE uploaded_by = %s ORDER BY upload_date DESC",
            (uploaded_by,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting materials by uploader: {e}")
        return []


def get_all_materials(cursor, approval_status: str = None) -> list:
    """Get all materials, optionally filtered by approval status"""
    try:
        if approval_status:
            cursor.execute(
                "SELECT * FROM study_materials WHERE approval_status = %s ORDER BY upload_date DESC",
                (approval_status,)
            )
        else:
            cursor.execute(
                "SELECT * FROM study_materials ORDER BY upload_date DESC"
            )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting all materials: {e}")
        return []


def update_material(cursor, material_id: int, title: str = None, subject: str = None, 
                   description: str = None, approval_status: str = None) -> dict:
    """Update material details"""
    try:
        updates = []
        params = []
        
        if title:
            updates.append("title = %s")
            params.append(title)
        
        if subject:
            updates.append("subject = %s")
            params.append(subject)
        
        if description:
            updates.append("description = %s")
            params.append(description)
        
        if approval_status:
            updates.append("approval_status = %s")
            params.append(approval_status)
        
        updates.append("updated_date = %s")
        params.append(datetime.now())
        
        params.append(material_id)
        
        if updates:
            query = f"UPDATE study_materials SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, params)
        
        return {"success": True, "message": "Material updated successfully"}
    
    except Exception as e:
        print(f"Error updating material: {e}")
        return {"success": False, "message": str(e)}


def delete_material(cursor, material_id: int) -> dict:
    """Delete material from database"""
    try:
        cursor.execute("DELETE FROM study_materials WHERE id = %s", (material_id,))
        return {"success": True, "message": "Material deleted successfully"}
    
    except Exception as e:
        print(f"Error deleting material: {e}")
        return {"success": False, "message": str(e)}


def get_pending_materials(cursor) -> list:
    """Get all materials pending approval"""
    try:
        cursor.execute(
            "SELECT * FROM study_materials WHERE approval_status = 'pending' ORDER BY upload_date ASC"
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting pending materials: {e}")
        return []
