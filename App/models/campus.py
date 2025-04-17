from App.database import db

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    sw_bound = db.Column(db.Float, nullable=False)
    ne_boundary = db.Column(db.Float, nullable=False)

    markers = db.relationship('Marker', backref='campus', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, location, sw_bound, ne_bound):
        self.name = name
        self.location = location
        self.sw_bound = sw_bound
        self.ne_bound = ne_bound

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'sw_bound': self.sw_bound,
            'ne_boundary': self.ne_boundary
        }

    def __repr__(self):
        return f"<Campus {self.id} - {self.name}>"