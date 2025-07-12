from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from src.models.user import get_db, User

swap_request_bp = Blueprint('swap_request', __name__)

@swap_request_bp.route('/swap-requests', methods=['POST'])
@jwt_required()
def create_swap_request():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('target_user_id'):
            return jsonify({'error': 'Target user ID is required'}), 400
        
        # Check if target user exists
        target_user = User.find_by_id(data['target_user_id'])
        if not target_user:
            return jsonify({'error': 'Target user not found'}), 404
        
        # Check if user is not requesting themselves
        if current_user_id == data['target_user_id']:
            return jsonify({'error': 'Cannot send request to yourself'}), 400
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Check if request already exists
        existing_request = db.swap_requests.find_one({
            'requester_id': ObjectId(current_user_id),
            'target_user_id': ObjectId(data['target_user_id']),
            'status': 'pending'
        })
        
        if existing_request:
            return jsonify({'error': 'Request already sent to this user'}), 400
        
        # Create swap request
        swap_request = {
            'requester_id': ObjectId(current_user_id),
            'target_user_id': ObjectId(data['target_user_id']),
            'message': data.get('message', ''),
            'status': 'pending',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db.swap_requests.insert_one(swap_request)
        
        if result.inserted_id:
            return jsonify({
                'success': True,
                'message': 'Swap request sent successfully',
                'request_id': str(result.inserted_id)
            }), 201
        else:
            return jsonify({'error': 'Failed to create swap request'}), 500
            
    except Exception as e:
        print(f"Create swap request error: {str(e)}")
        return jsonify({'error': 'Failed to create swap request'}), 500

@swap_request_bp.route('/swap-requests/sent/<user_id>', methods=['GET'])
@jwt_required()
def get_sent_requests(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own data
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get sent requests with target user details
        pipeline = [
            {
                '$match': {
                    'requester_id': ObjectId(user_id)
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'target_user_id',
                    'foreignField': '_id',
                    'as': 'target_user'
                }
            },
            {
                '$unwind': '$target_user'
            },
            {
                '$sort': {'created_at': -1}
            }
        ]
        
        requests = list(db.swap_requests.aggregate(pipeline))
        
        # Format response
        formatted_requests = []
        for req in requests:
            formatted_req = {
                '_id': str(req['_id']),
                'target_user': {
                    '_id': str(req['target_user']['_id']),
                    'name': req['target_user']['name'],
                    'photo_url': req['target_user'].get('photo_url', ''),
                    'skills_teach': req['target_user'].get('skills_teach', [])
                },
                'message': req['message'],
                'status': req['status'],
                'created_at': req['created_at'],
                'updated_at': req['updated_at']
            }
            formatted_requests.append(formatted_req)
        
        return jsonify({
            'success': True,
            'requests': formatted_requests
        }), 200
        
    except Exception as e:
        print(f"Get sent requests error: {str(e)}")
        return jsonify({'error': 'Failed to fetch sent requests'}), 500

@swap_request_bp.route('/swap-requests/received/<user_id>', methods=['GET'])
@jwt_required()
def get_received_requests(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own data
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get received requests with requester details
        pipeline = [
            {
                '$match': {
                    'target_user_id': ObjectId(user_id)
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'requester_id',
                    'foreignField': '_id',
                    'as': 'requester'
                }
            },
            {
                '$unwind': '$requester'
            },
            {
                '$sort': {'created_at': -1}
            }
        ]
        
        requests = list(db.swap_requests.aggregate(pipeline))
        
        # Format response
        formatted_requests = []
        for req in requests:
            formatted_req = {
                '_id': str(req['_id']),
                'requester': {
                    '_id': str(req['requester']['_id']),
                    'name': req['requester']['name'],
                    'photo_url': req['requester'].get('photo_url', ''),
                    'skills_teach': req['requester'].get('skills_teach', [])
                },
                'message': req['message'],
                'status': req['status'],
                'created_at': req['created_at'],
                'updated_at': req['updated_at']
            }
            formatted_requests.append(formatted_req)
        
        return jsonify({
            'success': True,
            'requests': formatted_requests
        }), 200
        
    except Exception as e:
        print(f"Get received requests error: {str(e)}")
        return jsonify({'error': 'Failed to fetch received requests'}), 500

@swap_request_bp.route('/swap-requests/<request_id>/accept', methods=['PUT'])
@jwt_required()
def accept_request(request_id):
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find the request
        swap_request = db.swap_requests.find_one({'_id': ObjectId(request_id)})
        if not swap_request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if current user is the target user
        if str(swap_request['target_user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update request status
        result = db.swap_requests.update_one(
            {'_id': ObjectId(request_id)},
            {
                '$set': {
                    'status': 'accepted',
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'message': 'Request accepted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to accept request'}), 500
            
    except Exception as e:
        print(f"Accept request error: {str(e)}")
        return jsonify({'error': 'Failed to accept request'}), 500

@swap_request_bp.route('/swap-requests/<request_id>/reject', methods=['PUT'])
@jwt_required()
def reject_request(request_id):
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find the request
        swap_request = db.swap_requests.find_one({'_id': ObjectId(request_id)})
        if not swap_request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if current user is the target user
        if str(swap_request['target_user_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update request status
        result = db.swap_requests.update_one(
            {'_id': ObjectId(request_id)},
            {
                '$set': {
                    'status': 'rejected',
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'message': 'Request rejected successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to reject request'}), 500
            
    except Exception as e:
        print(f"Reject request error: {str(e)}")
        return jsonify({'error': 'Failed to reject request'}), 500

@swap_request_bp.route('/swap-requests/<request_id>', methods=['DELETE'])
@jwt_required()
def delete_request(request_id):
    try:
        current_user_id = get_jwt_identity()
        
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find the request
        swap_request = db.swap_requests.find_one({'_id': ObjectId(request_id)})
        if not swap_request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if current user is the requester
        if str(swap_request['requester_id']) != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete the request
        result = db.swap_requests.delete_one({'_id': ObjectId(request_id)})
        
        if result.deleted_count > 0:
            return jsonify({
                'success': True,
                'message': 'Request deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete request'}), 500
            
    except Exception as e:
        print(f"Delete request error: {str(e)}")
        return jsonify({'error': 'Failed to delete request'}), 500

