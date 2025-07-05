from datetime import datetime, timezone
from extensions import db
from sqlalchemy import func
from utils.activitylogger import log_activity
import os
from flask import current_app

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime(timezone=True), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='incompleted', nullable=False)
    
    # Relationships
    assignees = db.relationship('User', secondary='task_assignees', backref='tasks')
    files = db.relationship('File', backref='task', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='task', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'status': self.status,
            'assignees': [user.to_dict() for user in self.assignees],
            'files': [file.to_dict() for file in self.files]
        }

class TaskAssignee(db.Model):
    __tablename__ = 'task_assignees'
    
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    assigned_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    is_encrypted = db.Column(db.Boolean, default=False, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    file_size = db.Column(db.BigInteger, default=0)  # Store actual file size in bytes
    
    # Relationships
    uploaded_by_user = db.relationship('User', backref='uploaded_files', foreign_keys=[uploaded_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'is_encrypted': self.is_encrypted,
            'task_id': self.task_id,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat(),
            'file_size': self.file_size
        }
        
    def get_full_path(self):
        """Get the absolute file path"""
        return os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            self.file_path
        )

    def get_formatted_size(self):
        """Get human readable file size"""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{round(self.file_size / 1024, 1)} KB"
        else:
            return f"{round(self.file_size / (1024 * 1024), 1)} MB"

class Key(db.Model):
    __tablename__ = 'keys'
    
    id = db.Column(db.Integer, primary_key=True)
    encryption_key = db.Column(db.String(256), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class KeyHolder(db.Model):
    __tablename__ = 'key_holders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key_id = db.Column(db.Integer, db.ForeignKey('keys.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True) 
    assigned_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Add relationship to User
    user = db.relationship('User', backref='comments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'comment_text': self.comment_text,
            'created_at': self.created_at.isoformat(),
            'user': self.user.to_dict() if self.user else None
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False) 
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    related_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    read_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    user = db.relationship('User', backref='notifications')
    task = db.relationship('Task', backref='notifications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
            'task_id': self.related_task_id,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
