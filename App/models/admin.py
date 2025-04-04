from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    marker_updates = db.relationship('MarkerUpdate', backref='admin', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
