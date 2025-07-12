from flask import Flask, jsonify, request, send_from_directory
from extensions import db, mail, cors, migrate
import os
from dotenv import load_dotenv
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError
from apscheduler.schedulers.background import BackgroundScheduler
import time
import atexit
import pymysql

from sqlalchemy import text
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()
pymysql.install_as_MySQLdb()


# Import blueprints
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

scheduler = None

def check_deadlines_job():
    try:
        from utils.sendnotification import check_and_notify_approaching_deadlines
        with db.app.app_context():
            result = check_and_notify_approaching_deadlines()
            print(f"Deadline check job completed with result: {result}")
    except Exception as e:
        print(f"Error in deadline check job: {str(e)}")

def create_app():
    global scheduler
    app = Flask(__name__, static_folder='uploads')

    # Detect environment
    app_env = os.getenv('APP_ENV', 'development').lower()
    hostname = os.getenv("FLASK_RUN_HOST", "")
    is_dev = app_env != 'production' or hostname.startswith("127.") or "localhost" in hostname
    print("APP_ENV =", app_env)
    print("FLASK_RUN_HOST =", hostname)
    print("Is Development =", is_dev)

    # File uploads
    upload_folder = '/tmp/uploads' if os.getenv("RENDER") else os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Base configuration
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
        'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=6),
        'JWT_TOKEN_LOCATION': ['cookies', 'headers'],
        'JWT_COOKIE_CSRF_PROTECT': False,
        'JWT_ACCESS_COOKIE_PATH': '/',
        'JWT_REFRESH_COOKIE_PATH': '/',
        'JWT_COOKIE_SECURE': not is_dev,
        'JWT_COOKIE_SAMESITE': 'None' if not is_dev else 'Lax',
        'JWT_ACCESS_COOKIE_NAME': 'access_token_cookie',
        'MAIL_SERVER': os.getenv('MAIL_SERVER'),
        'MAIL_PORT': int(os.getenv('MAIL_PORT')),
        'MAIL_USE_TLS': os.getenv('MAIL_USE_TLS').lower() == 'true',
        'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
        'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
        'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER'),
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN')
    })

    # CORS setup
    cors_origins = ["https://secureprojectracker.netlify.app"] if app_env == 'production' else ["http://localhost:5173"]
    debug_mode = app_env != 'production'

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app, supports_credentials=True, origins=cors_origins)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return False

    # Scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        db.app = app
        scheduler.add_job(
            func=check_deadlines_job,
            trigger="interval",
            minutes=30,
            id='deadline_check',
            replace_existing=True
        )
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown() if scheduler else None)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(password_recovery_bp, url_prefix='/auth')
    app.register_blueprint(admindashboard_bp, url_prefix='/admin')
    app.register_blueprint(task_bp, url_prefix='/tasks')
    app.register_blueprint(manager_bp, url_prefix='/manager')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(keyholder_bp, url_prefix='/keyholder')
    app.register_blueprint(nonkeyholder_bp, url_prefix='/nonkeyholder')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(activity_bp, url_prefix='/activity')
    app.register_blueprint(settings_bp, url_prefix='/settings')

    # Request hooks
    @app.before_request
    def log_token():
        token = request.cookies.get("access_token_cookie")
        print("JWT Cookie Token:", token)

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({"status": "preflight"})
            response.headers.update({
                "Access-Control-Allow-Origin": request.headers.get('Origin'),
                "Access-Control-Allow-Headers": "Content-Type,Authorization,Accept,X-Requested-With",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                "Access-Control-Allow-Credentials": "true"
            })
            return response

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    # Routes
    @app.route('/')
    def index():
        return {'message': 'Welcome to SPT API'}

    @app.route('/test-token')
    @jwt_required()
    def test_token():
        return jsonify({'user_id': get_jwt_identity()})

    @app.route('/test-db')
    def test_db():
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).fetchone()
                if result and result[0] == 1:
                    return jsonify({'status': 'Database connection successful'}), 200
                raise Exception("Unexpected result")
        except Exception as e:
            app.logger.error(f"Database test failed: {str(e)}")
            return jsonify({'error': 'DB failed', 'details': str(e)}), 500

    @app.route('/avatars/<filename>')
    def serve_avatar(filename):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), filename)

    @app.route('/task-files/<task_id>/<filename>')
    def serve_task_file(task_id, filename):
        try:
            safe_filename = secure_filename(filename)
            if not safe_filename or safe_filename != filename:
                return jsonify({'error': 'Invalid filename'}), 400
            directory = os.path.join(app.config['UPLOAD_FOLDER'], 'tasks', task_id)
            file_path = os.path.join(directory, safe_filename)
            if not os.path.exists(file_path):
                return jsonify({'error': 'File not found'}), 404
            return send_from_directory(directory, safe_filename)
        except Exception as e:
            app.logger.error(f"Error serving file: {str(e)}")
            return jsonify({'error': 'File error'}), 500

    # Error handlers
    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        return jsonify({"error": "Unprocessable Entity"}), 422

    @app.errorhandler(400)
    def handle_bad_request(err):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(401)
    def handle_unauthorized(err):
        return jsonify({
            "error": "Session expired",
            "message": "Please login again.",
            "action": "login_required",
            "redirect": "/login"
        }), 401

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token(e):
        return handle_unauthorized(e)

    @app.errorhandler(NoAuthorizationError)
    def handle_missing_token(e):
        return handle_unauthorized(e)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

app = create_app()

if __name__ == '__main__':
    app_env = os.getenv('APP_ENV', 'development').lower()
    if app_env in ['development', 'testing']:
        with app.app_context():
            try:
                db.create_all()
                app.logger.info("Tables created locally.")
            except Exception as e:
                app.logger.error(f"DB init failed: {str(e)}")
    app.run(debug=(app_env == 'development'), port=5001, host='0.0.0.0')
