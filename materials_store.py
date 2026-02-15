"""
Simple file-based storage for uploaded materials
"""
import json
import os
from datetime import datetime
from pathlib import Path

MATERIALS_FILE = 'materials_data.json'

def load_materials():
    """Load materials from JSON file"""
    if os.path.exists(MATERIALS_FILE):
        try:
            with open(MATERIALS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_materials(materials):
    """Save materials to JSON file"""
    with open(MATERIALS_FILE, 'w') as f:
        json.dump(materials, f, indent=2)

def add_material(title, description, filename, original_name, file_path, teacher_name="Teacher"):
    """Add a new material"""
    materials = load_materials()
    
    material = {
        'id': len(materials) + 1,
        'title': title,
        'description': description,
        'filename': filename,
        'original_name': original_name,
        'file_path': file_path,
        'teacher': teacher_name,
        'uploaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'downloads': 0
    }
    
    materials.append(material)
    save_materials(materials)
    return material

def get_all_materials():
    """Get all materials"""
    return load_materials()

def get_material(material_id):
    """Get a specific material"""
    materials = load_materials()
    for material in materials:
        if material['id'] == int(material_id):
            return material
    return None

def delete_material(material_id):
    """Delete a material"""
    materials = load_materials()
    materials = [m for m in materials if m['id'] != int(material_id)]
    save_materials(materials)
    return True

def increment_downloads(material_id):
    """Increment download count"""
    materials = load_materials()
    for material in materials:
        if material['id'] == int(material_id):
            material['downloads'] += 1
            break
    save_materials(materials)
