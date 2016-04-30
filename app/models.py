from . import db  

class myprofile(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String)
    url = db.Column(db.String)
    

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