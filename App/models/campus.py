from App.database import db

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lng = db.Column(db.Float, nullable=False)
    ne_lat = db.Column(db.Float, nullable=False)
    ne_lng = db.Column(db.Float, nullable=False)

    markers = db.relationship('Marker', backref='campus', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, location, sw_lat, sw_lng, ne_lat, ne_lng):
        self.name = name
        self.location = location
        self.sw_lat = sw_lat
        self.sw_lng = sw_lng
        self.ne_lat = ne_lat
        self.ne_lng = ne_lng

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'sw_bound': {'latitude': self.sw_lat, 'longitude': self.sw_lng},
            'ne_boundary': {'latitude': self.ne_lat, 'longitude': self.ne_lng}
        }

    def __repr__(self):
        return f"<Campus {self.id} - {self.name}>"