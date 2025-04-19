import csv
from App.models import Marker, MarkerUpdate
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_marker(user_id, name, campus_id, cateogry_id, description, latitude, longitude, image="https://placeholder.pics/svg/150"):
    from  App.controllers import add_marker_update # Avoid Circular Dependency

    try:
        marker = Marker(name=name, campus_id=campus_id, category_id=cateogry_id, description=description, latitude=latitude, longitude=longitude, image=image)
        db.session.add(marker)
        db.session.commit()

        # Add a marker update on creation
        add_marker_update(user_id=user_id, 
                          marker_id=marker.id,
                          description=f'Created new marker: "{marker.name}"'
                          )
        
        return marker
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating marker:", e)
        return None

def parse_marker_csv(user_id, file_path):
    from .category import get_category_by_name
    from .campus import get_campus_by_name
    with open(file_path, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        markers = []
        for row in reader:
            category = get_category_by_name(row['category'])
            campus = get_campus_by_name(row['campus'])
            image = row['image'] if row['image'] != "" else "https://placeholder.pics/svg/150"
            marker = Marker(name=row['name'], campus_id=campus.id, category_id=category.id, description=row['description'], latitude=row['latitude'], longitude=row['longitude'], image=image)
            markers.append(marker)
        
        try:
             # Add all markers first (without committing)
            db.session.add_all(markers)
            db.session.flush()  # Assigns marker IDs without committing

            # Now that marker IDs exist, add updates
            for marker in markers:
                update = MarkerUpdate(
                    user_id=user_id,
                    marker_id=marker.id,
                    description=f'Created new marker: "{marker.name}"'
                )
                db.session.add(update)

            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error parsing markers", e)
            return False
        
def get_all_markers():
    return Marker.query.all()

def get_marker(marker_id):
    return Marker.query.get(marker_id)

def get_all_markers_for_campus(campus_id):
    return Marker.query.filter_by(campus_id=campus_id).all()

def get_all_markers_for_campus_json(campus_id):
    markers = [marker.get_json() for marker in get_all_markers_for_campus(campus_id=campus_id)]
    return markers

def get_all_markers_filtered_json(campus_id, filters):
    filters = [int(fid) for fid in filters] # convert to int (safety)
    markers = Marker.query.filter(Marker.campus_id == campus_id, Marker.category_id.in_(filters))
    return [marker.get_json() for marker in markers]
    

def update_marker(marker_id, data):
    marker = get_marker(marker_id)
    if not marker:
        return None
    
    try:
        marker.name = data.get('name', marker.name)
        marker.campus_id = data.get('campus_id', marker.campus_id)
        marker.category_id = data.get('category_id', marker.category_id)
        marker.description = data.get('description', marker.description)
        marker.latitude = data.get('latitude', marker.latitude)
        marker.longitude = data.get('longitude', marker.longitude)
        marker.image = data.get('image', marker.image)
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