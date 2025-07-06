from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.activity import Activity
from models.user import User
from datetime import datetime, timedelta
from extensions import db
from flask import send_file
from io import BytesIO

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_activity_logs():
    current_user = User.query.get(get_jwt_identity())
    if not current_user or current_user.role not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized'}), 403

    # Get filters from query params
    date_range = request.args.get('date_range', 'all')
    category = request.args.get('category', 'all')
    user_id = request.args.get('user_id', None)
    search = request.args.get('search', '')

    query = Activity.query.outerjoin(User)

    # Apply filters
    if date_range != 'all':
        now = datetime.utcnow()
        if date_range == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(Activity.timestamp >= start)
        elif date_range == 'week':
            start = now - timedelta(days=7)
            query = query.filter(Activity.timestamp >= start)
        elif date_range == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(Activity.timestamp >= start)

    if category != 'all':
        query = query.filter(Activity.category == category)

    if user_id:
        query = query.filter(Activity.user_id == user_id)

    if search:
        search = f"%{search}%"
        query = query.filter(
            (Activity.action.ilike(search)) | 
            (User.full_name.ilike(search))
        )

    # Get results
    logs = query.order_by(Activity.timestamp.desc()).limit(100).all()
    
    return jsonify({
        'logs': [log.to_dict() for log in logs]
    }), 200
    
@activity_bp.route('/export', methods=['GET'])
@jwt_required()
def export_activity_logs():
    current_user = User.query.get(get_jwt_identity())
    if not current_user or current_user.role not in ['admin', 'manager']:
        return jsonify({'error': 'Unauthorized'}), 403

    # Get filters from query params
    date_range = request.args.get('date_range', 'today')
    category = request.args.get('category', 'all')
    user_id = request.args.get('user_id', None)
    search = request.args.get('search', '')

    query = Activity.query.outerjoin(User)

    # Apply filters (same as get_activity_logs)
    if date_range != 'all':
        now = datetime.utcnow()
        if date_range == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(Activity.timestamp >= start)
        elif date_range == 'week':
            start = now - timedelta(days=7)
            query = query.filter(Activity.timestamp >= start)
        elif date_range == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            query = query.filter(Activity.timestamp >= start)

    if category != 'all':
        query = query.filter(Activity.category == category)

    if user_id:
        query = query.filter(Activity.user_id == user_id)

    if search:
        search = f"%{search}%"
        query = query.filter (
            (Activity.action.ilike(search)) | 
            (User.full_name.ilike(search))
        )
    
    logs = query.order_by(Activity.timestamp.desc()).all()
    
    return generate_csv(logs)

def generate_csv(logs):
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Date', 'Time', 'User', 'Category', 'Action'])
    
    # Write rows
    for log in logs:
        timestamp = datetime.fromisoformat(log.timestamp.isoformat())
        writer.writerow([
            timestamp.strftime('%Y-%m-%d'),
            timestamp.strftime('%H:%M:%S'),
            log.user.full_name if log.user else 'Unknown',
            log.category.capitalize(),
            log.action
        ])
    
    output.seek(0)
    
    return send_file(
        BytesIO(output.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=f"activity-logs-{datetime.utcnow().strftime('%Y-%m-%d')}.csv",
        mimetype='text/csv'
    )