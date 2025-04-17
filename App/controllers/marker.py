from App.models import Marker
from . import add_marker_update
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_marker(user_id, name, campus_id, description, latitude, longitude):
    try:
        marker = Marker(name=name, campus_id=campus_id, description=description, latitude=latitude, longitude=longitude)
        db.session.add(marker)
        add_marker_update(user_id=user_id, 
                          marker_id=marker.id,
                          description=f'Created new marker: "{marker.name}"'
                          )
        
        return marker
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating marker:", e)
        return None
    
def get_all_markers():
    return Marker.query.all()

def get_marker(marker_id):
    return Marker.query.get(marker_id)

def update_marker(marker_id, data):
    marker = get_marker(marker_id)
    if not marker:
        return None
    
    try:
        marker.name = data.get('name', marker.name)
        marker.campus_id = data.get('campus_id', marker.campus_id)
        marker.description = data.get('description', marker.description)
        marker.latitude = data.get('latitude', marker.latitude)
        marker.lonitude = data.get('longitude', marker.longitude)
        db.session.commit()
        return marker
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating marker:", e)
        return None

def delete_marker(marker_id):
    marker = get_marker(marker_id)
    if not marker:
        return False
    
    try:
        db.session.delete(marker)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting marker:", e)
        return False