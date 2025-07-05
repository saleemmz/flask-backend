from flask import Blueprint, request, jsonify, make_response
from extensions import db, mail
from models.user import User, Verification, UserPreference
from flask_mail import Message
from flask_jwt_extended import create_access_token
from utils.sendnotification import notify_new_user_signup
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    unset_jwt_cookies
)

from datetime import datetime, timedelta
import re
from sqlalchemy import func, exc
import logging
from utils.activitylogger import log_activity
import random
import string
import traceback
from flask_jwt_extended import set_access_cookies

auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_session_expired():
    """Helper function to return consistent session expired response"""
    return jsonify({
        'error': 'Session expired',
        'message': 'Your login session has expired. Please login again.',
        'action': 'login_required',
        'redirect': '/login'
    }), 401

def send_verification_email(user, code):
    try:
        if not user or not user.email:
            logger.error("Invalid user or missing email")
            return False
            
        subject = "Verify Your Email Address"
        body = f"""Please use the following code to verify your email:
        Verification Code: {code}
        Expires in 30 minutes"""
        
        html = f"""<html>
            <body>
                <p>Your verification code is: <strong>{code}</strong></p>
                <p>This code will expire in 30 minutes.</p>
            </body>
        </html>"""

        msg = Message(
            subject=subject,
            recipients=[user.email],
            sender=("noreplyspt", "noreply@SPT.com"),
            body=body,
            html=html
        )
        mail.send(msg)
        logger.info(f"Verification email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def send_login_verification_email(user, code):
    try:
        if not user or not user.email:
            logger.error("Invalid user or missing email")
            return False
            
        subject = "Login Verification Code"
        body = f"""Your login verification code is: {code}
        This code will expire in 10 minutes.
        If you did not request this code, please ignore this email."""
        
        html = f"""<html>
            <body>
                <p>Your login verification code is: <strong>{code}</strong></p>
                <p>This code will expire in 10 minutes.</p>
                <p>If you did not request this code, please ignore this email or contact support.</p>
            </body>
        </html>"""

        msg = Message(
            subject=subject,
            recipients=[user.email],
            sender=("noreplyspt", "noreply@SPT.com"),
            body=body,
            html=html
        )
        mail.send(msg)
        logger.info(f"Login verification email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send login verification email: {str(e)}")
        logger.error(traceback.format_exc())
        return False

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        import re  # Only if not already imported

        # Sanitize all input data
        data = sanitize_input(request.get_json())
        
        # Required fields check
        required = ['firstName', 'lastName', 'username', 'email', 'password']
        if not all(field in data for field in required):
            return jsonify({'error': 'All fields are required'}), 400

        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400

        # Validate password strength
        if not validate_password(data['password']):
            return jsonify({'error': 'Password must be at least 8 characters with uppercase, number, and special character'}), 400

        # Inline: Validate first name
        if not re.fullmatch(r'[A-Z][a-z]*', data['firstName']):
            return jsonify({'error': 'First name must start with a capital letter and contain only letters'}), 400

        # Inline: Validate last name
        if not re.fullmatch(r'[A-Z][a-z]*', data['lastName']):
            return jsonify({'error': 'Last name must start with a capital letter and contain only letters'}), 400

        # Inline: Validate username
        if not re.fullmatch(r'[a-z][a-z0-9]*', data['username']):
            return jsonify({'error': 'Username must contain only lowercase letters and numbers, starting with a letter'}), 400

        # Check if user exists (case-insensitive)
        existing_user = User.query.filter(
            (func.lower(User.email) == func.lower(data['email'])) | 
            (func.lower(User.username) == func.lower(data['username']))
        ).first()

        if existing_user:
            if not existing_user.is_verified:
                return jsonify({
                    'error': 'Account exists but is not verified.',
                    'action': 'resend_verification',
                    'email': existing_user.email,
                    'message': 'Please verify your email or request a new code.'
                }), 409
            return jsonify({'error': 'User already exists'}), 400

        try:
            # Create user
            user = User(
                first_name=data['firstName'].strip(),
                last_name=data['lastName'].strip(),
                username=data['username'].strip(),
                email=data['email'].strip().lower(),
                phone=data.get('phone'),
                is_verified=False
            )

            try:
                user.password = data['password']  # Hash password
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

            db.session.add(user)
            db.session.flush()  # This generates the user.id without committing

            # Create default user preferences with email notifications enabled
            user_preference = UserPreference(
                user_id=user.id,
                email_notifications=True  # Default to enabled for new users
            )
            db.session.add(user_preference)

            # Generate verification code
            verification = Verification(
                user_id=user.id,
                code=''.join(random.choices(string.digits, k=6)),
                method='email',
                expires_at=datetime.utcnow() + timedelta(minutes=10)
            )
            db.session.add(verification)

            if not send_verification_email(user, verification.code):
                db.session.rollback()
                return jsonify({'error': 'Failed to send verification email'}), 500

            db.session.commit()  # Commit all changes together
            logger.info(f"User registered successfully with default preferences: {user.email}")
            notify_new_user_signup(user.id)
            log_activity(user.id, "Registered new account", "user")

            return jsonify({'message': 'Verification code sent', 'email': user.email}), 200

        except exc.IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database integrity error: {str(e)}")
            return jsonify({'error': 'Username or email already exists'}), 400

    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        code = data.get('code', '').strip()

        if not email or not code:
            return jsonify({'error': 'Email and code are required'}), 400

        # Find unverified user
        user = User.query.filter(
            func.lower(User.email) == email,
            User.is_verified == False
        ).first()

        if not user:
            log_activity(None, f"Failed email verification (user not found): {email}", "user")
            return jsonify({'error': 'No unverified user found'}), 404

        verification = Verification.query.filter_by(
            user_id=user.id,
            method='email',
            code=code
        ).first()

        if not verification or not verification.is_valid():
            if verification:
                verification.increment_attempts()
                log_activity(None, "Failed code verification (invalid or expired code): {email}", "logout")
            return jsonify({'error': 'Invalid or expired code'}), 400

        # Mark as verified and clean up
        user.is_verified = True
        db.session.delete(verification)

        # Ensure user preferences exist (in case they were somehow missing)
        existing_preference = UserPreference.query.filter_by(user_id=user.id).first()
        if not existing_preference:
            user_preference = UserPreference(
                user_id=user.id,
                email_notifications=True  # Default to enabled
            )
            db.session.add(user_preference)
            logger.info(f"Created missing user preferences for user {user.id}")

        # Create session token - Using just the user ID as identity
        access_token = create_access_token(identity=str(user.id))
        user_data = user.to_dict()
        db.session.commit()  # Commit after accessing all user attributes

        return jsonify({
            'access_token': access_token,
            'user': user.to_dict(),
            'message': 'Email verified successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Verification error: {str(e)}")
        return jsonify({'error': 'Verification failed'}), 500

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        user = User.query.filter(
            func.lower(User.email) == email,
            User.is_verified == False
        ).first()

        if not user:
            log_activity(None, f"Failed email verification (user not found): {email}", "user")
            return jsonify({'error': 'No unverified user found'}), 404

        # Ensure user preferences exist (in case they were somehow missing)
        existing_preference = UserPreference.query.filter_by(user_id=user.id).first()
        if not existing_preference:
            user_preference = UserPreference(
                user_id=user.id,
                email_notifications=True  # Default to enabled
            )
            db.session.add(user_preference)
            logger.info(f"Created missing user preferences for user {user.id}")

        # Delete old codes and create new one
        Verification.query.filter_by(user_id=user.id, method='email').delete()
        verification = Verification(
            user_id=user.id,
            code=''.join(random.choices(string.digits, k=6)),
            method='email',
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )
        db.session.add(verification)

        if not send_verification_email(user, verification.code):
            db.session.rollback()
            return jsonify({'error': 'Failed to resend code'}), 500

        db.session.commit()
        return jsonify({
            'message': 'New verification code sent',
            'email': user.email
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Resend error: {str(e)}")
        return jsonify({'error': 'Failed to resend code'}), 500

@auth_bp.route('/request-login-code', methods=['POST'])
def request_login_code():
    try:
        # Sanitize all input data
        data = sanitize_input(request.get_json())
        if not data:
            return jsonify({'error': 'No data received'}), 400

        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember = data.get('remember', False)

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        # Find the user
        user = User.query.filter(
            func.lower(User.email) == email
        ).first()

        if not user:
            log_activity(None, f"Failed login attempt (invalid credentials): {email}", "logout")
            return jsonify({'error': 'Invalid credentials'}), 401

        # Check password
        if not user.check_password(password):
            log_activity(user.id if user else None, "Failed login attempt (invalid password)", "logout")
            return jsonify({'error': 'Invalid credentials'}), 401

        # Check if user is verified
        if not user.is_verified:
            return jsonify({'error': 'Account not verified. Please verify your account first.'}), 403

        # Ensure user preferences exist (for existing users who might not have preferences)
        existing_preference = UserPreference.query.filter_by(user_id=user.id).first()
        if not existing_preference:
            user_preference = UserPreference(
                user_id=user.id,
                email_notifications=True  # Default to enabled
            )
            db.session.add(user_preference)
            logger.info(f"Created missing user preferences for existing user {user.id}")

        # Generate a login verification code
        # Delete any existing login verification codes
        Verification.query.filter_by(user_id=user.id, method='login').delete()
        
        verification = Verification(
            user_id=user.id,
            code=''.join(random.choices(string.digits, k=6)),
            method='login',  
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        
        db.session.add(verification)
        db.session.commit()
        
        if not send_login_verification_email(user, verification.code):
            db.session.rollback()
            return jsonify({'error': 'Failed to send verification code'}), 500
        
        return jsonify({
            'message': 'Verification code sent',
            'email': user.email
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Login code request error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to process login request'}), 500

@auth_bp.route('/verify-login', methods=['POST'])
def verify_login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        code = data.get('code', '').strip()
        remember = data.get('remember', False)

        if not email or not code:
            return jsonify({'error': 'Email and code are required'}), 400

        # Find user
        user = User.query.filter(
            func.lower(User.email) == email,
            User.is_verified == True
        ).first()

        if not user:
            log_activity(None, f"Failed login verification (user not found): {email}", "logout")
            return jsonify({'error': 'User not found or not verified'}), 404

        # Find verification code
        verification = Verification.query.filter_by(
            user_id=user.id,
            method='login',
            code=code
        ).first()

        if not verification or not verification.is_valid():
            if verification:
                verification.increment_attempts()
            log_activity(None, f"Failed email verification (invalid or expired code): {email}", "logout")
            return jsonify({'error': 'Invalid or expired code'}), 400

        # Ensure user preferences exist (for existing users who might not have preferences)
        existing_preference = UserPreference.query.filter_by(user_id=user.id).first()
        if not existing_preference:
            user_preference = UserPreference(
                user_id=user.id,
                email_notifications=True  # Default to enabled
            )
            db.session.add(user_preference)
            logger.info(f"Created missing user preferences for existing user {user.id}")

        # Delete the verification code
        db.session.delete(verification)
    
         # Record login
        user.record_login()
        log_activity(user.id, "Logged in to the system", "login")

        # Create access token
        expires_delta = timedelta(days=2) if remember else timedelta(hours=6)
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=expires_delta
        )

        # Create response
        response = jsonify({
            'access_token': access_token,
            'user': user.to_dict(),
            'message': 'Login successful'
        })
        
        # Set the access token in a cookie
        set_access_cookies(response, access_token)
        
        db.session.commit()
        return response, 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Login verification error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Login verification failed'}), 500

@auth_bp.route('/resend-login-code', methods=['POST'])
def resend_login_code():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Find user
        user = User.query.filter(
            func.lower(User.email) == email,
            User.is_verified == True
        ).first()

        if not user:
            log_activity(None, f"Failed login verification (user not found): {email}", "logout")
            return jsonify({'error': 'User not found or not verified'}), 404

        # Verify password again for security
        if not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Ensure user preferences exist (for existing users who might not have preferences)
        existing_preference = UserPreference.query.filter_by(user_id=user.id).first()
        if not existing_preference:
            user_preference = UserPreference(
                user_id=user.id,
                email_notifications=True  # Default to enabled
            )
            db.session.add(user_preference)
            logger.info(f"Created missing user preferences for existing user {user.id}")

        # Delete old codes
        Verification.query.filter_by(user_id=user.id, method='login').delete()
        
        # Create new verification code
        verification = Verification(
            user_id=user.id,
            code=''.join(random.choices(string.digits, k=6)),
            method='login',
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        
        db.session.add(verification)
        db.session.commit()
        
        # Send the verification code
        if not send_login_verification_email(user, verification.code):
            db.session.rollback()
            return jsonify({'error': 'Failed to send verification code'}), 500
        
        return jsonify({
            'message': 'New verification code sent',
            'email': user.email
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Resend login code error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to resend verification code'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Legacy login endpoint - kept for backward compatibility
    New applications should use the two-step verification flow:
    1. /request-login-code
    2. /verify-login
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter(
            func.lower(User.email) == email,
            User.is_verified == True
        ).first()

        if not user:
            log_activity(None, "invalid credentials (user not found): {email}", "logout")
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # For backward compatibility, indicate that verification is required
        return jsonify({
            'requiresVerification': True,
            'email': user.email,
            'message': 'Verification required'
        }), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred during login'}), 500
    

    
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Get the current user's identity from the token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Log the logout activity
        log_activity(user.id, "Logged out of the system", "logout")
        
        # Create a response
        response = jsonify({'message': 'Successfully logged out'})
        
        # Clear the JWT cookies
        unset_jwt_cookies(response)
        
        return response, 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Logout failed'}), 500
    
    

@auth_bp.route('/cleanup-unverified', methods=['POST'])
def cleanup_unverified():
    try:
        cutoff = datetime.utcnow() - timedelta(hours=24)
        unverified_users = User.query.filter(
            User.is_verified == False,
            User.created_at < cutoff
        ).all()

        count = 0
        for user in unverified_users:
            # Delete associated user preferences first (due to foreign key constraint)
            UserPreference.query.filter_by(user_id=user.id).delete()
            Verification.query.filter_by(user_id=user.id).delete()
            db.session.delete(user)
            count += 1

        db.session.commit()
        return jsonify({'message': f'Deleted {count} unverified accounts'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Cleanup error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to cleanup unverified accounts'}), 500

def sanitize_input(data):
    """Sanitize input data to prevent XSS and SQL injection"""
    if isinstance(data, str):
        # Remove potentially harmful characters
        return re.sub(r'[<>"\';]', '', data.strip())
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*()\-_=+{};:,<.>]', password):
        return False
    return True

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create new access token
        new_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        
        response = make_response(jsonify({
            'message': 'Token refreshed successfully',
            'access_token': new_token
        }))
        
        set_access_cookies(response, new_token)
        
        return response, 200
        
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Token refresh failed'}), 500