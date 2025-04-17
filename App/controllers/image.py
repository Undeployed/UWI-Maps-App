from App.models import Image
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def add_image(marker_id, url):
    try:
        image = Image(marker_id=marker_id, url=url)
        db.session.add(image)
        db.session.commit()
        return image
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating image:", e)
        return None

def get_marker_images(marker_id):
    return Image.query.filter_by(marker_id=marker_id).all()

def get_image(id):
    return Image.query.get(id)

def delete_image(id):
    image = get_image(id)
    if not image:
        return False
    
    try:
        db.session.delete(image)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting image", e)
        return False
