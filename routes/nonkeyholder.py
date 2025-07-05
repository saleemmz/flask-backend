from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.task import Task, File, TaskAssignee
from extensions import db
import os
from flask import current_app
from utils.activitylogger import log_activity
import logging

nonkeyholder_bp = Blueprint('nonkeyholder', __name__, url_prefix='/api/nonkeyholder')
logger = logging.getLogger(__name__)

@nonkeyholder_bp.route('/task/<int:task_id>', methods=['GET'])
@jwt_required()
def get_nonkeyholder_task(task_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Verify user is a staff member
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Check if user is assigned to the task
        assignment = TaskAssignee.query.filter_by(
            task_id=task_id,
            user_id=current_user_id
        ).first()
        if not assignment:
            return jsonify({'error': 'Not assigned to this task'}), 403
            
        # Get task details
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # FIXED: Get the specific file that the user was trying to access
        filename = request.args.get('filename')
        if filename:
            file = File.query.filter(
                File.task_id == task_id,
                File.file_name == filename,
                File.file_size > 0,
                File.is_encrypted == True
            ).first()
        else:
            # Fallback to first encrypted file
            file = File.query.filter(
                File.task_id == task_id,
                File.is_encrypted == True,
                File.file_size > 0
            ).first()
            
        if not file:
            return jsonify({'error': 'Encrypted file not found'}), 404
        
        # Log file access attempt
        log_activity(current_user_id, 
                    f"Attempted to access encrypted file {file.file_name} (no key access)", 
                    "file")
            
        return jsonify({
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None,
                'priority': task.priority
            },
            'file': {
                'name': file.file_name,
                'size': file.get_formatted_size(),
                'is_encrypted': file.is_encrypted
            }
        }), 200

    except Exception as e:
        logger.error(f"Error in nonkeyholder task: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
