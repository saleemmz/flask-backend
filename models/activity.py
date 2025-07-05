from datetime import datetime, timezone
from extensions import db

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., login, profile, password, task, file, user
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))  # UTC-aware

    user = db.relationship('User', backref='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.full_name if self.user else 'Unknown',
            'action': self.action,
            'category': self.category,
            # Send full ISO 8601 string in UTC
            'timestamp': self.timestamp.isoformat()
        }
