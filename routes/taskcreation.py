from flask import Blueprint, request, jsonify
from datetime import timedelta
from werkzeug.utils import secure_filename
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from flask import current_app
from extensions import db
from models.user import User
from models.task import Task, TaskAssignee, File, Key, KeyHolder
from datetime import datetime
import os
import logging
from utils.activitylogger import log_activity
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.sendnotification import (
    notify_task_assignment,
    notify_task_completion,
    check_and_notify_approaching_deadlines,
    notify_task_due
)

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')
logger = logging.getLogger(__name__)

@task_bp.route('/create', methods=['POST'])
@jwt_required()
def create_task():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get current user from database
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Unauthorized - Only managers and admins can create tasks'}), 403
        
        # Validate required fields
        if not data.get('title') or not data.get('deadline'):
            return jsonify({'error': 'Title and deadline are required'}), 400
        
        # Create the task
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            deadline=datetime.fromisoformat(data['deadline'].replace('Z', '+00:00')).replace(tzinfo=None),
            priority=data.get('priority', 'Medium'),
            created_by=current_user_id,
            status='incompleted'
        )
        
        db.session.add(task)
        db.session.flush()  # To get the task ID
        
        # Process assignees
        assignee_ids = data.get('assignees', [])
        for user_id in assignee_ids:
            assignee = TaskAssignee(task_id=task.id, user_id=user_id)
            db.session.add(assignee)
        
        # Create encryption key if any files are encrypted
        encryption_key = None
        files_data = data.get('files', [])
        if any(f.get('isEncrypted', False) for f in files_data):
            encryption_key = Key(
                encryption_key=data.get('aesKey', ''),
                task_id=task.id
            )
            db.session.add(encryption_key)
            db.session.flush()  # Get the key ID
        
        # FIXED: Store file metadata for later processing, don't create File records yet
        # Files will be created when actually uploaded
        if files_data and encryption_key:
            # Store the key holder assignments temporarily in session or pass to frontend
            # We'll handle this when files are actually uploaded
            pass
        
        db.session.commit()

        # Notify each assignee
        for user_id in assignee_ids:
            notify_task_assignment(task.id, user_id)

        # Check if deadline is within 24 hours
        if task.deadline and (task.deadline - datetime.utcnow()) <= timedelta(hours=24):
            notify_task_due(task.id)

        # Log task creation
        log_activity(current_user_id, 
                    f"Created new task: {task.title} (ID: {task.id}) with {len(assignee_ids)} assignees", 
                    "task")
        
        return jsonify({
            'message': 'Task created successfully',
            'task_id': task.id,
            'task': task.to_dict(),
            'files_metadata': files_data,  # Return file metadata for upload processing
            'encryption_key_id': encryption_key.id if encryption_key else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating task: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to create task'}), 500

@task_bp.route('/staff', methods=['GET'])
@jwt_required()
def get_staff_members():
    try:
        logger.info("Staff members endpoint hit")
        staff_members = User.query.filter(User.role == 'staff').all()
        
        # Add logging to debug
        for user in staff_members:
            logger.info(f"User ID: {user.id}, Name: {user.full_name}, Role: {user.role}")
        
        return jsonify({
            'staff': [user.to_dict() for user in staff_members]
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching staff members: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch staff members'}), 500


@task_bp.route('/upload-file', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Get task ID from form data
        task_id = request.form.get('task_id')
        if not task_id:
            return jsonify({'error': 'Task ID is required'}), 400

        is_encrypted = request.form.get('is_encrypted', 'false').lower() == 'true'
        key_holders = request.form.get('key_holders', '').split(',') if request.form.get('key_holders') else []
        current_user_id = get_jwt_identity()

        # DEBUG: Log the received data
        logger.info(f"Upload file: task_id={task_id}, is_encrypted={is_encrypted}, key_holders={key_holders}")

        # Secure the filename
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400

        # Define upload directory
        upload_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'tasks',
            str(task_id)
        )

        # Create the directory if it doesn't exist
        try:
            os.makedirs(upload_dir, exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directory {upload_dir}: {str(e)}")
            return jsonify({'error': 'Failed to create upload directory'}), 500

        # Ensure unique filename
        base, ext = os.path.splitext(filename)
        counter = 1
        original_filename = filename
        while os.path.exists(os.path.join(upload_dir, filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1

        # Save the file
        file_path = os.path.join(upload_dir, filename)
        try:
            file.save(file_path)
            file_size = os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Failed to save file {file_path}: {str(e)}")
            return jsonify({'error': 'Failed to save file'}), 500

        # Create file record in database
        file_record = File(
            file_name=original_filename,  # Use original filename for consistency
            file_path=f"tasks/{task_id}/{filename}",
            is_encrypted=is_encrypted,
            task_id=task_id,
            uploaded_by=current_user_id,
            file_size=file_size
        )
        db.session.add(file_record)
        db.session.flush()  # Get the file ID

        # DEBUG: Log file record creation
        logger.info(f"File record created: ID={file_record.id}, Name={file_record.file_name}, Encrypted={file_record.is_encrypted}")

        # If file is encrypted, assign key holders
        if is_encrypted:
            # Get the encryption key for this task
            key = Key.query.filter_by(task_id=task_id).first()
            if key:
                logger.info(f"Found encryption key: ID={key.id} for task {task_id}")
                
                # If specific key holders are provided, use them
                if key_holders and any(kh.strip() for kh in key_holders):
                    for user_id in key_holders:
                        if user_id.strip():  # Make sure user_id is not empty
                            try:
                                user_id_int = int(user_id.strip())
                                key_holder = KeyHolder(
                                    user_id=user_id_int,
                                    key_id=key.id,
                                    file_id=file_record.id
                                )
                                db.session.add(key_holder)
                                logger.info(f"Created KeyHolder: user_id={user_id_int}, key_id={key.id}, file_id={file_record.id}")
                            except ValueError:
                                logger.warning(f"Invalid user_id for key holder: {user_id}")
                else:
                    # FALLBACK: If no specific key holders, make all task assignees key holders
                    assignees = TaskAssignee.query.filter_by(task_id=task_id).all()
                    for assignee in assignees:
                        key_holder = KeyHolder(
                            user_id=assignee.user_id,
                            key_id=key.id,
                            file_id=file_record.id
                        )
                        db.session.add(key_holder)
                        logger.info(f"Created fallback KeyHolder: user_id={assignee.user_id}, key_id={key.id}, file_id={file_record.id}")
            else:
                logger.error(f"No encryption key found for task {task_id}")

        db.session.commit()

        return jsonify({
            'message': 'File uploaded successfully',
            'file_name': original_filename,
            'file_path': f"tasks/{task_id}/{filename}",
            'file_id': file_record.id,
            'is_encrypted': is_encrypted,
            'file_size': file_size,
            'full_path': f"/task-files/{task_id}/{filename}"
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to upload file'}), 500
    
@task_bp.route('/test-upload', methods=['GET', 'POST'])
def test_upload_file():
    if request.method == 'GET':
        return '''
            <form method="post" enctype="multipart/form-data">
                Task ID: <input type="text" name="task_id" value="test"><br>
                File: <input type="file" name="file"><br>
                <input type="submit" value="Upload">
            </form>
        '''

    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        task_id = request.form.get('task_id', 'test')
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400

        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'tasks', str(task_id))
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        return jsonify({
            'message': 'Test file uploaded successfully',
            'file_path': file_path,
            'exists': os.path.exists(file_path)
        }), 200

    except Exception as e:
        current_app.logger.error(f"Test upload failed: {str(e)}", exc_info=True)
        return jsonify({'error': 'Test upload failed', 'details': str(e)}), 500
