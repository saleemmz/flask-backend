from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from extensions import db, mail
from flask_mail import Message
import logging
from models.support import ContactMessage  
from utils.activitylogger import log_activity

support_bp = Blueprint('support', __name__, url_prefix='/api/support')  

@support_bp.route('/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        email = data.get('email')
        message_text = data.get('message')
        
        if not email or '@' not in email:
            return jsonify({'error': 'Please provide a valid email address'}), 400
            
        if not message_text or len(message_text.strip()) == 0:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Create new contact message record
        contact_message = ContactMessage(
            email=email,
            message=message_text,
            ip_address=request.remote_addr
        )
        db.session.add(contact_message)
        db.session.commit()
        
        # Send email to support team
        msg = Message(
            subject=f"New Support Request from {email}",
            recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
            body=f"Email: {email}\n\nMessage:\n{message_text}"
        )
        mail.send(msg)
        
        current_app.logger.info(f"New contact message received (ID: {contact_message.id}) from {email}")
        
        return jsonify({'message': 'Your message has been sent successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting contact form: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500