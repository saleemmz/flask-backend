from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, UserPreference
from models.task import Notification
from flask_mail import re
from extensions import db
from utils.sendnotification import send_email_notification
from utils.activitylogger import log_activity
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

def handle_session_expired():
    """Helper function to return consistent session expired response"""
    return jsonify({
        'error': 'Session expired',
        'message': 'Your login session has expired. Please login again.',
        'action': 'login_required',
        'redirect': '/login'
    }), 401

@settings_bp.route('/account', methods=['GET'])
@jwt_required()
def get_account_settings():
    """Get current user's account settings"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "email": user.email,
            "account_created": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None
        }), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        return jsonify({'error': 'Failed to fetch account settings'}), 500

@settings_bp.route('/update-email', methods=['POST'])
@jwt_required()
def update_email():
    """Update user's email address"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        new_email = data.get('email')
        
        if not new_email:
            return jsonify({"error": "Email is required"}), 400
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Check if email is already in use
        existing_user = User.query.filter(User.email == new_email, User.id != user_id).first()
        if existing_user:
            return jsonify({"error": "Email already in use"}), 400
        
        # Update email
        old_email = user.email
        user.email = new_email
        
        # Create notification
        notification = Notification(
            user_id=user_id,
            title="Email Changed",
            message=f"Your email address was changed from {old_email} to {new_email}",
            notification_type="account_change",
            created_at=datetime.utcnow()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Send notification to old email (always send security notifications)
        subject = "Email Address Changed"
        message = f"""Hello {user.full_name},
        
Your email address has been changed from {old_email} to {new_email}.

If you didn't make this change, please contact support immediately.
"""
        send_email_notification(old_email, subject, message)
        
        # Send confirmation to new email
        confirmation_subject = "Email Address Update Confirmation"
        confirmation_message = f"""Hello {user.full_name},
        
This email confirms that your account's email address has been successfully updated to this address.
"""
        send_email_notification(new_email, confirmation_subject, confirmation_message)
        
        return jsonify({"message": "Email updated successfully"}), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        return jsonify({'error': 'Failed to update email'}), 500

@settings_bp.route('/update-password', methods=['POST'])
@jwt_required()
def update_password():
    """Update user's password"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')
        
        if not all([current_password, new_password, confirm_password]):
            return jsonify({"error": "All password fields are required"}), 400
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({"error": "Current password is incorrect"}), 401
        
        # Verify new passwords match
        if new_password != confirm_password:
            return jsonify({"error": "New passwords do not match"}), 400
        
        # Set new password
        try:
            user.password = new_password
            
            # Create notification
            notification = Notification(
                user_id=user_id,
                title="Password Changed",
                message="Your account password was successfully updated",
                notification_type="account_change",
                created_at=datetime.utcnow()
            )
            
            
            db.session.add(notification)
            db.session.commit()
            
            # Always send security notifications regardless of email preference
            subject = "Password Changed"
            message = f"""Hello {user.full_name},
            
Your password has been successfully changed.

If you didn't make this change, please contact support immediately.
"""
            send_email_notification(user.email, subject, message)
            
            return jsonify({"message": "Password updated successfully"}), 200
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        return jsonify({'error': 'Failed to update password'}), 500

@settings_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    """Get user's notification preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get or create user preferences
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        if not preference:
            # Create default preferences
            preference = UserPreference(
                user_id=user_id,
                email_notifications=True  # Default to enabled
            )
            
            db.session.add(preference)
            db.session.commit()
            
            log_activity(
                user_id=user.id,
                action=f"Successfully reset password",
                category="password"
            )
        
        return jsonify({
            "email_notifications": preference.email_notifications,
            "created_at": preference.created_at.isoformat(),
            "updated_at": preference.updated_at.isoformat()
        }), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        return jsonify({'error': 'Failed to fetch notification preferences'}), 500

@settings_bp.route('/notifications', methods=['POST'])
@jwt_required()
def update_notification_preferences():
    """Update user's notification preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        email_notifications = data.get('email_notifications', False)
        
        # Get or create user preferences
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        if not preference:
            preference = UserPreference(
                user_id=user_id,
                email_notifications=email_notifications
            )
            db.session.add(preference)
        else:
            preference.email_notifications = email_notifications
            preference.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create notification about preference change
        notification = Notification(
            user_id=user_id,
            title="Notification Preferences Updated",
            message=f"Email notifications {'enabled' if email_notifications else 'disabled'}",
            notification_type="account_change",
            created_at=datetime.utcnow()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            "message": "Notification preferences updated successfully",
            "email_notifications": email_notifications
        }), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        return jsonify({'error': 'Failed to update notification preferences'}), 500

@settings_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_account_activity():
    """Get recent account activity and changes"""
    try:
        user_id = get_jwt_identity()
        
        notifications = Notification.query.filter(
            Notification.user_id == user_id,
            Notification.notification_type == "account_change"
        ).order_by(Notification.created_at.desc()).limit(10).all()
        
        return jsonify({
            "activity": [{
                "title": n.title,
                "message": n.message,
                "timestamp": n.created_at.isoformat()
            } for n in notifications]
        }), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        return jsonify({'error': 'Failed to fetch account activity'}), 500
