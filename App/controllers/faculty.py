import csv
from App.models import Faculty
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_faculty(name):
    try:
        faculty = Faculty(name)
        db.session.add(faculty)
        db.session.commit()
        return faculty
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating faculty:", e)
        return None
    
def parse_faculty_csv(file_path):
    with open(file_path, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        faculties = []
        for row in reader:
            faculty = Faculty(name=row['name'])
            faculties.append(faculty)
        
        try:
            db.session.add_all(faculties)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error parsing faculty", e)
            return False
    
def get_all_faculties():
    return Faculty.query.all()

def get_faculty(faculty_id):
    return Faculty.query.get(faculty_id)

def get_faculty_by_name(name):
    return Faculty.query.filter_by(name=name).first()

def update_faculty(faculty_id, name):
    faculty = get_faculty(faculty_id)
    if not faculty:
        return None
    
    try:
        faculty.name = name
        db.session.commit()
        return faculty
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating faculty:", e)
        return None
    
def delete_faculty(faculty_id):
    faculty = get_faculty(faculty_id)
    if not faculty:
        return False
    
    try:
        db.session.delete(faculty)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting faculty:", e)
        return False