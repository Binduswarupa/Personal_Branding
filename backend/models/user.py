"""
============================================
User Model
LinkedIn Branding Assistant
============================================
Handles user data operations with MongoDB.
"""

from datetime import datetime, timezone
import bcrypt
from bson import ObjectId
from database import Database


class UserModel:
    """User model for authentication and profile management."""

    COLLECTION = 'users'

    @classmethod
    def get_collection(cls):
        """Get the users collection."""
        return Database.get_collection(cls.COLLECTION)

    @classmethod
    def create_user(cls, name, email, password, career_goal=''):
        """
        Create a new user with hashed password.
        Returns the created user document or None if email already exists.
        """
        collection = cls.get_collection()

        # Check if email already exists
        if collection.find_one({'email': email.lower()}):
            return None

        # Hash the password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = {
            'name': name.strip(),
            'email': email.lower().strip(),
            'password': hashed_password,
            'career_goal': career_goal.strip(),
            'profile_data': {
                'headline': '',
                'about': '',
                'skills': [],
                'experience': '',
                'projects': '',
                'education': ''
            },
            'branding_score': 0,
            'posts_generated': 0,
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }

        result = collection.insert_one(user)
        user['_id'] = result.inserted_id
        return user

    @classmethod
    def find_by_email(cls, email):
        """Find a user by email address."""
        return cls.get_collection().find_one({'email': email.lower().strip()})

    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by their ObjectId."""
        try:
            return cls.get_collection().find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None

    @classmethod
    def verify_password(cls, stored_password, provided_password):
        """Verify a password against the stored hash."""
        return bcrypt.checkpw(
            provided_password.encode('utf-8'),
            stored_password.encode('utf-8')
        )

    @classmethod
    def update_profile(cls, user_id, profile_data):
        """Update user profile data."""
        return cls.get_collection().update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'profile_data': profile_data,
                    'updated_at': datetime.now(timezone.utc)
                }
            }
        )

    @classmethod
    def update_career_goal(cls, user_id, career_goal):
        """Update user's career goal."""
        return cls.get_collection().update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'career_goal': career_goal,
                    'updated_at': datetime.now(timezone.utc)
                }
            }
        )

    @classmethod
    def increment_posts_count(cls, user_id):
        """Increment the posts generated counter."""
        return cls.get_collection().update_one(
            {'_id': ObjectId(user_id)},
            {
                '$inc': {'posts_generated': 1},
                '$set': {'updated_at': datetime.now(timezone.utc)}
            }
        )

    @classmethod
    def update_branding_score(cls, user_id, score):
        """Update the user's branding score."""
        return cls.get_collection().update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'branding_score': score,
                    'updated_at': datetime.now(timezone.utc)
                }
            }
        )
