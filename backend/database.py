"""
============================================
Database Module
LinkedIn Branding Assistant
============================================
Handles MongoDB Atlas connection and provides database access.
"""

from pymongo import MongoClient
from config import Config


class Database:
    """MongoDB Atlas database connection manager."""

    _client = None
    _db = None

    @classmethod
    def initialize(cls):
        """Initialize the MongoDB connection."""
        try:
            cls._client = MongoClient(Config.MONGO_URI)
            # Extract database name from URI or use default
            try:
                cls._db = cls._client.get_default_database()
            except Exception:
                cls._db = cls._client['linkedin_branding']
            # Test the connection
            cls._client.admin.command('ping')
            print("[OK] Connected to MongoDB Atlas successfully!")
        except Exception as e:
            print(f"[ERROR] MongoDB connection error: {e}")
            # Fallback to local MongoDB
            try:
                cls._client = MongoClient('mongodb://localhost:27017/')
                cls._db = cls._client['linkedin_branding']
                cls._client.admin.command('ping')
                print("[OK] Connected to local MongoDB successfully!")
            except Exception as e2:
                print(f"[ERROR] Local MongoDB connection error: {e2}")
                raise

    @classmethod
    def get_db(cls):
        """Get the database instance."""
        if cls._db is None:
            cls.initialize()
        return cls._db

    @classmethod
    def get_collection(cls, collection_name):
        """Get a specific collection from the database."""
        db = cls.get_db()
        return db[collection_name]

    @classmethod
    def close(cls):
        """Close the database connection."""
        if cls._client:
            cls._client.close()
            print("[CLOSED] MongoDB connection closed.")
