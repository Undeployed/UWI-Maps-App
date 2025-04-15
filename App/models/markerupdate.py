from App.database import db

class MarkerUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, marker_id, date, description):
        self.user_id = user_id
        self.marker_id = marker_id
        self.date = date
        self.description= description

    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'marker_id': self.marker_id,
            'date': self.date.isoformat(),
            'description': self.description
        }
