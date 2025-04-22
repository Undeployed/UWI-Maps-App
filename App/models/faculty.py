from App.database import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    markers = db.relationship('Marker', backref='faculty', lazy=True)

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return f"<Faculty {self.id} - {self.name}>"