from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import current_app
from extensions import db
from flask import send_file
from models.user import User
from models.task import Task, Comment, TaskAssignee, File, Key, KeyHolder
from datetime import datetime, timezone
import os
import logging
from models.task import Notification
from utils.activitylogger import log_activity
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.sendnotification import (
    notify_task_assignment,
    notify_task_completion,
    check_and_notify_approaching_deadlines,
    notify_task_due
)


staff_bp = Blueprint('staff', __name__)
logger = logging.getLogger(__name__)

def handle_session_expired():
    """Helper function to return consistent session expired response"""
    return jsonify({
        'error': 'Session expired',
        'message': 'Your login session has expired. Please login again.',
        'action': 'login_required',
        'redirect': '/login'
    }), 401

@staff_bp.route('/user', methods=['GET'])
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

@staff_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_staff_tasks():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or (current_user.role != 'staff' and current_user.role != 'admin'):
            return jsonify({'error': 'Unauthorized - Only staff members can access this endpoint'}), 403
        
        assigned_tasks = Task.query.join(TaskAssignee).filter(
            TaskAssignee.user_id == current_user_id
        ).order_by(Task.deadline.asc()).all()
        
        tasks_data = []
        for task in assigned_tasks:
            # FIXED: Only get files that actually exist on disk (file_size > 0)
            all_files = File.query.filter(
                File.task_id == task.id,
                File.file_size > 0  # Only get files that have been actually uploaded
            ).all()
            
            manager_files = []
            staff_uploads = []
            
            # Get all keys for this task
            task_keys = Key.query.filter_by(task_id=task.id).all()
            key_ids = [key.id for key in task_keys]
            
            # Check which encrypted files the user has access to
            user_key_holder_files = set()
            if key_ids:
                key_holders = KeyHolder.query.filter(
                    KeyHolder.user_id == current_user_id,
                    KeyHolder.key_id.in_(key_ids)
                ).all()
                user_key_holder_files = {kh.file_id for kh in key_holders if kh.file_id}
            
            for file in all_files:
                file_entry = {
                    'name': file.file_name,
                    'type': file.file_name.split('.')[-1].lower(),
                    'size': file.get_formatted_size(),
                    'date': file.created_at.strftime('%Y-%m-%d') if file.created_at else None,
                    'isEncrypted': file.is_encrypted,
                    'canAccess': True if not file.is_encrypted else (file.id in user_key_holder_files)
                }
                
                file_uploader_id = int(file.uploaded_by) if file.uploaded_by is not None else None
                current_user_id_int = int(current_user_id) if current_user_id is not None else None
                
                if file_uploader_id == current_user_id_int:
                    file_entry['uploadedBy'] = 'You'
                    staff_uploads.append(file_entry)
                else:
                    uploaded_by_user = User.query.get(file.uploaded_by)
                    file_entry['uploadedBy'] = uploaded_by_user.full_name if uploaded_by_user else 'Manager'
                    manager_files.append(file_entry)
            
            comments = []
            for comment in task.comments:
                comment_user = User.query.get(comment.user_id)
                comments.append({
                    'text': comment.comment_text,
                    'user': comment_user.full_name if comment_user else 'Unknown',
                    'date': comment.created_at.strftime('%Y-%m-%d') if comment.created_at else None
                })
            
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'status': task.status.capitalize(),
                'priority': task.priority,
                'deadline': task.deadline.replace(tzinfo=timezone.utc).isoformat() if task.deadline else None,
                'description': task.description,
                'managerFiles': manager_files,
                'myUploads': staff_uploads,
                'comments': comments
            })
        
        return jsonify({'tasks': tasks_data}), 200
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error fetching staff tasks: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch tasks', 'details': str(e)}), 500
    

@staff_bp.route('/tasks/<int:task_id>/files/<string:filename>/download', methods=['GET'])
@jwt_required()
def download_staff_file(task_id, filename):
    try:
        current_user_id = get_jwt_identity()
        
        # Verify user and assignment
        assignment = TaskAssignee.query.filter_by(
            task_id=task_id,
            user_id=current_user_id
        ).first()
        
        if not assignment:
            return jsonify({'error': 'Not assigned to this task'}), 403
            
        # Get the file with actual content (file_size > 0)
        file_record = File.query.filter(
            File.task_id == task_id,
            File.file_name == filename,
            File.file_size > 0
        ).order_by(File.created_at.desc()).first()
        
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        # If file is NOT encrypted - allow direct download
        if not file_record.is_encrypted:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_record.file_path)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, download_name=filename)
            else:
                return jsonify({'error': 'File not found on disk'}), 404
        
        # File IS encrypted - check key holder status
        key = Key.query.filter_by(task_id=task_id).first()
        if not key:
            logger.error(f"No encryption key found for task {task_id}")
            return jsonify({'error': 'Encryption key not found'}), 403
        
        # Check if user is a key holder for this specific file
        key_holder_record = KeyHolder.query.filter_by(
            user_id=current_user_id,
            key_id=key.id,
            file_id=file_record.id
        ).first()
        
        if key_holder_record:
            # User IS a key holder - redirect to keyholder page for verification
            return jsonify({
                'message': 'Redirecting to key holder verification page',
                'is_encrypted': True,
                'has_access': True,
                'task_id': task_id,
                'filename': filename
            }), 200
        else:
            # User is NOT a key holder - deny access
            return jsonify({
                'error': 'Not authorized to access this encrypted file',
                'is_encrypted': True,
                'has_access': False
            }), 403

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to download file'}), 500
    
@staff_bp.route('/tasks/<int:task_id>/submit', methods=['POST'])
@jwt_required()
def submit_task(task_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Verify the user is a staff member
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'error': 'Unauthorized - Only staff members can submit tasks'}), 403
        
        # Get the task
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Check if the task is assigned to this user
        assignment = TaskAssignee.query.filter_by(
            task_id=task_id,
            user_id=current_user_id
        ).first()
        if not assignment:
            return jsonify({'error': 'You are not assigned to this task'}), 403
        
        # Get data from request
        data = request.get_json()
        comment_text = data.get('comment', '')
        
        # Update task status
        task.status = 'completed'
        task.updated_at = datetime.now(timezone.utc)
        
        # Add comment if provided
        if comment_text:
            comment = Comment(
                task_id=task_id,
                user_id=current_user_id,
                comment_text=comment_text,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(comment)
        
        db.session.commit()

        log_activity(current_user_id, f"submitted task: {task.title} (ID: {task_id})", "task")

         # Notify the manager who created the task
        notify_task_completion(task_id, current_user_id)
        
        return jsonify({'message': 'Task submitted successfully'}), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error submitting task: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to submit task', 'details': str(e)}), 500

@staff_bp.route('/tasks/<int:task_id>/upload', methods=['POST'])
@jwt_required()
def upload_task_file(task_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Verify the user is a staff member
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'error': 'Unauthorized - Only staff members can upload files'}), 403
        
        # Check if the task is assigned to this user
        assignment = TaskAssignee.query.filter_by(
            task_id=task_id,
            user_id=current_user_id
        ).first()
        if not assignment:
            return jsonify({'error': 'You are not assigned to this task'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Create task-specific upload directory
        upload_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'tasks',
            str(task_id)
        )
        os.makedirs(upload_dir, exist_ok=True)

        # Secure filename and ensure uniqueness
        filename = file.filename
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(upload_dir, filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1

        # Save the file
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        # Get file size
        file_size = os.path.getsize(file_path)

        # Create file record in database
        file_record = File(
            file_name=filename,
            file_path=f"tasks/{task_id}/{filename}",
            task_id=task_id,
            uploaded_by=current_user_id,
            created_at=datetime.now(timezone.utc),
            file_size=file_size
        )
        db.session.add(file_record)
        db.session.commit()

        return jsonify({
            'message': 'File uploaded successfully',
            'file': {
                'name': filename,
                'type': filename.split('.')[-1].lower(),
                'size': file_record.get_formatted_size(),
                'uploadedBy': 'You',
                'date': datetime.now(timezone.utc).strftime('%Y-%m-%d')
            }
        }), 200
        
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to upload file'}), 500

@staff_bp.route('/tasks/<int:task_id>/files', methods=['DELETE'])
@jwt_required()
def delete_staff_file(task_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Verify the user is a staff member
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'error': 'Unauthorized - Only staff members can delete files'}), 403
        
        # Check if the task is assigned to this user
        assignment = TaskAssignee.query.filter_by(
            task_id=task_id,
            user_id=current_user_id
        ).first()
        if not assignment:
            return jsonify({'error': 'You are not assigned to this task'}), 403
        
        data = request.get_json()
        filename = data.get('fileName')
        
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        
        # Find the file record
        file_record = File.query.filter_by(
            task_id=task_id,
            file_name=filename,
            uploaded_by=current_user_id  # Only allow deleting own files
        ).first()
        
        if not file_record:
            return jsonify({'error': 'File not found or not owned by you'}), 404
        
        # Delete the physical file
        file_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            file_record.file_path
        )
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the database record
        db.session.delete(file_record)
        db.session.commit()
        
        return jsonify({'message': 'File deleted successfully'}), 200
        
    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error deleting file: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to delete file'}), 500
    
@staff_bp.route('/notifications', methods=['GET'])
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
    
@staff_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
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
        notification.read_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200

    except Exception as e:
        if 'token' in str(e).lower() or 'expired' in str(e).lower():
            return handle_session_expired()
        db.session.rollback()
        logger.error(f"Error marking notification as read: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to mark notification as read'}), 500
