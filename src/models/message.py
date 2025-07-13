from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    received_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='new')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'message': self.message,
            'received_date': self.received_date.isoformat() if self.received_date else None,
            'status': self.status
        }

