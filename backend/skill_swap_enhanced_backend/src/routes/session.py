from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from bson import ObjectId
from src.models.user import get_db, User

session_bp = Blueprint('session', __name__)

@session_bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['participant_id', 'skill', 'scheduled_date', 'duration']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if participant exists
        participant = User.find_by_id(data['participant_id'])
        if not participant:
            return jsonify({'error': 'Participant not found'}), 404
        
        # Check if user is not scheduling with themselves
        if current_user_id == data['participant_id']:
            return jsonify({'error': 'Cannot schedule session with yourself'}), 400
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Parse scheduled date
        try:
            scheduled_date = datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # Create session
        session_data = {
            'teacher_id': ObjectId(current_user_id),
            'student_id': ObjectId(data['participant_id']),
            'skill': data['skill'],
            'description': data.get('description', ''),
            'scheduled_date': scheduled_date,
            'duration': int(data['duration']),  # Duration in minutes
            'status': 'scheduled',  # scheduled, completed, cancelled, missed
            'meeting_link': data.get('meeting_link', ''),
            'notes': data.get('notes', ''),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db.sessions.insert_one(session_data)
        
        if result.inserted_id:
            return jsonify({
                'success': True,
                'message': 'Session scheduled successfully',
                'session_id': str(result.inserted_id)
            }), 201
        else:
            return jsonify({'error': 'Failed to schedule session'}), 500
            
    except Exception as e:
        print(f"Create session error: {str(e)}")
        return jsonify({'error': 'Failed to schedule session'}), 500

@session_bp.route('/sessions/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_sessions(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own data
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get sessions where user is either teacher or student
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'teacher_id': ObjectId(user_id)},
                        {'student_id': ObjectId(user_id)}
                    ]
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'teacher_id',
                    'foreignField': '_id',
                    'as': 'teacher'
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'student_id',
                    'foreignField': '_id',
                    'as': 'student'
                }
            },
            {
                '$unwind': '$teacher'
            },
            {
                '$unwind': '$student'
            },
            {
                '$sort': {'scheduled_date': -1}
            }
        ]
        
        sessions = list(db.sessions.aggregate(pipeline))
        
        # Format response
        formatted_sessions = []
        for session in sessions:
            formatted_session = {
                '_id': str(session['_id']),
                'teacher': {
                    '_id': str(session['teacher']['_id']),
                    'name': session['teacher']['name'],
                    'photo_url': session['teacher'].get('photo_url', '')
                },
                'student': {
                    '_id': str(session['student']['_id']),
                    'name': session['student']['name'],
                    'photo_url': session['student'].get('photo_url', '')
                },
                'skill': session['skill'],
                'description': session['description'],
                'scheduled_date': session['scheduled_date'],
                'duration': session['duration'],
                'status': session['status'],
                'meeting_link': session['meeting_link'],
                'notes': session['notes'],
                'created_at': session['created_at'],
                'updated_at': session['updated_at']
            }
            formatted_sessions.append(formatted_session)
        
        return jsonify({
            'success': True,
            'sessions': formatted_sessions
        }), 200
        
    except Exception as e:
        print(f"Get user sessions error: {str(e)}")
        return jsonify({'error': 'Failed to fetch sessions'}), 500

@session_bp.route('/sessions/<session_id>', methods=['PUT'])
@jwt_required()
def update_session(session_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find the session
        session = db.sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Check if current user is either teacher or student
        if (str(session['teacher_id']) != current_user_id and 
            str(session['student_id']) != current_user_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Prepare update data
        update_data = {'updated_at': datetime.utcnow()}
        
        # Allow updating specific fields
        allowed_fields = ['status', 'meeting_link', 'notes', 'scheduled_date', 'duration']
        for field in allowed_fields:
            if field in data:
                if field == 'scheduled_date':
                    try:
                        update_data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                    except ValueError:
                        return jsonify({'error': 'Invalid date format'}), 400
                else:
                    update_data[field] = data[field]
        
        # Update session
        result = db.sessions.update_one(
            {'_id': ObjectId(session_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            # If session is marked as completed, update user stats
            if data.get('status') == 'completed':
                # Update teacher's session count
                teacher = User.find_by_id(str(session['teacher_id']))
                if teacher:
                    teacher.total_sessions_taught += 1
                    teacher.update_badge_level()
                    teacher.save()
                
                # Update student's session count
                student = User.find_by_id(str(session['student_id']))
                if student:
                    student.total_sessions_attended += 1
                    student.save()
            
            return jsonify({
                'success': True,
                'message': 'Session updated successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to update session'}), 500
            
    except Exception as e:
        print(f"Update session error: {str(e)}")
        return jsonify({'error': 'Failed to update session'}), 500

@session_bp.route('/sessions/<session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find the session
        session = db.sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Check if current user is the teacher (only teacher can delete)
        if str(session['teacher_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete the session
        result = db.sessions.delete_one({'_id': ObjectId(session_id)})
        
        if result.deleted_count > 0:
            return jsonify({
                'success': True,
                'message': 'Session deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete session'}), 500
            
    except Exception as e:
        print(f"Delete session error: {str(e)}")
        return jsonify({'error': 'Failed to delete session'}), 500

@session_bp.route('/sessions/upcoming', methods=['GET'])
@jwt_required()
def get_upcoming_sessions():
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get upcoming sessions (next 7 days)
        now = datetime.utcnow()
        next_week = now + timedelta(days=7)
        
        pipeline = [
            {
                '$match': {
                    '$and': [
                        {
                            '$or': [
                                {'teacher_id': ObjectId(current_user_id)},
                                {'student_id': ObjectId(current_user_id)}
                            ]
                        },
                        {'scheduled_date': {'$gte': now, '$lte': next_week}},
                        {'status': 'scheduled'}
                    ]
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'teacher_id',
                    'foreignField': '_id',
                    'as': 'teacher'
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'student_id',
                    'foreignField': '_id',
                    'as': 'student'
                }
            },
            {
                '$unwind': '$teacher'
            },
            {
                '$unwind': '$student'
            },
            {
                '$sort': {'scheduled_date': 1}
            }
        ]
        
        sessions = list(db.sessions.aggregate(pipeline))
        
        # Format response
        formatted_sessions = []
        for session in sessions:
            formatted_session = {
                '_id': str(session['_id']),
                'teacher': {
                    '_id': str(session['teacher']['_id']),
                    'name': session['teacher']['name'],
                    'photo_url': session['teacher'].get('photo_url', '')
                },
                'student': {
                    '_id': str(session['student']['_id']),
                    'name': session['student']['name'],
                    'photo_url': session['student'].get('photo_url', '')
                },
                'skill': session['skill'],
                'description': session['description'],
                'scheduled_date': session['scheduled_date'],
                'duration': session['duration'],
                'status': session['status'],
                'meeting_link': session['meeting_link'],
                'role': 'teacher' if str(session['teacher_id']) == current_user_id else 'student'
            }
            formatted_sessions.append(formatted_session)
        
        return jsonify({
            'success': True,
            'sessions': formatted_sessions
        }), 200
        
    except Exception as e:
        print(f"Get upcoming sessions error: {str(e)}")
        return jsonify({'error': 'Failed to fetch upcoming sessions'}), 500

