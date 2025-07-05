from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, Verification, UserPreference
from models.activity import Activity
from models.task import Task, TaskAssignee, File, Comment, Notification, KeyHolder
from extensions import db
from datetime import datetime
import traceback 
from utils.activitylogger import log_activity
import logging

admindashboard_bp = Blueprint('admin', __name__)

logger = logging.getLogger(__name__)

def handle_session_expired():
    """Helper function to return consistent session expired response"""
    return jsonify({
        'error': 'Session expired',
        'message': 'Your login session has expired. Please login again.',
        'action': 'login_required',
        'redirect': '/login'
    }), 401

@admindashboard_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

       
        users = User.query.all()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email,
                'role': user.position,
                'status': 'Active' if user.is_verified else 'Inactive',
                'avatar': user.avatar_url or '/placeholder.svg',
                'department': 'General',
                'joinDate': user.created_at.strftime('%Y-%m-%d'),
                'lastActive': user.last_login.strftime('%Y-%m-%d %I:%M %p') if user.last_login else 'Never',
                'tasksAssigned': 0,
                'tasksCompleted': 0
            })

        return jsonify(users_data), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@admindashboard_bp.route('/users', methods=['POST'])
@jwt_required()
def add_user():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        required_fields = ['firstName', 'lastName', 'username', 'email', 'position']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # === VALIDATION LOGIC ===

        # Capitalize first letter of names and ensure the rest are lowercase
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        if not first_name.istitle():
            return jsonify({'error': 'First name must start with a capital letter'}), 400
        if not last_name.istitle():
            return jsonify({'error': 'Last name must start with a capital letter'}), 400

        # Enforce lowercase usernames
        username = data['username'].strip()
        if not username.islower():
            return jsonify({'error': 'Username must be all lowercase letters'}), 400

        # Check for duplicates
        existing_user = User.query.filter(
            (User.username == username) | 
            (User.email == data['email'])
        ).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=data['email'].strip(),
            position=data['position'].strip(),
            is_verified=True,
            role='staff' if data['position'].lower() != 'admin' else 'admin'
        )

        try:
            new_user.password = data.get('password', 'DefaultPassword123!')
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        db.session.add(new_user)
        db.session.commit()

        log_activity(current_user_id, f"Created new user: {username} ({data['email']})", "user")

        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': new_user.id,
                'name': f"{new_user.first_name} {new_user.last_name}",
                'username': new_user.username,
                'email': new_user.email,
                'role': new_user.position,
                'status': 'Active'
            }
        }), 201

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error adding user: {str(e)}")
        return jsonify({'error': f'Failed to add user: {str(e)}'}), 500

@admindashboard_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if 'role' in data:  # Changed from 'position' to 'role'
            user.role = data['role'].lower()  # Ensure lowercase for consistency
            # Update position as well if needed
            if 'position' in data:
                user.position = data['position']

        db.session.commit()

        log_activity(current_user_id, f"Updated user role: {user.username} (ID: {user_id})", "user")
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email,
                'role': user.role, 
                'status': 'Active' if user.is_verified else 'Inactive'
            }
        }), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error updating user: {str(e)}")
        return jsonify({'error': 'Failed to update user'}), 500

@admindashboard_bp.route('/users/<int:user_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_user(user_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'preflight'}), 200
    
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.id == current_user.id:
            return jsonify({'error': 'Cannot delete your own account'}), 400

        # Clean up all related records before deleting the user
        username = user.username
        
        # Delete verifications
        Verification.query.filter_by(user_id=user_id).delete()
        
        # Delete user preferences
        UserPreference.query.filter_by(user_id=user_id).delete()
        
        # Delete activities
        Activity.query.filter_by(user_id=user_id).delete()
        
        # Handle task assignments
        TaskAssignee.query.filter_by(user_id=user_id).delete()
        
        # Handle files uploaded by user
        File.query.filter_by(uploaded_by=user_id).delete()
        
        # Handle comments by user
        Comment.query.filter_by(user_id=user_id).delete()
        
        # Handle notifications for user
        Notification.query.filter_by(user_id=user_id).delete()
        
        # Handle key holders
        KeyHolder.query.filter_by(user_id=user_id).delete()
        
        # Now delete the user
        db.session.delete(user)
        db.session.commit()

        log_activity(current_user_id, f"Deleted user: {username} (ID: {user_id})", "user")
        
        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error deleting user: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500

@admindashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        # User statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_verified=True).count()
        inactive_users = total_users - active_users
        
        roles = db.session.query(
            User.position,
            db.func.count(User.id).label('count')
        ).group_by(User.position).all()
        
        role_distribution = {role[0]: role[1] for role in roles}

        # Task statistics
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter_by(status='completed').count()
        incomplete_tasks = Task.query.filter_by(status='incompleted').count()

        return jsonify({
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'role_distribution': role_distribution,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'incomplete_tasks': incomplete_tasks
        }), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500
