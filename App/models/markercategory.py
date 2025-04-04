from App.database import db

class MarkerCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), nullable=False)

    def __init__(self, category_id, marker_id):
        self.category_id= category_id
        self.marker_id = marker_id


    def get_json(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'marker_id': self.marker_id
        }
