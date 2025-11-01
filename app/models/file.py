from app.extensions import db 
from datetime import datetime



class File(db.Model):
    __tablename__ = 'files'
    id =  db.Column(db.Integer, primary_key= True)
    filename = db.Column(db.String(255), nullable=False,unique=True)
    filepath = db.Column(db.String(500), nullable = False, unique =True)
    mime_type = db.Column(db.String(50), nullable = False)
    size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default= datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    