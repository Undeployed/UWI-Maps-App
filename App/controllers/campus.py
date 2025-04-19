import csv
from App.models import Campus
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_campus(name, location, sw_lat, sw_lng, ne_lat, ne_lng):
    try:
        campus = Campus(name=name, location=location, sw_lat=sw_lat, sw_lng=sw_lng, ne_lat=ne_lat, ne_lng=ne_lng)
        db.session.add(campus)
        db.session.commit()
        return campus
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating campus:", e)
        return None

def parse_campus_csv(file_path):
    with open(file_path, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        campuses = []
        for row in reader:
            campus = Campus(name=row['name'], location=row['location'], sw_lat=row['sw_lat'], sw_lng=row['sw_lng'], ne_lat=row['ne_lat'], ne_lng=row['ne_lng'])
            campuses.append(campus)
        
        try:
            db.session.add_all(campuses)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error parsing campuses", e)
            return False
           
def get_all_campuses():
    return Campus.query.all()

def get_campus(campus_id):
    return Campus.query.get(campus_id)

def update_campus(campus_id, data):
    campus = get_campus(campus_id)
    if not campus:
        return None
    
    try:
        campus.name = data.get('name', campus.name)
        campus.location = data.get('location', campus.location)
        campus.sw_lat = data.get('sw_lat', campus.sw_lat)
        campus.sw_lng = data.get('sw_lng', campus.sw_lng)
        campus.ne_lat = data.get('ne_lat', campus.ne_lat)
        campus.ne_lng = data.get('ne_lng', campus.ne_lng)
        db.session.commit()
        return campus
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating campus:", e)
        return None
    
def delete_campus(campus_id):
    campus = get_campus(campus_id)
    if not campus:
        return False
    
    try:
        db.session.delete(campus)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleteing campus:", e)
        return False