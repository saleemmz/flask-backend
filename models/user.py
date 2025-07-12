from datetime import datetime, timedelta
from extensions import db
import re
from sqlalchemy import func
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship(
        'User',
        backref=db.backref('preference', uselist=False, passive_deletes=True),
        passive_deletes=True
    )


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False, default='')
    last_name = db.Column(db.String(60), nullable=False, default='')
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True, default=None)
    _password = db.Column('password', db.String(256), nullable=False)
    bio = db.Column(db.Text, nullable=True, default=None)
    position = db.Column(db.String(60), nullable=True, default='Staff')
    company_name = db.Column(db.String(120), nullable=True, default=None)
    avatar_url = db.Column(db.String(255), nullable=True, default=None)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), default='staff', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    verifications = db.relationship(
        'Verification',
        backref=db.backref('user_ref', passive_deletes=True),
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        error = self.validate_password(password)
        if error:
            raise ValueError(error)
        self._password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        logger.info(f"Password set for user {self.username}")

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if len(password) > 128:
            return "Password must be less than 128 characters."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one number."
        if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password):
            return "Password must contain at least one special character."
        if re.search(r"(.)\1{2,}", password):
            return "Password contains repeating characters."
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'bio': self.bio,
            'position': self.position,
            'company_name': self.company_name,
            'avatar_url': self.avatar_url,
            'is_verified': self.is_verified,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def record_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
        logger.info(f"Recorded login for user {self.username}")

    @classmethod
    def get_unverified_by_email(cls, email):
        return cls.query.filter(
            func.lower(cls.email) == func.lower(email),
            cls.is_verified == False
        ).first()

    @classmethod
    def get_by_username_or_email(cls, identifier):
        return cls.query.filter(
            (func.lower(cls.username) == func.lower(identifier)) |
            (func.lower(cls.email) == func.lower(identifier))
        ).first()

    def verify_email(self):
        self.is_verified = True
        Verification.query.filter_by(user_id=self.id).delete()
        db.session.commit()
        logger.info(f"User {self.username} verified email")


class Verification(db.Model):
    __tablename__ = 'verifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    code = db.Column(db.String(6), nullable=False)
    method = db.Column(db.String(20), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    attempts = db.Column(db.Integer, default=0, nullable=False)

    __table_args__ = (
        db.Index('idx_user_method', 'user_id', 'method'),
    )

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.code = kwargs.get('code', ''.join(random.choices(string.digits, k=6)))
        self.method = kwargs.get('method', 'email')
        self.expires_at = kwargs.get('expires_at', datetime.utcnow() + timedelta(minutes=30))
        self.attempts = kwargs.get('attempts', 0)

    def is_valid(self):
        return datetime.utcnow() < self.expires_at and self.attempts < 3

    def increment_attempts(self):
        self.attempts += 1
        db.session.commit()
        logger.info(f"Incremented attempts for verification {self.id}")

    @classmethod
    def create_for_password_reset(cls, user_id, code=None):
        cls.query.filter_by(user_id=user_id, method='password_reset').delete()
        verification = cls(
            user_id=user_id,
            code=code or ''.join(random.choices(string.digits, k=6)),
            method='password_reset',
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )
        db.session.add(verification)
        db.session.commit()
        logger.info(f"Created password reset code for user {user_id}")
        return verification

    @classmethod
    def get_valid_code(cls, user_id, code, method):
        return cls.query.filter(
            cls.user_id == user_id,
            cls.code == code,
            cls.method == method,
            cls.expires_at > datetime.utcnow(),
            cls.attempts < 3
        ).first()
