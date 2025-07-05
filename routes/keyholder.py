from flask import Blueprint, jsonify, request
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.task import Task, Key, KeyHolder, File, TaskAssignee
from extensions import db, mail
from flask_mail import Message
import os
from email.utils import formataddr
import logging
from utils.activitylogger import log_activity
import traceback
from flask import send_file

keyholder_bp = Blueprint('keyholder', __name__, url_prefix='/api/keyholder')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@keyholder_bp.route('/task/<int:task_id>', methods=['GET'])
@jwt_required()
def get_keyholder_task(task_id):
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

        # FIXED: Get the specific file that the user is trying to access
        filename = request.args.get('filename') 
        
        if filename:
            # Get the actual file with content (file_size > 0)
            file = File.query.filter(
                File.task_id == task_id,
                File.file_name == filename,
                File.file_size > 0,  # Only get files that have been actually uploaded
                File.is_encrypted == True
            ).order_by(File.created_at.desc()).first()
        else:
            # Fallback to first encrypted file with content
            file = File.query.filter(
                File.task_id == task_id,
                File.is_encrypted == True,
                File.file_size > 0
            ).first()
        
        if not file:
            return jsonify({'error': 'Encrypted file not found'}), 404

        # Get the encryption key for this specific file
        key_holder = KeyHolder.query.join(Key).filter(
            KeyHolder.user_id == current_user_id,
            Key.task_id == task_id,
            KeyHolder.file_id == file.id
        ).first()

        if not key_holder:
            return jsonify({'error': 'Not a key holder for this file'}), 403

        key = Key.query.get(key_holder.key_id)

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
                'encryptionKey': key.encryption_key if key else None,
                'is_encrypted': file.is_encrypted,
                'file_id': file.id
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting keyholder task: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@keyholder_bp.route('/send-key', methods=['POST'])
@jwt_required()
def send_decryption_key():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        task_id = data.get('task_id')

        if not task_id:
            return jsonify({'error': 'Task ID is required'}), 400

        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'error': 'Unauthorized'}), 403

        assignment = TaskAssignee.query.filter_by(
            task_id=task_id,
            user_id=current_user_id
        ).first()
        if not assignment:
            return jsonify({'error': 'Not assigned to this task'}), 403

        # Get the specific file being accessed
        filename = data.get('filename')
        if filename:
            file = File.query.filter(
                File.task_id == task_id,
                File.file_name == filename,
                File.file_size > 0,
                File.is_encrypted == True
            ).first()
        else:
            file = File.query.filter(
                File.task_id == task_id,
                File.is_encrypted == True,
                File.file_size > 0
            ).first()

        if not file:
            return jsonify({'error': 'File not found'}), 404

        key_holder = KeyHolder.query.join(Key).filter(
            KeyHolder.user_id == current_user_id,
            Key.task_id == task_id,
            KeyHolder.file_id == file.id
        ).first()

        if not key_holder:
            return jsonify({'error': 'Not a key holder for this file'}), 403

        key = Key.query.get(key_holder.key_id)
        if not key or not key.encryption_key:
            return jsonify({'error': 'No encryption key found'}), 404

        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Create email message
        subject = f"Decryption Key for Task: {task.title}"
        body = f"""Here is your decryption key for the task "{task.title}":

Key: {key.encryption_key}

File: {file.file_name}

Please use this key to decrypt the file when needed.

This key is sensitive information - do not share it with others.
        """

        msg = Message(
            subject=subject,
            recipients=[current_user.email],
           sender=formataddr(("noreplyspt", "saleemm1137@gmail.com")),
            body=body
        )

        # Test mail server connection
        try:
            mail.send(msg)
            logger.info(f"Decryption key email sent to {current_user.email}")
            
            # Log key email sent
            log_activity(current_user_id, f"Requested decryption key email for task: {task.title}", "file")
            
            return jsonify({
                'message': 'Decryption key has been sent to your email',
                'email': current_user.email
            }), 200
        except Exception as mail_error:
            logger.error(f"Mail sending failed: {str(mail_error)}")
            logger.error(f"Mail server config: {current_app.config['MAIL_SERVER']}:{current_app.config['MAIL_PORT']}")
            logger.error(f"Mail username: {current_app.config['MAIL_USERNAME']}")
            return jsonify({
                'error': 'Failed to send email. Please check mail server configuration.',
                'details': str(mail_error)
            }), 500

    except Exception as e:
        logger.error(f"Error in send_decryption_key: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Failed to send decryption key',
            'details': str(e)
        }), 500

@keyholder_bp.route('/verify-key', methods=['POST'])
@jwt_required()
def verify_decryption_key():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        task_id = data.get('task_id')
        input_key = data.get('key')

        if not task_id or not input_key:
            return jsonify({'error': 'Task ID and key are required'}), 400

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

        # Get the encryption key
        key_holder = KeyHolder.query.join(Key).filter(
            KeyHolder.user_id == current_user_id,
            Key.task_id == task_id
        ).first()

        if not key_holder:
            return jsonify({'error': 'Not a key holder for this task'}), 403

        key = Key.query.get(key_holder.key_id)
        if not key or not key.encryption_key:
            return jsonify({'error': 'No encryption key found'}), 404

        # Verify the provided key matches the stored key
        key_valid = (input_key == key.encryption_key)

        # Log key verification attempt
        log_activity(current_user_id, 
                   f"Attempted to verify decryption key for task {task_id} - {'success' if key_valid else 'failed'}", 
                   "file")

        return jsonify({
            'valid': key_valid,
            'message': 'Key verification successful' if key_valid else 'Invalid key'
        }), 200
    
    except Exception as e:
        logger.error(f"Error verifying decryption key: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Failed to verify decryption key',
            'details': str(e)
        }), 500
    
@keyholder_bp.route('/download/<int:task_id>/<string:filename>', methods=['GET'])
@jwt_required()
def download_verified_file(task_id, filename):
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

        # FIXED: Get the actual file with content
        file = File.query.filter(
            File.task_id == task_id,
            File.file_name == filename,
            File.file_size > 0  # Only get files that have been actually uploaded
        ).order_by(File.created_at.desc()).first()
        
        if not file:
            return jsonify({'error': 'File not found'}), 404

        # Verify user is a key holder for this file (if encrypted)
        if file.is_encrypted:
            key_holder = KeyHolder.query.join(Key).filter(
                KeyHolder.user_id == current_user_id,
                Key.task_id == task_id,
                KeyHolder.file_id == file.id
            ).first()

            if not key_holder:
                return jsonify({'error': 'Not authorized to download this file'}), 403

        # Get the actual file path
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.file_path)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found on disk'}), 404

        # Log the download
        task = Task.query.get(task_id)
        log_activity(current_user_id, f"Downloaded file: {file.file_name} for task: {task.title}", "file")
        
        return send_file(file_path, as_attachment=True, download_name=filename)

    except Exception as e:
        logger.error(f"Error downloading verified file: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@keyholder_bp.route('/log-download/<int:task_id>', methods=['POST'])
@jwt_required()
def log_file_download(task_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Verify user is a staff member
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'error': 'Unauthorized'}), 403

        # Get task details
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Get the file
        filename = request.json.get('filename') if request.json else None
        if filename:
            file = File.query.filter(
                File.task_id == task_id,
                File.file_name == filename,
                File.file_size > 0
            ).first()
        else:
            file = File.query.filter(
                File.task_id == task_id,
                File.file_size > 0
            ).first()
        
        if not file:
            return jsonify({'error': 'File not found'}), 404


        
        return jsonify({'message': 'Download logged successfully'}), 200

    except Exception as e:
        logger.error(f"Error logging file download: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
