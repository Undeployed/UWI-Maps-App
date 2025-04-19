from .user import create_user
from .campus import parse_campus_csv
from .category import parse_category_csv
from .marker import parse_marker_csv
from App.database import db

datafiles = './App/static/data_files'

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'admin')
    parse_campus_csv(f'{datafiles}/campuses.csv')
    parse_category_csv(f'{datafiles}/categories.csv')
    parse_marker_csv(1 , f'{datafiles}/markers.csv') # 1 is bob