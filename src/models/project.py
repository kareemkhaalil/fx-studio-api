from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # JSON string for multiple tags
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='active')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'video_url': self.video_url,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'status': self.status
        }

