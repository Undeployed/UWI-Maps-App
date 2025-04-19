from App.database import db

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False, default=1)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)

    marker_updates = db.relationship('MarkerUpdate', backref='marker', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, campus_id, category_id, description, latitude, longitude, image):
        self.campus_id= campus_id
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.category_id = category_id
        self.image = image

    def get_json(self):
        return {
            'id': self.id,
            'campus_id': self.campus_id,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category.get_json()
        }
    
    def __repr__(self):
        return f"<Marker {self.id} - {self.name} @ ({self.latitude}, {self.longitude})>"