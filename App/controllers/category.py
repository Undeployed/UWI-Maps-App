import csv
from App.models import Category
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_category(name, color):
    try:
        category = Category(name, color)
        db.session.add(category)
        db.session.commit()
        return category
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating category:", e)
        return None
    
def parse_category_csv(file_path):
    with open(file_path, newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        categories = []
        for row in reader:
            category = Category(name=row['name'], color=row['color'])
            categories.append(category)
        
        try:
            db.session.add_all(categories)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error parsing categories", e)
            return False
    
def get_all_categories():
    return Category.query.all()

def get_category(category_id):
    return Category.query.get(category_id)

def get_category_by_name(name):
    return Category.query.filter_by(name=name).first()

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