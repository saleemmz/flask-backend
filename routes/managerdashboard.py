from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.task import Task, TaskAssignee,Comment,File,Key,KeyHolder
from datetime import datetime
from flask import send_file
from flask import current_app
from extensions import db, mail
from datetime import timezone
from flask_mail import Message
from flask import request
import logging
from utils.activitylogger import log_activity
from models.task import Notification
import os  
from extensions import db
from utils.sendnotification import (
    notify_task_deletion,create_in_app_notification
)

manager_bp = Blueprint('manager', __name__)
logger = logging.getLogger(__name__)

def handle_session_expired():
    """Helper function to return consistent session expired response"""
    return jsonify({
        'error': 'Session expired',
        'message': 'Your login session has expired. Please login again.',
        'action': 'login_required',
        'redirect': '/login'
    }), 401

@manager_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_manager_tasks():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or (current_user.role != 'manager' and current_user.role != 'admin'):
            return jsonify({'error': 'Unauthorized - Only managers can access this endpoint'}), 403
        
        tasks = Task.query.order_by(Task.deadline.asc()).all()
        
        tasks_data = []
        for task in tasks:
            assignees = []
            for assignee in task.assignees:
                assignees.append({
                    'id': assignee.id,
                    'name': assignee.full_name,
                    'avatar': assignee.avatar_url or '/placeholder.svg'
                })
            
            processed_files = set()
            files = []
            
            # Only get files that actually exist on disk (file_size > 0)
            all_files = File.query.filter(
                File.task_id == task.id,
                File.file_size > 0  # Only get files that have been actually uploaded
            ).all()
            
            for file in all_files:
                file_identifier = f"{file.file_name}_{file.uploaded_by}"
                if file_identifier in processed_files:
                    continue
                    
                processed_files.add(file_identifier)
                
                uploaded_by_user = User.query.get(file.uploaded_by)
                files.append({
                    'name': file.file_name,
                    'size': file.get_formatted_size(),
                    'uploadedBy': uploaded_by_user.full_name if uploaded_by_user else 'Unknown',
                    'date': file.created_at.strftime('%Y-%m-%d') if file.created_at else None,
                    'isEncrypted': file.is_encrypted
                })
            
            comment_text = 'No comments'
            if task.comments:
                latest_comment = sorted(task.comments, key=lambda c: c.created_at, reverse=True)[0]
                comment_text = latest_comment.comment_text
            
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status.capitalize(),
                'priority': task.priority,
                'deadline': task.deadline.replace(tzinfo=timezone.utc).isoformat() if task.deadline else None,
                'created': task.created_at.strftime('%Y-%m-%d') if task.created_at else None,
                'lastUpdated': task.updated_at.strftime('%Y-%m-%d') if task.updated_at else None,
                'assignee': assignees[0]['name'] if assignees else 'Unassigned',
                'assigneeId': assignees[0]['id'] if assignees else '',
                'assigneeAvatar': assignees[0]['avatar'] if assignees else '/placeholder.svg',
                'comments': comment_text,
                'files': files
            })
        
        return jsonify({'tasks': tasks_data}), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error fetching manager tasks: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch tasks', 'details': str(e)}), 500
    
    
@manager_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'role': user.role
        }), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        return jsonify({'error': 'Failed to fetch user data'}), 500

@manager_bp.route('/tasks/<int:task_id>/files/<string:filename>/download', methods=['GET'])
@jwt_required()
def download_manager_file(task_id, filename):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role not in ['manager', 'admin']:
            return jsonify({'error': 'Unauthorized'}), 403
            
        file_record = File.query.filter_by(
            task_id=task_id,
            file_name=filename
        ).first()
        
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
            
        file_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            file_record.file_path.replace('uploads/', '')
        )
            
        if not os.path.exists(file_path):
            logger.error(f"File not found at path: {file_path}")
            return jsonify({'error': 'File not found on server'}), 404
        
        log_activity(current_user_id, f"Downloaded file: {filename} from task {task_id}", "file")
            
        return send_file(file_path, as_attachment=True, download_name=file_record.file_name)

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to download file'}), 500
    
@manager_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or (current_user.role != 'manager' and current_user.role != 'admin'):
            return jsonify({'error': 'Unauthorized - Only managers can delete tasks'}), 403
        
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Store task details before deletion
        task_title = task.title
        assignees = [assignee for assignee in task.assignees]  # Create a copy of assignees list
        
        # Send notifications before deleting
        notify_task_deletion(task_id, current_user_id)
        
        # First delete KeyHolders associated with the task's keys
        KeyHolder.query.filter(
    KeyHolder.key_id.in_(
        db.session.query(Key.id).filter_by(task_id=task_id)
    )
).delete(synchronize_session=False)
        
        # Then delete the Keys
        Key.query.filter_by(task_id=task_id).delete(synchronize_session=False)
        
        # Delete other related records
        TaskAssignee.query.filter_by(task_id=task_id).delete(synchronize_session=False)
        Comment.query.filter_by(task_id=task_id).delete(synchronize_session=False)
        File.query.filter_by(task_id=task_id).delete(synchronize_session=False)
        
        # Finally delete the task
        db.session.delete(task)
        db.session.commit()

        log_activity(current_user_id, f"Deleted task: {task_title} (ID: {task_id})", "task")
        
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error deleting task {task_id}: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to delete task',
            'details': str(e),
        }), 500
    
@manager_bp.route('/invite', methods=['POST'])
@jwt_required()
def invite_staff():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role not in ['manager', 'admin']:
            return jsonify({'error': 'Unauthorized'}), 403
            
        data = request.get_json()
        email = data.get('email')
        method = data.get('method', 'email')  
        
        if method == 'email' and not email:
            return jsonify({'error': 'Email is required'}), 400
            
        
        invitation_link = f"http://localhost:5173/signup"
        
        if method == 'email':
            # Send email with invitation link
            subject = "You've been invited to join Secure Project Tracker"
            body = f"""You've been invited by {current_user.full_name} to join Secure Project Tracker.
            
Please use the following link to create your account:
{invitation_link}

This link does not expire."""
            
            html = f"""<html>
                <body>
                    <h2>Join Secure Project Tracker</h2>
                    <p>You've been invited by {current_user.full_name} to join Secure Project Tracker.</p>
                    <p>Please click the link below to create your account:</p>
                    <p><a href="{invitation_link}" style="color: #4b0082; font-weight: bold;">Create Account</a></p>
                    <p>Or copy and paste this URL into your browser: {invitation_link}</p>
                </body>
            </html>"""

            msg = Message(
                subject=subject,
                recipients=[email],
                sender=("Secure Project Tracker", "noreply@SPT.com"),
                body=body,
                html=html
            )
            mail.send(msg)
            
        return jsonify({
            'message': 'Invitation sent successfully',
            'link': invitation_link if method == 'link' else None
        }), 200
        
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error sending invitation: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to send invitation'}), 500
    
@manager_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_staff_notifications():
    try:
        current_user_id = get_jwt_identity()
        notifications = Notification.query.filter_by(
            user_id=current_user_id
        ).order_by(Notification.created_at.desc()).all()
        
        notifications_data = [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notification_type,
            'is_read': n.is_read,
            'created_at': n.created_at.replace(tzinfo=timezone.utc).isoformat() if n.created_at else None,
            'task_id': n.related_task_id
        } for n in notifications]
        
        return jsonify({'notifications': notifications_data}), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch notifications'}), 500
    
@manager_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    try:
        current_user_id = get_jwt_identity()
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
            
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error marking notification as read: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to mark notification as read'}), 500
