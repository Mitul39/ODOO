from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import cloudinary
import cloudinary.uploader
import os
from src.models.user import User

user_bp = Blueprint('user', __name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        # Get query parameters
        is_public = request.args.get('is_public', 'true').lower() == 'true'
        search = request.args.get('search', '')
        
        if is_public:
            users = User.get_all_public_users()
        else:
            # For now, only return public users
            users = User.get_all_public_users()
        
        # Filter by search term if provided
        if search:
            search_lower = search.lower()
            filtered_users = []
            for user in users:
                if (search_lower in user.name.lower() or 
                    search_lower in user.bio.lower() or
                    any(search_lower in skill.lower() for skill in user.skills_teach) or
                    any(search_lower in skill.lower() for skill in user.skills_learn)):
                    filtered_users.append(user)
            users = filtered_users
        
        # Convert to dict format
        users_data = []
        for user in users:
            user_dict = user.to_dict()
            user_dict['_id'] = str(user_dict['_id'])
            # Remove sensitive information
            user_dict.pop('password', None)
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'users': users_data
        }), 200
        
    except Exception as e:
        print(f"Get users error: {str(e)}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_dict = user.to_dict()
        user_dict['_id'] = str(user_dict['_id'])
        # Remove sensitive information
        user_dict.pop('password', None)
        
        return jsonify({
            'success': True,
            'user': user_dict
        }), 200
        
    except Exception as e:
        print(f"Get user error: {str(e)}")
        return jsonify({'error': 'Failed to fetch user'}), 500

@user_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update user profile
        if 'bio' in data:
            user.bio = data['bio']
        if 'skills_teach' in data:
            user.skills_teach = data['skills_teach']
        if 'skills_learn' in data:
            user.skills_learn = data['skills_learn']
        if 'availability' in data:
            user.availability = data['availability']
        if 'is_public' in data:
            user.is_public = data['is_public']
        
        if user.save():
            user_dict = user.to_dict()
            user_dict['_id'] = str(user_dict['_id'])
            user_dict.pop('password', None)
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'user': user_dict
            }), 200
        else:
            return jsonify({'error': 'Failed to update profile'}), 500
            
    except Exception as e:
        print(f"Create user profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile'}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is updating their own profile
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update user profile
        if 'name' in data:
            user.name = data['name']
        if 'bio' in data:
            user.bio = data['bio']
        if 'skills_teach' in data:
            user.skills_teach = data['skills_teach']
        if 'skills_learn' in data:
            user.skills_learn = data['skills_learn']
        if 'availability' in data:
            user.availability = data['availability']
        if 'is_public' in data:
            user.is_public = data['is_public']
        if 'notification_preferences' in data:
            user.notification_preferences = data['notification_preferences']
        
        if user.save():
            user_dict = user.to_dict()
            user_dict['_id'] = str(user_dict['_id'])
            user_dict.pop('password', None)
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'user': user_dict
            }), 200
        else:
            return jsonify({'error': 'Failed to update profile'}), 500
            
    except Exception as e:
        print(f"Update user error: {str(e)}")
        return jsonify({'error': 'Failed to update profile'}), 500

@user_bp.route('/users/upload-image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Upload to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                folder="skillswap/profile_images",
                transformation=[
                    {'width': 400, 'height': 400, 'crop': 'fill'},
                    {'quality': 'auto'},
                    {'format': 'jpg'}
                ]
            )
            
            image_url = upload_result['secure_url']
            
            # Update user's photo URL
            user.photo_url = image_url
            user.save()
            
            return jsonify({
                'success': True,
                'message': 'Image uploaded successfully',
                'imageUrl': image_url
            }), 200
            
        except Exception as upload_error:
            print(f"Cloudinary upload error: {str(upload_error)}")
            return jsonify({'error': 'Failed to upload image'}), 500
            
    except Exception as e:
        print(f"Upload image error: {str(e)}")
        return jsonify({'error': 'Failed to upload image'}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is deleting their own account
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # For now, we'll just mark the user as inactive instead of deleting
        # In a real application, you might want to handle this differently
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_public = False
        user.save()
        
        return jsonify({
            'success': True,
            'message': 'Account deactivated successfully'
        }), 200
        
    except Exception as e:
        print(f"Delete user error: {str(e)}")
        return jsonify({'error': 'Failed to delete account'}), 500

@user_bp.route('/users/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'stats': {
                'total_sessions_taught': user.total_sessions_taught,
                'total_sessions_attended': user.total_sessions_attended,
                'rating': user.rating,
                'badge_level': user.badge_level,
                'skills_count': {
                    'teaching': len(user.skills_teach),
                    'learning': len(user.skills_learn)
                }
            }
        }), 200
        
    except Exception as e:
        print(f"Get user stats error: {str(e)}")
        return jsonify({'error': 'Failed to fetch user stats'}), 500

