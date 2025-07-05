from flask import current_app
from flask_mail import Message
from extensions import mail
from models.task import Notification
from models.user import User, UserPreference
from models.task import Task, TaskAssignee
from datetime import datetime, timedelta, timezone
from extensions import db
from email.utils import formataddr
import logging

logger = logging.getLogger(__name__)

def create_in_app_notification(user_id, title, message, notification_type, task_id=None):
    """Create an in-app notification with proper timezone handling"""
    try:
        # Ensure we're using UTC timezone
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            related_task_id=task_id,
            created_at=datetime.now(timezone.utc)  # Explicitly set UTC timezone
        )
        db.session.add(notification)
        db.session.commit()
        logger.info(f"Created notification for user {user_id}: {title} at {notification.created_at}")
        return notification
    except Exception as e:
        logger.error(f"Error creating in-app notification: {str(e)}", exc_info=True)
        db.session.rollback()
        return None

def should_send_email_notification(user_id, notification_type=None):
    """Check if user has email notifications enabled"""
    try:
        # Always send security-related notifications
        security_types = ['password_reset', 'email_change', 'account_security']
        if notification_type in security_types:
            return True
        
        # Check user preference for other notifications
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        if not preference:
            # Create default preference if it doesn't exist
            preference = UserPreference(
                user_id=user_id,
                email_notifications=True  # Default to enabled
            )
            db.session.add(preference)
            db.session.commit()
            return True
        
        return preference.email_notifications
    except Exception as e:
        logger.error(f"Error checking email notification preference for user {user_id}: {str(e)}")
        # Default to sending notifications if we can't check preference
        return True

def send_email_notification(email, subject, message, html_message=None, user_id=None, notification_type=None):
    """Send an email notification if user has email notifications enabled"""
    try:
        # Check if we should send email notification
        if user_id and not should_send_email_notification(user_id, notification_type):
            logger.info(f"Email notifications disabled for user {user_id}, skipping email")
            return True
        
        msg = Message(
            subject=subject,
            recipients=[email],
            sender=formataddr(("noreplyspt", "saleemm1137@gmail.com")),
            body=message,
            html=html_message
        )
        mail.send(msg)
        logger.info(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Error sending email notification to {email}: {str(e)}", exc_info=True)
        return False

def notify_task_assignment(task_id, assignee_id):
    """Notify staff about task assignment"""
    try:
        task = Task.query.get(task_id)
        assignee = User.query.get(assignee_id)
        
        if not task or not assignee:
            logger.warning(f"Task {task_id} or assignee {assignee_id} not found")
            return False
            
        # In-app notification with current timestamp
        title = "New Task Assigned"
        message = f"You have been assigned a new task: '{task.title}'"
        create_in_app_notification(
            assignee_id,
            title,
            message,
            'task_assignment',
            task_id
        )
        
        # Email notification (respects user preference)
        email_subject = "New Task Assignment"
        email_message = f"""Hello {assignee.full_name},
        
You have been assigned a new task: {task.title}.
Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M UTC') if task.deadline else 'No deadline'}

Please log in to your account to view the details.
"""
        html_message = f"""<html>
            <body>
                <p>Hello {assignee.full_name},</p>
                <p>You have been assigned a new task: <strong>{task.title}</strong></p>
                <p>Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M UTC') if task.deadline else 'No deadline'}</p>
                <p>Please log in to your account to view the details.</p>
            </body>
        </html>"""
        
        send_email_notification(
            assignee.email, 
            email_subject, 
            email_message, 
            html_message, 
            assignee_id, 
            'task_assignment'
        )
        return True
    except Exception as e:
        logger.error(f"Error in task assignment notification: {str(e)}", exc_info=True)
        return False

def notify_task_completion(task_id, staff_id):
    """Notify manager about task completion"""
    try:
        task = Task.query.get(task_id)
        staff = User.query.get(staff_id)
        manager = User.query.get(task.created_by)
        
        if not task or not staff or not manager:
            logger.warning(f"Task {task_id}, staff {staff_id}, or manager not found")
            return False
            
        # In-app notification with current timestamp
        title = "Task Completed"
        message = f"{staff.full_name} has completed the task: '{task.title}'"
        create_in_app_notification(
            manager.id,
            title,
            message,
            'task_completion',
            task_id
        )
        
        # Email notification (respects user preference)
        email_subject = "Task Completed"
        email_message = f"""Hello {manager.full_name},
        
{staff.full_name} has completed the task: {task.title}.
        
Please log in to review the submission.
"""
        html_message = f"""<html>
            <body>
                <p>Hello {manager.full_name},</p>
                <p>{staff.full_name} has completed the task: <strong>{task.title}</strong></p>
                <p>Please log in to review the submission.</p>
            </body>
        </html>"""
        
        send_email_notification(
            manager.email, 
            email_subject, 
            email_message, 
            html_message, 
            manager.id, 
            'task_completion'
        )
        return True
    except Exception as e:
        logger.error(f"Error in task completion notification: {str(e)}", exc_info=True)
        return False

def get_deadline_debug_info():
    """Get debug information about tasks and their deadlines"""
    try:
        now = datetime.now(timezone.utc)
        logger.info(f"Debug: Current time (UTC): {now}")
        
        # Get all incomplete tasks
        all_tasks = Task.query.filter(Task.status == 'incompleted').all()
        logger.info(f"Debug: Found {len(all_tasks)} incomplete tasks total")
        
        debug_info = {
            'current_time_utc': now.isoformat(),
            'total_incomplete_tasks': len(all_tasks),
            'tasks': []
        }
        
        for task in all_tasks:
            task_deadline = task.deadline
            if task_deadline:
                # Handle timezone-naive deadlines
                if task_deadline.tzinfo is None:
                    task_deadline_utc = task_deadline.replace(tzinfo=timezone.utc)
                else:
                    task_deadline_utc = task_deadline.astimezone(timezone.utc)
                
                time_diff = task_deadline_utc - now
                hours_until = time_diff.total_seconds() / 3600
                
                # Get assignees count
                assignee_count = TaskAssignee.query.filter_by(task_id=task.id).count()
                
                task_info = {
                    'id': task.id,
                    'title': task.title,
                    'deadline_original': task.deadline.isoformat() if task.deadline else None,
                    'deadline_utc': task_deadline_utc.isoformat(),
                    'hours_until_deadline': round(hours_until, 2),
                    'assignee_count': assignee_count,
                    'is_future': hours_until > 0,
                    'within_48h': 0 < hours_until <= 48,
                    'within_24h': 0 < hours_until <= 24,
                    'within_2h': 0 < hours_until <= 2
                }
                debug_info['tasks'].append(task_info)
        
        return debug_info
    except Exception as e:
        logger.error(f"Error getting debug info: {str(e)}", exc_info=True)
        return {'error': str(e)}

def check_and_notify_approaching_deadlines():
    """Check for tasks with approaching deadlines and notify staff"""
    try:
        now = datetime.now(timezone.utc)
        logger.info(f"Starting deadline check at {now}")
        
        # Get debug info first
        debug_info = get_deadline_debug_info()
        logger.info(f"Debug info: {debug_info}")
        
        # Check for tasks due within the next 48 hours
        threshold_48h = now + timedelta(hours=48)
        
        # Modified query to handle timezone-naive deadlines
        tasks = Task.query.filter(
            Task.status == 'incompleted',
            Task.deadline.isnot(None)
        ).all()
        
        # Filter tasks manually to handle timezone issues
        eligible_tasks = []
        for task in tasks:
            task_deadline = task.deadline
            if task_deadline:
                # Handle timezone-naive deadlines
                if task_deadline.tzinfo is None:
                    task_deadline_utc = task_deadline.replace(tzinfo=timezone.utc)
                else:
                    task_deadline_utc = task_deadline.astimezone(timezone.utc)
                
                # Check if deadline is in the future and within 48 hours
                if now < task_deadline_utc <= threshold_48h:
                    eligible_tasks.append((task, task_deadline_utc))
        
        logger.info(f"Found {len(eligible_tasks)} tasks with approaching deadlines")
        
        if not eligible_tasks:
            logger.info("No tasks found with approaching deadlines")
            return False
        
        notifications_sent = 0
        
        for task, task_deadline_utc in eligible_tasks:
            logger.info(f"Processing task {task.id}: {task.title}, deadline: {task_deadline_utc}")
            
            # Calculate hours until deadline
            time_until_deadline = task_deadline_utc - now
            hours_until_deadline = time_until_deadline.total_seconds() / 3600
            
            # Determine notification type and urgency
            if hours_until_deadline <= 2:
                notification_type = 'task_due_soon'
                title = "Task Due Very Soon"
                urgency = "within 2 hours"
                spam_prevention_hours = 1
            elif hours_until_deadline <= 24:
                notification_type = 'deadline_approaching_24h'
                title = "Deadline Approaching"
                urgency = f"in {int(hours_until_deadline)} hours"
                spam_prevention_hours = 4
            else:
                notification_type = 'deadline_approaching_48h'
                title = "Deadline Reminder"
                urgency = f"in {int(hours_until_deadline)} hours"
                spam_prevention_hours = 12
            
            # Get task assignees using proper join
            assignees = db.session.query(User).join(TaskAssignee).filter(
                TaskAssignee.task_id == task.id
            ).all()
            
            logger.info(f"Task {task.id} has {len(assignees)} assignees")
            
            if not assignees:
                logger.warning(f"Task {task.id} has no assignees")
                continue
            
            for assignee in assignees:
                # Check if we already sent a notification for this urgency level recently
                spam_check_time = now - timedelta(hours=spam_prevention_hours)
                recent_notification = Notification.query.filter(
                    Notification.user_id == assignee.id,
                    Notification.related_task_id == task.id,
                    Notification.notification_type == notification_type,
                    Notification.created_at > spam_check_time
                ).first()
                
                if recent_notification:
                    logger.info(f"Skipping notification for user {assignee.id}, task {task.id} - recent notification exists")
                    continue
                
                # Create in-app notification
                message = f"Task '{task.title}' is due {urgency}"
                notification = create_in_app_notification(
                    assignee.id,
                    title,
                    message,
                    notification_type,
                    task.id
                )
                
                if notification:
                    notifications_sent += 1
                    logger.info(f"Created notification for user {assignee.id}, task {task.id}")
                
                # Send email notification (respects user preference)
                email_subject = f"Task Deadline Alert - {title}"
                email_message = f"""Hello {assignee.full_name},
                
The task '{task.title}' is due {urgency}.
Deadline: {task_deadline_utc.strftime('%Y-%m-%d %H:%M UTC')}
                
Please complete the task before the deadline.
"""
                html_message = f"""<html>
                    <body>
                        <p>Hello {assignee.full_name},</p>
                        <p>The task <strong>{task.title}</strong> is due {urgency}.</p>
                        <p>Please complete the task before the deadline.</p>
                    </body>
                </html>"""
                
                send_email_notification(
                    assignee.email, 
                    email_subject, 
                    email_message, 
                    html_message, 
                    assignee.id, 
                    'deadline_approaching'
                )
                
        logger.info(f"Deadline check completed. Sent {notifications_sent} notifications for {len(eligible_tasks)} tasks")
        return notifications_sent > 0 or len(eligible_tasks) > 0
        
    except Exception as e:
        logger.error(f"Error in deadline notification: {str(e)}", exc_info=True)
        return False

def notify_task_due(task_id):
    """Notify staff when task is overdue"""
    try:
        task = Task.query.get(task_id)
        
        if not task or task.status == 'completed':
            return False
            
        now = datetime.now(timezone.utc)
        
        # Handle timezone-naive deadlines
        task_deadline = task.deadline
        if task_deadline.tzinfo is None:
            task_deadline_utc = task_deadline.replace(tzinfo=timezone.utc)
        else:
            task_deadline_utc = task_deadline.astimezone(timezone.utc)
        
        # Only notify if the deadline has actually passed
        if task_deadline_utc > now:
            return False
            
        assignees = db.session.query(User).join(TaskAssignee).filter(
            TaskAssignee.task_id == task.id
        ).all()
            
        for assignee in assignees:
            # Check if we already sent an overdue notification for this task
            existing_notification = Notification.query.filter(
                Notification.user_id == assignee.id,
                Notification.related_task_id == task.id,
                Notification.notification_type == 'task_overdue'
            ).first()
            
            if existing_notification:
                continue
                
            # In-app notification
            title = "Task Overdue"
            message = f"Task '{task.title}' is now overdue"
            create_in_app_notification(
                assignee.id,
                title,
                message,
                'task_overdue',
                task.id
            )
            
            # Email notification (respects user preference)
            email_subject = "Task Overdue"
            email_message = f"""Hello {assignee.full_name},
            
The task '{task.title}' is now overdue.
Original deadline: {task_deadline_utc.strftime('%Y-%m-%d %H:%M UTC')}
            
Please complete the task as soon as possible.
"""
            html_message = f"""<html>
                <body>
                    <p>Hello {assignee.full_name},</p>
                    <p>The task <strong>{task.title}</strong> is now overdue.</p>
                    <p>Original deadline: {task_deadline_utc.strftime('%Y-%m-%d %H:%M UTC')}</p>
                    <p>Please complete the task as soon as possible.</p>
                </body>
            </html>"""
            
            send_email_notification(
                assignee.email, 
                email_subject, 
                email_message, 
                html_message, 
                assignee.id, 
                'task_overdue'
            )
        return True
    except Exception as e:
        logger.error(f"Error in task due notification: {str(e)}", exc_info=True)
        return False

def notify_new_user_signup(user_id):
    """Notify managers when a new user signs up"""
    try:
        new_user = User.query.get(user_id)
        if not new_user:
            return False
            
        # Get all managers
        managers = User.query.filter(User.role.in_(['manager', 'admin'])).all()
        
        for manager in managers:
            title = "New Staff Registration"
            message = f"A new user has signed up: {new_user.full_name} ({new_user.email})"
            create_in_app_notification(
                manager.id,
                title,
                message,
                'new_user',
                None
            )
            
            # Email notification (respects user preference)
            email_subject = "New User Registration"
            email_message = f"""Hello {manager.full_name},
            
A new user has registered on Secure Project Tracker:
Name: {new_user.full_name}
Email: {new_user.email}
Role: {new_user.role}

Please verify their account if needed.
"""
            html_message = f"""<html>
                <body>
                    <p>Hello {manager.full_name},</p>
                    <p>A new user has registered on Secure Project Tracker:</p>
                    <ul>
                        <li>Name: {new_user.full_name}</li>
                        <li>Email: {new_user.email}</li>
                        <li>Role: {new_user.role}</li>
                    </ul>
                    <p>Please verify their account if needed.</p>
                </body>
            </html>"""
            
            send_email_notification(
                manager.email, 
                email_subject, 
                email_message, 
                html_message, 
                manager.id, 
                'new_user'
            )
        return True
    except Exception as e:
        logger.error(f"Error in new user signup notification: {str(e)}", exc_info=True)
        return False
    
def notify_task_deletion(task_id, manager_id):
    """Notify staff when a manager deletes a task they were assigned to"""
    try:
        task = Task.query.get(task_id)
        manager = User.query.get(manager_id)
        
        if not task or not manager:
            return False
            
        assignees = db.session.query(User).join(TaskAssignee).filter(
            TaskAssignee.task_id == task.id
        ).all()
            
        for assignee in assignees:
            # In-app notification
            title = "Task Deleted"
            message = f"The task '{task.title}' has been deleted by {manager.full_name}"
            create_in_app_notification(
                assignee.id,
                title,
                message,
                'task_deletion',
                task_id
            )
            
            # Email notification (respects user preference)
            email_subject = "Task Deleted"
            email_message = f"""Hello {assignee.full_name},
            
The task '{task.title}' has been deleted by {manager.full_name}.

If you have any questions, please contact the manager.
"""
            html_message = f"""<html>
                <body>
                    <p>Hello {assignee.full_name},</p>
                    <p>The task <strong>{task.title}</strong> has been deleted by {manager.full_name}.</p>
                    <p>If you have any questions, please contact the manager.</p>
                </body>
            </html>"""
            
            send_email_notification(
                assignee.email, 
                email_subject, 
                email_message, 
                html_message, 
                assignee.id, 
                'task_deletion'
            )
        
        return True
    except Exception as e:
        logger.error(f"Error in task deletion notification: {str(e)}", exc_info=True)
        return False
