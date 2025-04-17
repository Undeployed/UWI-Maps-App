from App.models import User
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_user(username, password, role='admin'):
    try:
        newuser = User(username=username, password=password, role=role)
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error creating user:", e)
        return None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    return [user.get_json() for user in users]

def update_user(id, data):
    user = get_user(id)
    if not user or not data:
        return None
    
    try:
         user.username = data.get('username', user.username)
         user.role = data.get('role', user.role)
         db.session.commit()
         return user
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error updating user:", e)
        return None
    
def delete_user(id):
    user = get_user(id)
    if not user:
        return False
    
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error deleting user:", e)
        return False