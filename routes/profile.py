import os
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.activitylogger import log_activity


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Allowed file extensions for avatar uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

profile_bp = Blueprint('profile', __name__)

# Dynamically get BASE_URL from env or default localhost
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5001')


@profile_bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    """Get the current user's profile data."""
    try:
        user_id = get_jwt_identity()

        if not user_id:
            logger.error("No user ID found in JWT token")
            return jsonify({'error': 'Invalid token'}), 401

        user = User.query.get(user_id)

        if not user:
            logger.error(f"User not found with ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404

        # Construct full URL for avatar using BASE_URL
        avatar_url = (
            f"{BASE_URL}/avatars/{os.path.basename(user.avatar_url)}"
            if user.avatar_url else ''
        )

        return jsonify({
            'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone or '',
                'company_name': user.company_name or '',
                'position': user.position or '',
                'bio': user.bio or '',
                'avatar_url': avatar_url,
                'is_verified': user.is_verified,
                'role': user.role
            },
            'message': 'Profile retrieved successfully'
        }), 200

    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch profile data'}), 500


@profile_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({'error': 'Invalid token'}), 401

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Track changes for logging
        changes = []
        fields_to_check = {
            'firstName': 'First name',
            'lastName': 'Last name',
            'username': 'Username',
            'email': 'Email',
            'phone': 'Phone',
            'bio': 'Bio',
            'position': 'Position',
            'company_name': 'Company name'
        }

        for field, display_name in fields_to_check.items():
            if field in data:
                # Handle firstName and lastName specially
                if field == 'firstName':
                    old_value = user.first_name
                    new_value = data[field]
                    if old_value != new_value:
                        changes.append(f"{display_name} changed from '{old_value}' to '{new_value}'")
                        user.first_name = new_value.strip()
                elif field == 'lastName':
                    old_value = user.last_name
                    new_value = data[field]
                    if old_value != new_value:
                        changes.append(f"{display_name} changed from '{old_value}' to '{new_value}'")
                        user.last_name = new_value.strip()
                else:
                    old_value = getattr(user, field)
                    new_value = data[field]
                    if old_value != new_value:
                        changes.append(f"{display_name} changed from '{old_value}' to '{new_value}'")
                        setattr(user, field, new_value.strip() if isinstance(new_value, str) else new_value)

        db.session.commit()

        # Log profile update if any changes were made
        if changes:
            log_activity(user_id, f"Updated profile: {', '.join(changes)}", "profile")

        avatar_url = (
            f"{BASE_URL}/avatars/{os.path.basename(user.avatar_url)}"
            if user.avatar_url else ''
        )

        return jsonify({
            'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone or '',
                'company_name': user.company_name or '',
                'position': user.position or '',
                'bio': user.bio or '',
                'avatar_url': avatar_url,
                'is_verified': user.is_verified,
                'role': user.role
            },
            'message': 'Profile updated successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating profile: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to update profile'}), 500


@profile_bp.route('/update-avatar', methods=['POST'])
@jwt_required()
def update_avatar():
    """Update the user's avatar."""
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({'error': 'Invalid token'}), 401

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if 'avatar' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['avatar']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Only jpg, jpeg, png, gif are allowed.'
            }), 400

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")
        avatars_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
        os.makedirs(avatars_dir, exist_ok=True)
        file_path = os.path.join(avatars_dir, filename)
        file.save(file_path)

        # Update avatar URL in DB (relative path for serving later)
        user.avatar_url = filename
        db.session.commit()

        # Log avatar update
        log_activity(user_id, "Updated profile avatar", "profile")

        # Construct full URL with BASE_URL
        avatar_url = f"{BASE_URL}/avatars/{filename}"

        return jsonify({
            'avatarUrl': avatar_url,
            'message': 'Avatar updated successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating avatar: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to update avatar'}), 500
