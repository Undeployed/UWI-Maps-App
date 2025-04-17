from App.database import db
from datetime import datetime, timezone

class MarkerUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc))
    description = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, marker_id, description, date=None):
        self.user_id = user_id
        self.marker_id = marker_id
        self.description= description
        self.date = date or datetime.now(timezone.utc)

    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'marker_id': self.marker_id,
            'date': self.date.isoformat(),
            'description': self.description
        }
    
    def __repr__(self):
        return f"<MarkerUpdate {self.id} by User {self.user_id} on Marker {self.marker_id}>"
