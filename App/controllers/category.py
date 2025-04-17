from App.models import Category, MarkerCategory
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_category(name):
    try:
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        return category
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating category:", e)
        return None
    
def get_all_categories():
    return Category.query.all()

def get_category(category_id):
    return Category.query.get(category_id)

def get_category_by_name(name):
    return Category.query.filter_by(name=name).first()

def get_markers_by_category(category_id):
    marker_categories = MarkerCategory.query.filter_by(category_id=category_id)
    return [marker_category.marker for marker_category in marker_categories]

def update_category(category_id, name):
    category = get_category(category_id)
    if not category:
        return None
    
    try:
        category.name = name
        db.session.commit()
        return category
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating category:", e)
        return None
    
def delete_category(category_id):
    category = get_category(category_id)
    if not category:
        return False
    
    try:
        db.session.delete(category)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting category:", e)
        return False