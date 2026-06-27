"""
============================================
Authentication Routes
LinkedIn Branding Assistant
============================================
Handles user registration, login, logout, and JWT token management.
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone
import jwt

from config import Config
from models.user import UserModel

auth_bp = Blueprint('auth', __name__)


def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401

        try:
            # Decode the JWT token
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            current_user = UserModel.find_by_id(data['user_id'])

            if not current_user:
                return jsonify({'error': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Validate email format
        email = data['email'].strip()
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400

        # Validate password length
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        # Create the user
        user = UserModel.create_user(
            name=data['name'],
            email=email,
            password=data['password'],
            career_goal=data.get('career_goal', '')
        )

        if not user:
            return jsonify({'error': 'Email already registered'}), 409

        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'email': user['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }, Config.JWT_SECRET, algorithm='HS256')

        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'career_goal': user.get('career_goal', '')
            }
        }), 201

    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        # Find the user
        user = UserModel.find_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password
        if not UserModel.verify_password(user['password'], data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'email': user['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
        }, Config.JWT_SECRET, algorithm='HS256')

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'career_goal': user.get('career_goal', ''),
                'branding_score': user.get('branding_score', 0),
                'posts_generated': user.get('posts_generated', 0)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current authenticated user's profile."""
    return jsonify({
        'user': {
            'id': str(current_user['_id']),
            'name': current_user['name'],
            'email': current_user['email'],
            'career_goal': current_user.get('career_goal', ''),
            'profile_data': current_user.get('profile_data', {}),
            'branding_score': current_user.get('branding_score', 0),
            'posts_generated': current_user.get('posts_generated', 0),
            'created_at': str(current_user.get('created_at', ''))
        }
    }), 200


@auth_bp.route('/update-profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile information."""
    try:
        data = request.get_json()
        user_id = str(current_user['_id'])

        # Update career goal if provided
        if 'career_goal' in data:
            UserModel.update_career_goal(user_id, data['career_goal'])

        # Update profile data if provided
        if 'profile_data' in data:
            UserModel.update_profile(user_id, data['profile_data'])

        # Fetch updated user
        updated_user = UserModel.find_by_id(user_id)

        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': str(updated_user['_id']),
                'name': updated_user['name'],
                'email': updated_user['email'],
                'career_goal': updated_user.get('career_goal', ''),
                'profile_data': updated_user.get('profile_data', {}),
                'branding_score': updated_user.get('branding_score', 0)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Profile update failed: {str(e)}'}), 500
