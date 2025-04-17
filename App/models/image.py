from App.database import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('marker.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __init__(self, marker_id, url):
        self.marker_id = marker_id
        self.url = url

    def get_json(self):
        return {
            'id': self.id,
            'marker_id': self.marker_id,
            'url': self.url
        }
    
    def __repr__(self):
        return f"<Image {self.id} for Marker {self.marker_id}>"