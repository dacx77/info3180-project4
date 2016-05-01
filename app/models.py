from . import db 
from werkzeug.security import generate_password_hash, check_password_hash

class myprofile(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    url = db.Column(db.String)
    

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
        
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
        
    def __repr__(self):
        return '{%s : %d}' % ("User", self.id)