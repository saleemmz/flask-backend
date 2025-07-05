from flask import Flask, jsonify, request
from extensions import db, mail, cors, migrate
from flask import send_from_directory
import os
from dotenv import load_dotenv
from datetime import timedelta
from flask_migrate import Migrate
import pymysql
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError
from flask import send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit
from sqlalchemy import text
from flask_jwt_extended import create_access_token, set_access_cookies

# Import all blueprints
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.passwordrecovery import password_recovery_bp
from routes.admindashboard import admindashboard_bp
from routes.taskcreation import task_bp
from routes.managerdashboard import manager_bp
from routes.staffdashboard import staff_bp
from routes.keyholder import keyholder_bp
from routes.nonkeyholder import nonkeyholder_bp
from routes.support import support_bp
from routes.activitylogs import activity_bp
from routes.settings import settings_bp

pymysql.install_as_MySQLdb()
load_dotenv()

# Global scheduler variable
scheduler = None

def check_deadlines_job():
    """Wrapper function for the scheduler job"""
    try:
        from utils.sendnotification import check_and_notify_approaching_deadlines
        with db.app.app_context():
            result = check_and_notify_approaching_deadlines()
            print(f"Deadline check job completed with result: {result}")
    except Exception as e:
        print(f"Error in deadline check job: {str(e)}")

def create_app():
    global scheduler
    app = Flask(__name__)
    
    app = Flask(__name__, static_folder='uploads')
    app.config['UPLOAD_FOLDER'] = '/Users/promobile/Desktop/SPT/Backend/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit 

    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'connect_args': {
                'connect_timeout': 10
            }
        },
        'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
        'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
        'JWT_TOKEN_LOCATION': ['headers', 'cookies'],
        'JWT_COOKIE_SECURE': False,
        'JWT_COOKIE_CSRF_PROTECT': False,
        'JWT_ACCESS_COOKIE_PATH': '/',
        'JWT_REFRESH_COOKIE_PATH': '/',
        'JWT_COOKIE_SAMESITE': 'Lax',
        'MAIL_SERVER': os.getenv('MAIL_SERVER'),
        'MAIL_PORT': int(os.getenv('MAIL_PORT')),
        'MAIL_USE_TLS': os.getenv('MAIL_USE_TLS').lower() == 'true',
        'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
        'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER'),
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN')
    })

    # Initialize extensions with retry logic
    def initialize_extensions(app):
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                db.init_app(app)
                mail.init_app(app)
                cors.init_app(
                    app,
                    supports_credentials=True,
                    origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
                    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                    expose_headers=["Authorization", "Set-Cookie"],
                    max_age=86400
                )
                migrate.init_app(app, db)
                jwt = JWTManager(app)

                @jwt.token_in_blocklist_loader
                def check_if_token_revoked(jwt_header, jwt_payload):
                    return False

                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to initialize extensions after {max_retries} attempts: {str(e)}")
                time.sleep(retry_delay)

    initialize_extensions(app)

    # Initialize scheduler after app context is available
    if scheduler is None:
        scheduler = BackgroundScheduler()
        
        db.app = app
        scheduler.add_job(
            func=check_deadlines_job, 
            trigger="interval", 
            minutes=1,  
            id='deadline_check',
            replace_existing=True
        )
        scheduler.start()
        
        # Ensure scheduler shuts down properly
        atexit.register(lambda: scheduler.shutdown() if scheduler else None)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(password_recovery_bp, url_prefix='/auth')
    app.register_blueprint(admindashboard_bp, url_prefix='/admin') 
    app.register_blueprint(task_bp,url_prefix='/tasks' )
    app.register_blueprint(manager_bp, url_prefix='/manager')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(keyholder_bp, url_prefix='/keyholder')
    app.register_blueprint(nonkeyholder_bp, url_prefix='/nonkeyholder')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(activity_bp, url_prefix='/activity')
    app.register_blueprint(settings_bp, url_prefix='/settings')

    # Preflight handler for CORS
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({"status": "preflight"})
            response.headers.add("Access-Control-Allow-Origin", request.headers.get('Origin'))
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,Accept,X-Requested-With")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response

    @app.route('/')
    def index():
        return {'message': 'Welcome to SPT API'}

    @app.route('/test-db')
    def test_db():
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).fetchone()
                if result and result[0] == 1:
                    return jsonify({'status': 'Database connection successful'}), 200
                raise Exception("Unexpected query result")
        except Exception as e:
            app.logger.error(f"Database test failed: {str(e)}")
            return jsonify({'error': 'Database connection failed', 'details': str(e)}), 500
    
    # Enhanced test endpoint with detailed debugging
    @app.route('/test-deadline-notifications')
    def test_deadline_notifications():
        try:
            from utils.sendnotification import check_and_notify_approaching_deadlines, get_deadline_debug_info
            
            # Get debug info first
            debug_info = get_deadline_debug_info()
            
            # Run the notification check
            result = check_and_notify_approaching_deadlines()
            
            return jsonify({
                'status': 'success', 
                'result': result,
                'debug_info': debug_info
            }), 200
        except Exception as e:
            return jsonify({'error': str(e), 'status': 'error'}), 500

    # New endpoint to create a test task for debugging
    @app.route('/create-test-task')
    def create_test_task():
        try:
            from models.task import Task, TaskAssignee
            from models.user import User
            from datetime import datetime, timezone, timedelta
            
            # Find a staff user to assign the task to
            staff_user = User.query.filter_by(role='staff').first()
            if not staff_user:
                return jsonify({'error': 'No staff user found'}), 400
            
            # Find an admin/manager to create the task
            manager = User.query.filter(User.role.in_(['admin', 'manager'])).first()
            if not manager:
                return jsonify({'error': 'No manager found'}), 400
            
            # Create a test task with deadline in 1 hour
            test_deadline = datetime.now(timezone.utc) + timedelta(hours=1)
            
            task = Task(
                title="Test Deadline Notification Task",
                description="This is a test task to verify deadline notifications",
                deadline=test_deadline,
                priority="High",
                created_by=manager.id,
                status='incompleted'
            )
            
            db.session.add(task)
            db.session.flush()
            
            # Assign to staff user
            assignment = TaskAssignee(task_id=task.id, user_id=staff_user.id)
            db.session.add(assignment)
            db.session.commit()
            
            return jsonify({
                'message': 'Test task created successfully',
                'task_id': task.id,
                'deadline': test_deadline.isoformat(),
                'assigned_to': staff_user.full_name
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Serve avatar files
    @app.route('/avatars/<filename>')
    def serve_avatar(filename):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), filename)
    
    @app.route('/task-files/<task_id>/<filename>')
    def serve_task_file(task_id, filename):
       return send_from_directory(
        os.path.join(app.config['UPLOAD_FOLDER'], 'tasks', task_id),
        filename
    )
    
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    # Error handlers
    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        return jsonify({
            "error": "Unprocessable Entity",
            "message": "The request was well-formed but contained semantic errors"
        }), 422

    @app.errorhandler(400)
    def handle_bad_request(err):
        return jsonify({
            "error": "Bad Request",
            "message": "The request could not be understood by the server"
        }), 400

    @app.errorhandler(401)
    def handle_unauthorized(err):
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication is required to access this resource"
        }), 401

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token(e):
        return jsonify({"error": "session has expired login again"}), 401

    @app.errorhandler(NoAuthorizationError)
    def handle_missing_token(e):
        return jsonify({"error": "Authorization token required"}), 401

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created/verified")
        except Exception as e:
            app.logger.error(f"Database initialization failed: {str(e)}")
            raise

    app.run(debug=True, port=5001, host='0.0.0.0')
