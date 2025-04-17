from App.models import MarkerCategory
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def add_marker_category(category_id, marker_id):
    try:
        category = MarkerCategory(category_id=category_id, marker_id=marker_id)
        db.session.add(category)
        db.session.commit()
        return category
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error adding category:", e)
        return None

def get_marker_category(id):
    return MarkerCategory.query.get(id)

def delete_marker_category(id):
    marker_category = get_marker_category(id)
    if not marker_category:
        return False
    
    try:
        db.session.delete(marker_category)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting marker category:", e)
        return False