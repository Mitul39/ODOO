import os
import json
from flask import Blueprint, request, jsonify, redirect, url_for, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import cloudinary
import cloudinary.uploader
from src.models.user import User, get_db
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_CALLBACK_URL = os.getenv('GOOGLE_CALLBACK_URL')

# Google OAuth flow configuration
client_config = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [GOOGLE_CALLBACK_URL]
    }
}

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Validate email format
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if user already exists
        existing_user = User.find_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        if user.save():
            # Create JWT token
            access_token = create_access_token(identity=str(user._id))
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'token': access_token,
                'user': {
                    'id': str(user._id),
                    'name': user.name,
                    'email': user.email,
                    'photo_url': user.photo_url,
                    'skills_teach': user.skills_teach,
                    'skills_learn': user.skills_learn,
                    'badge_level': user.badge_level
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
            
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.find_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not user.password or not User.check_password(data['password'], user.password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=str(user._id))
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': access_token,
            'user': {
                'id': str(user._id),
                'name': user.name,
                'email': user.email,
                'photo_url': user.photo_url,
                'bio': user.bio,
                'skills_teach': user.skills_teach,
                'skills_learn': user.skills_learn,
                'availability': user.availability,
                'is_public': user.is_public,
                'badge_level': user.badge_level,
                'total_sessions_taught': user.total_sessions_taught,
                'rating': user.rating
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/google', methods=['GET'])
def google_login():
    try:
        # Create flow instance
        flow = Flow.from_client_config(
            client_config,
            scopes=['openid', 'email', 'profile']
        )
        flow.redirect_uri = GOOGLE_CALLBACK_URL
        
        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        # Store state in session for security
        session['state'] = state
        
        return redirect(authorization_url)
        
    except Exception as e:
        print(f"Google login error: {str(e)}")
        return jsonify({'error': 'Failed to initiate Google login'}), 500

@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    try:
        # Verify state parameter
        if request.args.get('state') != session.get('state'):
            return redirect(f"http://localhost:5173/login?error=invalid_state")
        
        # Check for error in callback
        if request.args.get('error'):
            return redirect(f"http://localhost:5173/login?error=google_auth_failed")
        
        # Create flow instance
        flow = Flow.from_client_config(
            client_config,
            scopes=['openid', 'email', 'profile'],
            state=session['state']
        )
        flow.redirect_uri = GOOGLE_CALLBACK_URL
        
        # Fetch token
        flow.fetch_token(authorization_response=request.url)
        
        # Get user info from Google
        credentials = flow.credentials
        request_session = requests.Request()
        
        # Verify the token and get user info
        idinfo = id_token.verify_oauth2_token(
            credentials.id_token,
            request_session,
            GOOGLE_CLIENT_ID
        )
        
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo.get('picture', '')
        
        # Check if user exists
        user = User.find_by_google_id(google_id)
        if not user:
            # Check if user exists with same email
            user = User.find_by_email(email)
            if user:
                # Link Google account to existing user
                user.google_id = google_id
                if not user.photo_url and picture:
                    user.photo_url = picture
                user.save()
            else:
                # Create new user
                user = User(
                    name=name,
                    email=email,
                    google_id=google_id,
                    photo_url=picture
                )
                user.save()
        
        # Create JWT token
        access_token = create_access_token(identity=str(user._id))
        
        # Redirect to frontend with token and user data
        user_data = {
            'id': str(user._id),
            'name': user.name,
            'email': user.email,
            'photo_url': user.photo_url,
            'bio': user.bio,
            'skills_teach': user.skills_teach,
            'skills_learn': user.skills_learn,
            'availability': user.availability,
            'is_public': user.is_public,
            'badge_level': user.badge_level,
            'total_sessions_taught': user.total_sessions_taught,
            'rating': user.rating
        }
        
        # Encode user data for URL
        import urllib.parse
        encoded_user_data = urllib.parse.quote(json.dumps(user_data))
        
        return redirect(f"http://localhost:5173/auth/google/callback?token={access_token}&user={encoded_user_data}")
        
    except Exception as e:
        print(f"Google callback error: {str(e)}")
        return redirect(f"http://localhost:5173/login?error=google_auth_failed")

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': str(user._id),
                'name': user.name,
                'email': user.email,
                'photo_url': user.photo_url,
                'bio': user.bio,
                'skills_teach': user.skills_teach,
                'skills_learn': user.skills_learn,
                'availability': user.availability,
                'is_public': user.is_public,
                'badge_level': user.badge_level,
                'total_sessions_taught': user.total_sessions_taught,
                'rating': user.rating
            }
        }), 200
        
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Invalid token'}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # In a more sophisticated setup, you might want to blacklist the token
        # For now, we'll just return success and let the frontend handle token removal
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create new access token
        new_token = create_access_token(identity=str(user._id))
        
        return jsonify({
            'success': True,
            'token': new_token
        }), 200
        
    except Exception as e:
        print(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500

