from models.activity import Activity
from extensions import db
from datetime import datetime

def log_activity(user_id, action, category):
    """
    Log user activity
    
    Args:
        user_id: ID of the user performing the action (can be None for anonymous actions)
        action: Description of the action (e.g., "Logged in to the system")
        category: One of ['login', 'logout', 'profile', 'password', 'task', 'file', 'user']
    """
    try:
        activity = Activity(
            user_id=user_id,
            action=action,
            category=category
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log the error but don't break the application
        print(f"Failed to log activity: {str(e)}")
