from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from bson import ObjectId
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os
from src.models.user import get_db, User

notification_bp = Blueprint('notification', __name__)

# Email configuration
EMAIL_ID = os.getenv('EMAIL_ID')
APP_PASSWORD = os.getenv('APP_PASSWORD')

def send_email(to_email, subject, body):
    """Send email notification"""
    try:
        if not EMAIL_ID or not APP_PASSWORD:
            print("Email credentials not configured")
            return False
        
        msg = MimeMultipart()
        msg['From'] = EMAIL_ID
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MimeText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ID, APP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ID, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending error: {str(e)}")
        return False

@notification_bp.route('/notifications/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_notifications(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own notifications
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get user notifications
        notifications = list(db.notifications.find(
            {'user_id': ObjectId(user_id)}
        ).sort('created_at', -1).limit(50))
        
        # Format response
        formatted_notifications = []
        for notification in notifications:
            formatted_notification = {
                '_id': str(notification['_id']),
                'type': notification['type'],
                'title': notification['title'],
                'message': notification['message'],
                'read': notification.get('read', False),
                'created_at': notification['created_at'],
                'data': notification.get('data', {})
            }
            formatted_notifications.append(formatted_notification)
        
        return jsonify({
            'success': True,
            'notifications': formatted_notifications
        }), 200
        
    except Exception as e:
        print(f"Get user notifications error: {str(e)}")
        return jsonify({'error': 'Failed to fetch notifications'}), 500

@notification_bp.route('/notifications/<notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find the notification
        notification = db.notifications.find_one({'_id': ObjectId(notification_id)})
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        # Check if current user owns the notification
        if str(notification['user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Mark as read
        result = db.notifications.update_one(
            {'_id': ObjectId(notification_id)},
            {'$set': {'read': True, 'read_at': datetime.utcnow()}}
        )
        
        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'message': 'Notification marked as read'
            }), 200
        else:
            return jsonify({'error': 'Failed to mark notification as read'}), 500
            
    except Exception as e:
        print(f"Mark notification read error: {str(e)}")
        return jsonify({'error': 'Failed to mark notification as read'}), 500

@notification_bp.route('/notifications/mark-all-read', methods=['PUT'])
@jwt_required()
def mark_all_notifications_read():
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Mark all user's notifications as read
        result = db.notifications.update_many(
            {'user_id': ObjectId(current_user_id), 'read': False},
            {'$set': {'read': True, 'read_at': datetime.utcnow()}}
        )
        
        return jsonify({
            'success': True,
            'message': f'{result.modified_count} notifications marked as read'
        }), 200
        
    except Exception as e:
        print(f"Mark all notifications read error: {str(e)}")
        return jsonify({'error': 'Failed to mark notifications as read'}), 500

@notification_bp.route('/notifications/send', methods=['POST'])
@jwt_required()
def send_notification():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'type', 'title', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if target user exists
        target_user = User.find_by_id(data['user_id'])
        if not target_user:
            return jsonify({'error': 'Target user not found'}), 404
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Create notification
        notification_data = {
            'user_id': ObjectId(data['user_id']),
            'type': data['type'],  # 'session_reminder', 'new_request', 'request_accepted', 'badge_earned', etc.
            'title': data['title'],
            'message': data['message'],
            'read': False,
            'created_at': datetime.utcnow(),
            'data': data.get('data', {})
        }
        
        result = db.notifications.insert_one(notification_data)
        
        # Send email notification if user has email notifications enabled
        if (target_user.notification_preferences.get('email_notifications', True) and 
            data['type'] in ['session_reminder', 'new_request', 'request_accepted']):
            
            email_subject = f"SkillSwap: {data['title']}"
            email_body = f"""
            <html>
            <body>
                <h2>SkillSwap Notification</h2>
                <h3>{data['title']}</h3>
                <p>{data['message']}</p>
                <br>
                <p>Best regards,<br>The SkillSwap Team</p>
                <hr>
                <p><small>You can manage your notification preferences in your account settings.</small></p>
            </body>
            </html>
            """
            
            send_email(target_user.email, email_subject, email_body)
        
        if result.inserted_id:
            return jsonify({
                'success': True,
                'message': 'Notification sent successfully',
                'notification_id': str(result.inserted_id)
            }), 201
        else:
            return jsonify({'error': 'Failed to send notification'}), 500
            
    except Exception as e:
        print(f"Send notification error: {str(e)}")
        return jsonify({'error': 'Failed to send notification'}), 500

@notification_bp.route('/notifications/session-reminders', methods=['POST'])
def send_session_reminders():
    """Send reminders for upcoming sessions (to be called by a cron job)"""
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find sessions starting in the next 24 hours
        now = datetime.utcnow()
        tomorrow = now + timedelta(hours=24)
        
        upcoming_sessions = list(db.sessions.find({
            'scheduled_date': {'$gte': now, '$lte': tomorrow},
            'status': 'scheduled'
        }))
        
        reminders_sent = 0
        
        for session in upcoming_sessions:
            # Get teacher and student details
            teacher = User.find_by_id(str(session['teacher_id']))
            student = User.find_by_id(str(session['student_id']))
            
            if not teacher or not student:
                continue
            
            # Check if reminder already sent
            existing_reminder = db.notifications.find_one({
                'user_id': {'$in': [session['teacher_id'], session['student_id']]},
                'type': 'session_reminder',
                'data.session_id': str(session['_id'])
            })
            
            if existing_reminder:
                continue
            
            # Create reminder message
            session_time = session['scheduled_date'].strftime('%Y-%m-%d at %H:%M UTC')
            
            # Send reminder to teacher
            if teacher.notification_preferences.get('session_reminders', True):
                teacher_notification = {
                    'user_id': session['teacher_id'],
                    'type': 'session_reminder',
                    'title': 'Upcoming Teaching Session',
                    'message': f'You have a session to teach "{session["skill"]}" to {student.name} on {session_time}',
                    'read': False,
                    'created_at': datetime.utcnow(),
                    'data': {
                        'session_id': str(session['_id']),
                        'participant_name': student.name,
                        'skill': session['skill']
                    }
                }
                db.notifications.insert_one(teacher_notification)
                
                # Send email
                if teacher.notification_preferences.get('email_notifications', True):
                    email_subject = "SkillSwap: Upcoming Teaching Session"
                    email_body = f"""
                    <html>
                    <body>
                        <h2>Session Reminder</h2>
                        <p>Hi {teacher.name},</p>
                        <p>You have an upcoming teaching session:</p>
                        <ul>
                            <li><strong>Skill:</strong> {session['skill']}</li>
                            <li><strong>Student:</strong> {student.name}</li>
                            <li><strong>Date & Time:</strong> {session_time}</li>
                            <li><strong>Duration:</strong> {session['duration']} minutes</li>
                        </ul>
                        {f'<p><strong>Meeting Link:</strong> <a href="{session["meeting_link"]}">{session["meeting_link"]}</a></p>' if session.get('meeting_link') else ''}
                        <p>Best regards,<br>The SkillSwap Team</p>
                    </body>
                    </html>
                    """
                    send_email(teacher.email, email_subject, email_body)
                
                reminders_sent += 1
            
            # Send reminder to student
            if student.notification_preferences.get('session_reminders', True):
                student_notification = {
                    'user_id': session['student_id'],
                    'type': 'session_reminder',
                    'title': 'Upcoming Learning Session',
                    'message': f'You have a session to learn "{session["skill"]}" from {teacher.name} on {session_time}',
                    'read': False,
                    'created_at': datetime.utcnow(),
                    'data': {
                        'session_id': str(session['_id']),
                        'participant_name': teacher.name,
                        'skill': session['skill']
                    }
                }
                db.notifications.insert_one(student_notification)
                
                # Send email
                if student.notification_preferences.get('email_notifications', True):
                    email_subject = "SkillSwap: Upcoming Learning Session"
                    email_body = f"""
                    <html>
                    <body>
                        <h2>Session Reminder</h2>
                        <p>Hi {student.name},</p>
                        <p>You have an upcoming learning session:</p>
                        <ul>
                            <li><strong>Skill:</strong> {session['skill']}</li>
                            <li><strong>Teacher:</strong> {teacher.name}</li>
                            <li><strong>Date & Time:</strong> {session_time}</li>
                            <li><strong>Duration:</strong> {session['duration']} minutes</li>
                        </ul>
                        {f'<p><strong>Meeting Link:</strong> <a href="{session["meeting_link"]}">{session["meeting_link"]}</a></p>' if session.get('meeting_link') else ''}
                        <p>Best regards,<br>The SkillSwap Team</p>
                    </body>
                    </html>
                    """
                    send_email(student.email, email_subject, email_body)
                
                reminders_sent += 1
        
        return jsonify({
            'success': True,
            'message': f'{reminders_sent} session reminders sent'
        }), 200
        
    except Exception as e:
        print(f"Send session reminders error: {str(e)}")
        return jsonify({'error': 'Failed to send session reminders'}), 500

@notification_bp.route('/notifications/preferences/<user_id>', methods=['PUT'])
@jwt_required()
def update_notification_preferences(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is updating their own preferences
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update notification preferences
        if 'notification_preferences' in data:
            user.notification_preferences = data['notification_preferences']
            user.save()
        
        return jsonify({
            'success': True,
            'message': 'Notification preferences updated successfully',
            'preferences': user.notification_preferences
        }), 200
        
    except Exception as e:
        print(f"Update notification preferences error: {str(e)}")
        return jsonify({'error': 'Failed to update notification preferences'}), 500

