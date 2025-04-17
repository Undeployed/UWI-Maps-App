from App.models import Campus
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_campus(name, location, sw_bound, ne_bound):
    try:
        campus = Campus(name=name, location=location, sw_bound=sw_bound, ne_bound=ne_bound)
        db.session.add(campus)
        db.session.commit()
        return campus
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating campus:", e)
        return None
    
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
        campus.sw_bound = data.get('sw_bound', campus.sw_bound)
        campus.ne_bound = data.get('ne_bound', campus.ne_bound)
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