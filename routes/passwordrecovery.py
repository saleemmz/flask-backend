# passwordrecovery.py
from flask import Blueprint, request, jsonify, current_app
from extensions import db, mail
from models.user import User, Verification
from flask_mail import Message
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from datetime import datetime, timedelta
import random
import string
import logging
from email.utils import formataddr
import traceback
import jwt
from sqlalchemy import func, text
import re
import time
from utils.activitylogger import log_activity

password_recovery_bp = Blueprint('password_recovery', __name__)

# Configure logging
logger = logging.getLogger(__name__)

def is_valid_email(email):
    """More robust email validation"""
    if not email or len(email) > 254:
        return False
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def test_db_connection(max_retries=3, retry_delay=1):
    """Test database connection with retries"""
    for attempt in range(max_retries):
        try:
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Database connection failed after {max_retries} attempts: {str(e)}")
                return False
            time.sleep(retry_delay)
    return False

@password_recovery_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    try:
        # Verify database connection first with retries
        if not test_db_connection():
            logger.error("Database connection test failed")
            return jsonify({'error': 'Database connection failed'}), 500

        data = request.get_json()
        if not data:
            logger.error("No data received in request")
            return jsonify({'error': 'No data received'}), 400
            
        email = data.get('email', '').strip().lower()
        
        if not is_valid_email(email):
            logger.error(f"Invalid email format: {email}")
            return jsonify({'error': 'Valid email is required'}), 400

        logger.info(f"Password reset request for: {email}")

        # Find user with retry logic
        user = None
        for attempt in range(3):
            try:
                user = User.query.filter(
                    func.lower(User.email) == email,
                    User.is_verified == True
                ).first()
                break
            except Exception as query_error:
                logger.error(f"User query attempt {attempt+1} failed: {str(query_error)}")
                if attempt == 2:
                    logger.error(f"Database query error: {str(query_error)}")
                    return jsonify({'error': 'Database error occurred'}), 500
                time.sleep(0.5)

        # Always return success to prevent email enumeration
        if not user:
            logger.info(f"No verified user found for email: {email}")
            return jsonify({
                'message': 'If an account exists with this email, a reset code has been sent'
            }), 200

        # Transaction with proper error handling
        try:
            # Generate a new code
            code = ''.join(random.choices(string.digits, k=6))
            
            # Use the simplified method to create a verification code
            try:
                verification = Verification.create_for_password_reset(user.id, code)
                logger.info(f"Created new verification code for user {user.id}")
            except Exception as ver_error:
                logger.error(f"Error creating verification: {str(ver_error)}\n{traceback.format_exc()}")
                db.session.rollback()
                return jsonify({'error': 'Failed to create verification code'}), 500

            # Log password reset request activity
            log_activity(
                user_id=user.id,
                action=f"Requested password reset",
                category="password"
            )

            # Send email with retry logic
            email_sent = False
            for attempt in range(2):  # Try twice to send email
                try:
                    if send_password_reset_email(user, code):
                        email_sent = True
                        break
                    logger.warning(f"Email send attempt {attempt+1} failed without exception")
                except Exception as email_error:
                    logger.error(f"Email send attempt {attempt+1} failed with exception: {str(email_error)}")
                time.sleep(1)

            if not email_sent:
                db.session.rollback()
                logger.error(f"Failed to send email to {email} after 2 attempts")
                return jsonify({'error': 'Failed to send reset email'}), 500

            logger.info(f"Password reset code sent to {email}")
            return jsonify({
                'message': 'If an account exists with this email, a reset code has been sent',
                'email': user.email
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.error(f"Transaction error: {str(e)}\n{traceback.format_exc()}")
            return jsonify({'error': 'Failed to process reset request'}), 500

    except Exception as e:
        logger.error(f"Unexpected error in request_password_reset: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@password_recovery_bp.route('/verify-password-reset', methods=['POST'])
def verify_password_reset():
    try:
        if not test_db_connection():
            return jsonify({'error': 'Database connection failed'}), 500

        data = request.get_json()
        email = data.get('email', '').strip().lower()
        code = data.get('code', '').strip()

        if not email or not code:
            return jsonify({'error': 'Email and code are required'}), 400

        # Find user with retry
        user = None
        for attempt in range(3):
            try:
                user = User.query.filter(
                    func.lower(User.email) == email,
                    User.is_verified == True
                ).first()
                break
            except Exception as e:
                if attempt == 2:
                    logger.error(f"User query failed: {str(e)}")
                    return jsonify({'error': 'Database error'}), 500
                time.sleep(0.5)

        if not user:
            return jsonify({'error': 'Invalid request'}), 400

        # Find verification code using the helper method
        verification = Verification.get_valid_code(user.id, code, 'password_reset')
        
        if not verification:
            return jsonify({'error': 'Invalid or expired code'}), 400

        verification.increment_attempts()
        
        if not verification.is_valid():
            return jsonify({'error': 'Invalid or expired code'}), 400

        # Create reset token - simplified to use a string instead of a dictionary
        # This makes token handling more reliable
        reset_token = create_access_token(
            identity=f"reset_{user.id}_{user.email}",
            expires_delta=timedelta(minutes=30)  # Increased from 10 to 30 minutes
        )
        
        logger.info(f"Created reset token for user {user.id}: {reset_token[:10]}...")

        # Log password reset verification activity
        log_activity(
            user_id=user.id,
            action=f"Verified password reset code",
            category="password"
        )

        # Clean up
        try:
            db.session.delete(verification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Commit error: {str(e)}")
            return jsonify({'error': 'Failed to complete verification'}), 500

        return jsonify({
            'reset_token': reset_token,
            'message': 'Code verified. You can now reset your password.'
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Verification error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'Password reset verification failed'}), 500

@password_recovery_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        if not test_db_connection():
            return jsonify({'error': 'Database connection failed'}), 500

        data = request.get_json()
        reset_token = data.get('reset_token')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not all([reset_token, new_password, confirm_password]):
            return jsonify({'error': 'All fields are required'}), 400

        if new_password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        # Verify token with better error handling
        try:
            logger.info(f"Attempting to decode token: {reset_token[:10]}...")
            token_data = decode_token(reset_token)
            identity = token_data['sub']

            if not isinstance(identity, str) or not identity.startswith("reset_"):
                logger.error(f"Invalid token format: {identity}")
                return jsonify({'error': 'Invalid token format'}), 400

            parts = identity.split('_', 2)
            if len(parts) != 3:
                logger.error(f"Invalid token parts: {parts}")
                return jsonify({'error': 'Invalid token format'}), 400

            user_id = int(parts[1])
            user_email = parts[2]

            logger.info(f"Extracted user_id: {user_id}, email: {user_email}")
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}\n{traceback.format_exc()}")
            return jsonify({'error': 'Invalid or expired token'}), 400

        # Find user with explicit query
        user = db.session.query(User).filter_by(id=user_id).first()
        if not user:
            logger.error(f"User not found: {user_id}")
            return jsonify({'error': 'User not found'}), 400

        if user.email != user_email:
            logger.error(f"Email mismatch: token {user_email} vs db {user.email}")
            return jsonify({'error': 'Invalid user'}), 400

        # Set and persist password properly
        try:
            user.password = new_password  # Calls @password.setter
            db.session.add(user)
            db.session.flush()
            db.session.commit()

            log_activity(
                user_id=user.id,
                action="Successfully reset password",
                category="password"
            )

            logger.info(f"Password reset successful for user {user.email}")
            return jsonify({'message': 'Password reset successfully'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Password update failed: {str(e)}")
            return jsonify({'error': 'Failed to update password'}), 500

    except Exception as e:
        db.session.rollback()
        logger.error(f"Password reset error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'Password reset failed'}), 500

def send_password_reset_email(user, code):
    """Send password reset email with improved error handling"""
    for attempt in range(2):  # Try twice
        try:
            subject = "Password Reset Request"
            html = f"""<html>
                <body>
                    <h2>Password Reset</h2>
                    <p>Your verification code is: <strong>{code}</strong></p>
                    <p>This code will expire in 30 minutes.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                </body>
            </html>"""

            msg = Message(
                subject=subject,
                recipients=[user.email],
                sender=formataddr(("noreplyspt", "saleemm1137@gmail.com")),
                html=html
            )
            mail.send(msg)
            logger.info(f"Password reset email sent to {user.email}")
            return True
        except Exception as e:
            logger.warning(f"Email send attempt {attempt + 1} failed: {str(e)}")
            if attempt == 1:
                logger.error(f"Final email send failure: {traceback.format_exc()}")
    
    return False