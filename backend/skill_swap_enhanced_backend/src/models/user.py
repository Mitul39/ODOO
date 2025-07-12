import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import bcrypt

# MongoDB connection
client = None
db = None

def init_db():
    global client, db
    mongodb_uri = os.getenv('MONGODB_URI')
    if mongodb_uri:
        client = MongoClient(mongodb_uri)
        db = client.skillswap
        print("Connected to MongoDB")
    else:
        print("MongoDB URI not found in environment variables")

def get_db():
    return db

class User:
    def __init__(self, name, email, password=None, google_id=None, photo_url=None):
        self.name = name
        self.email = email
        self.password = self.hash_password(password) if password else None
        self.google_id = google_id
        self.photo_url = photo_url
        self.bio = ""
        self.skills_teach = []
        self.skills_learn = []
        self.availability = ""
        self.is_public = True
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.total_sessions_taught = 0
        self.total_sessions_attended = 0
        self.rating = 0.0
        self.badge_level = "Bronze"
        self.notification_preferences = {
            "email_notifications": True,
            "session_reminders": True,
            "new_requests": True
        }

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def to_dict(self):
        return {
            "_id": getattr(self, '_id', None),
            "name": self.name,
            "email": self.email,
            "google_id": self.google_id,
            "photo_url": self.photo_url,
            "bio": self.bio,
            "skills_teach": self.skills_teach,
            "skills_learn": self.skills_learn,
            "availability": self.availability,
            "is_public": self.is_public,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "total_sessions_taught": self.total_sessions_taught,
            "total_sessions_attended": self.total_sessions_attended,
            "rating": self.rating,
            "badge_level": self.badge_level,
            "notification_preferences": self.notification_preferences
        }

    def save(self):
        db = get_db()
        if db is None:
            raise Exception("Database not initialized")
        
        self.updated_at = datetime.utcnow()
        user_data = self.to_dict()
        
        if hasattr(self, '_id') and self._id:
            # Update existing user
            user_data.pop('_id')
            result = db.users.update_one(
                {"_id": self._id},
                {"$set": user_data}
            )
            return result.modified_count > 0
        else:
            # Create new user
            result = db.users.insert_one(user_data)
            self._id = result.inserted_id
            return True

    @staticmethod
    def find_by_email(email):
        db = get_db()
        if db is None:
            return None
        
        user_data = db.users.find_one({"email": email})
        if user_data:
            user = User(user_data['name'], user_data['email'])
            user._id = user_data['_id']
            user.password = user_data.get('password')
            user.google_id = user_data.get('google_id')
            user.photo_url = user_data.get('photo_url')
            user.bio = user_data.get('bio', '')
            user.skills_teach = user_data.get('skills_teach', [])
            user.skills_learn = user_data.get('skills_learn', [])
            user.availability = user_data.get('availability', '')
            user.is_public = user_data.get('is_public', True)
            user.created_at = user_data.get('created_at', datetime.utcnow())
            user.updated_at = user_data.get('updated_at', datetime.utcnow())
            user.total_sessions_taught = user_data.get('total_sessions_taught', 0)
            user.total_sessions_attended = user_data.get('total_sessions_attended', 0)
            user.rating = user_data.get('rating', 0.0)
            user.badge_level = user_data.get('badge_level', 'Bronze')
            user.notification_preferences = user_data.get('notification_preferences', {
                "email_notifications": True,
                "session_reminders": True,
                "new_requests": True
            })
            return user
        return None

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        if db is None:
            return None
        
        try:
            user_data = db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                user = User(user_data['name'], user_data['email'])
                user._id = user_data['_id']
                user.password = user_data.get('password')
                user.google_id = user_data.get('google_id')
                user.photo_url = user_data.get('photo_url')
                user.bio = user_data.get('bio', '')
                user.skills_teach = user_data.get('skills_teach', [])
                user.skills_learn = user_data.get('skills_learn', [])
                user.availability = user_data.get('availability', '')
                user.is_public = user_data.get('is_public', True)
                user.created_at = user_data.get('created_at', datetime.utcnow())
                user.updated_at = user_data.get('updated_at', datetime.utcnow())
                user.total_sessions_taught = user_data.get('total_sessions_taught', 0)
                user.total_sessions_attended = user_data.get('total_sessions_attended', 0)
                user.rating = user_data.get('rating', 0.0)
                user.badge_level = user_data.get('badge_level', 'Bronze')
                user.notification_preferences = user_data.get('notification_preferences', {
                    "email_notifications": True,
                    "session_reminders": True,
                    "new_requests": True
                })
                return user
        except:
            pass
        return None

    @staticmethod
    def find_by_google_id(google_id):
        db = get_db()
        if db is None:
            return None
        
        user_data = db.users.find_one({"google_id": google_id})
        if user_data:
            user = User(user_data['name'], user_data['email'])
            user._id = user_data['_id']
            user.password = user_data.get('password')
            user.google_id = user_data.get('google_id')
            user.photo_url = user_data.get('photo_url')
            user.bio = user_data.get('bio', '')
            user.skills_teach = user_data.get('skills_teach', [])
            user.skills_learn = user_data.get('skills_learn', [])
            user.availability = user_data.get('availability', '')
            user.is_public = user_data.get('is_public', True)
            user.created_at = user_data.get('created_at', datetime.utcnow())
            user.updated_at = user_data.get('updated_at', datetime.utcnow())
            user.total_sessions_taught = user_data.get('total_sessions_taught', 0)
            user.total_sessions_attended = user_data.get('total_sessions_attended', 0)
            user.rating = user_data.get('rating', 0.0)
            user.badge_level = user_data.get('badge_level', 'Bronze')
            user.notification_preferences = user_data.get('notification_preferences', {
                "email_notifications": True,
                "session_reminders": True,
                "new_requests": True
            })
            return user
        return None

    @staticmethod
    def get_all_public_users():
        db = get_db()
        if db is None:
            return []
        
        users = []
        for user_data in db.users.find({"is_public": True}):
            user = User(user_data['name'], user_data['email'])
            user._id = user_data['_id']
            user.password = user_data.get('password')
            user.google_id = user_data.get('google_id')
            user.photo_url = user_data.get('photo_url')
            user.bio = user_data.get('bio', '')
            user.skills_teach = user_data.get('skills_teach', [])
            user.skills_learn = user_data.get('skills_learn', [])
            user.availability = user_data.get('availability', '')
            user.is_public = user_data.get('is_public', True)
            user.created_at = user_data.get('created_at', datetime.utcnow())
            user.updated_at = user_data.get('updated_at', datetime.utcnow())
            user.total_sessions_taught = user_data.get('total_sessions_taught', 0)
            user.total_sessions_attended = user_data.get('total_sessions_attended', 0)
            user.rating = user_data.get('rating', 0.0)
            user.badge_level = user_data.get('badge_level', 'Bronze')
            user.notification_preferences = user_data.get('notification_preferences', {
                "email_notifications": True,
                "session_reminders": True,
                "new_requests": True
            })
            users.append(user)
        return users

    def update_badge_level(self):
        """Update badge level based on sessions taught"""
        if self.total_sessions_taught >= 50:
            self.badge_level = "Platinum"
        elif self.total_sessions_taught >= 25:
            self.badge_level = "Gold"
        elif self.total_sessions_taught >= 10:
            self.badge_level = "Silver"
        else:
            self.badge_level = "Bronze"

