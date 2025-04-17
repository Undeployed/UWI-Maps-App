from App.database import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    markers = db.relationship('MarkerCategory', backref='category', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f"<Category {self.id} - {self.name}>"
