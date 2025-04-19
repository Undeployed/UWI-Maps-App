from App.database import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=False, default="#555555")

    markers = db.relationship('Marker', backref='category', lazy=True)

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }

    def __repr__(self):
        return f"<Category {self.id} - {self.name} {self.color}>"