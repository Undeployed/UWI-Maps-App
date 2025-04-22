from App.database import db
from datetime import time, datetime

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False, default=1)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    open_time = db.Column(db.Time, nullable=True)
    close_time = db.Column(db.Time, nullable=True)

    updates = db.relationship('MarkerUpdate', backref='marker', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, campus_id, category_id, description, latitude, longitude, image, faculty_id=None, open_time=None, close_time=None):
        self.campus_id= campus_id
        self.name = name
        self.faculty_id=faculty_id
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.category_id = category_id
        self.image = image
        self.open_time = self.parse_time(open_time) if open_time else None
        self.close_time = self.parse_time(close_time) if close_time else None
    
    def parse_time(self, time_input):
        if isinstance(time_input, time):
            return time_input
        if not time_input:
            return None
        try:
            return datetime.strptime(time_input.strip().upper(), "%I:%M %p").time()
        except ValueError:
            try:
                return datetime.strptime(time_input.strip(), "%H:%M").time()
            except ValueError:
                print(f"[WARN] Invalid time format: '{time_input}'")
                return None
    
    def format_time(self, time_obj):
        if not time_obj:
            return None
        return time_obj.strftime("%I:%M %p").lstrip("0").replace("AM", "am").replace("PM", "pm")


    def get_json(self):
        return {
            'id': self.id,
            'campus': self.campus.name,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'faculty': self.faculty.get_json() if self.faculty else None,
            'category': self.category.get_json(),
            'image': self.image,
            'open_time': self.format_time(self.open_time),
            'close_time': self.format_time(self.close_time),
            'updates': [update.get_json() for update in self.updates]
        }
    
    def __repr__(self):
        return f"<Marker {self.id} - {self.name} @ ({self.latitude}, {self.longitude})>"