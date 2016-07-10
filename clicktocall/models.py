from . import db

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    messagetext = db.Column(db.String(128), nullable=False)