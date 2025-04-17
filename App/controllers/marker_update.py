from App.models import MarkerUpdate
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def add_marker_update(user_id, marker_id, description, date=None):
    try:
        update = MarkerUpdate(user_id=user_id, marker_id=marker_id, description=description, date=date)
        db.session.add(update)
        db.session.commit()
        return update
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating MarkerUpdate:", e)
        return None 

def get_all_marker_updates(marker_id):
    return MarkerUpdate.query.filter_by(marker_id=marker_id).all()

def get_marker_updates_from_user(marker_id, user_id):
    return MarkerUpdate.query.filter_by(marker_id=marker_id, user_id=user_id).all()

def get_all_user_updates(user_id):
    return MarkerUpdate.query.filter_by(user_id=user_id).all()

def get_marker_update(id):
    return MarkerUpdate.query.get(id)


def update_marker_update(id, data):
    update = get_marker_update(id)
    if not update:
        return None
    
    try:
        update.description = data.get('description', update.description)
        update.date = data.get('date', update.date)
        db.session.commit()
        return update
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating MarkerUpdate:", e)
        return None

def delete_marker_update(id):
    update = get_marker_update(id)
    if not update:
        return False
    
    try:
        db.session.delete(update)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting MarkerUpdate:", e)
        return False


