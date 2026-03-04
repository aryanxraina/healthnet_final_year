from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from datetime import datetime
import os
from typing import Optional, List, Dict, Any
from bson import ObjectId

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "healthnet"

# MongoDB client
client: Optional[AsyncIOMotorClient] = None

async def connect_to_mongo():
    """Connect to MongoDB"""
    global client
    client = AsyncIOMotorClient(MONGODB_URL)
    print("✅ Connected to MongoDB!")
    return client

async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed!")

def get_database():
    """Get database instance"""
    if not client:
        raise Exception("MongoDB client not initialized")
    return client[DATABASE_NAME]

# Database collections
def get_users_collection():
    """Get users collection"""
    return get_database()["users"]

def get_health_assessments_collection():
    """Get health assessments collection"""
    return get_database()["health_assessments"]

def get_food_entries_collection():
    """Get food entries collection"""
    return get_database()["food_entries"]

def get_exercise_entries_collection():
    """Get exercise entries collection"""
    return get_database()["exercise_entries"]

def get_ai_recommendations_collection():
    """Get AI recommendations collection"""
    return get_database()["ai_recommendations"]

# Database indexes for better performance
async def create_indexes():
    """Create database indexes"""
    db = get_database()
    
    # Users collection indexes
    await db.users.create_index([("email", ASCENDING)], unique=True)
    await db.users.create_index([("created_at", DESCENDING)])
    
    # Health assessments indexes
    await db.health_assessments.create_index([("user_id", ASCENDING)])
    await db.health_assessments.create_index([("created_at", DESCENDING)])
    
    # Food entries indexes
    await db.food_entries.create_index([("user_id", ASCENDING)])
    await db.food_entries.create_index([("consumed_at", DESCENDING)])
    await db.food_entries.create_index([("meal_type", ASCENDING)])
    
    # Exercise entries indexes
    await db.exercise_entries.create_index([("user_id", ASCENDING)])
    await db.exercise_entries.create_index([("performed_at", DESCENDING)])
    await db.exercise_entries.create_index([("exercise_type", ASCENDING)])
    
    # AI recommendations indexes
    await db.ai_recommendations.create_index([("user_id", ASCENDING)])
    await db.ai_recommendations.create_index([("generated_at", DESCENDING)])
    await db.ai_recommendations.create_index([("priority", ASCENDING)])
    
    print("✅ Database indexes created!")

# Initialize database
async def init_database():
    """Initialize database and create indexes"""
    await connect_to_mongo()
    await create_indexes()
    print("🎉 MongoDB database initialized successfully!")

# Helper functions for ObjectId conversion
def str_to_object_id(id_str: str) -> ObjectId:
    """Convert string ID to ObjectId"""
    return ObjectId(id_str)

def object_id_to_str(obj_id: ObjectId) -> str:
    """Convert ObjectId to string"""
    return str(obj_id)

def serialize_mongo_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize MongoDB document for JSON response"""
    if doc is None:
        return None
    
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, dict):
            serialized[key] = serialize_mongo_document(value)
        elif isinstance(value, list):
            serialized[key] = [serialize_mongo_document(item) if isinstance(item, dict) else item for item in value]
        else:
            serialized[key] = value
    
    return serialized

# Data models (MongoDB documents)
class UserDocument:
    """User document structure"""
    def __init__(self, email: str, password_hash: str, name: str, age: int, 
                 gender: str, phone: Optional[str] = None, abha_id: Optional[str] = None):
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.abha_id = abha_id
        self.is_active = True
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password_hash": self.password_hash,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "abha_id": self.abha_id,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class HealthAssessmentDocument:
    """Health assessment document structure"""
    def __init__(self, user_id: str, age: int, avg_glucose_level: float, bmi: float,
                 gender: str, smoking_status: str, diabetes_risk: float = 0.0,
                 hypertension_risk: float = 0.0, overall_health_score: float = 0.0,
                 blood_pressure_systolic: Optional[int] = None,
                 blood_pressure_diastolic: Optional[int] = None,
                 heart_rate: Optional[int] = None, weight: Optional[float] = None,
                 height: Optional[float] = None):
        self.user_id = user_id
        self.age = age
        self.avg_glucose_level = avg_glucose_level
        self.bmi = bmi
        self.gender = gender
        self.smoking_status = smoking_status
        self.diabetes_risk = diabetes_risk
        self.hypertension_risk = hypertension_risk
        self.overall_health_score = overall_health_score
        self.blood_pressure_systolic = blood_pressure_systolic
        self.blood_pressure_diastolic = blood_pressure_diastolic
        self.heart_rate = heart_rate
        self.weight = weight
        self.height = height
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "age": self.age,
            "avg_glucose_level": self.avg_glucose_level,
            "bmi": self.bmi,
            "gender": self.gender,
            "smoking_status": self.smoking_status,
            "diabetes_risk": self.diabetes_risk,
            "hypertension_risk": self.hypertension_risk,
            "overall_health_score": self.overall_health_score,
            "blood_pressure_systolic": self.blood_pressure_systolic,
            "blood_pressure_diastolic": self.blood_pressure_diastolic,
            "heart_rate": self.heart_rate,
            "weight": self.weight,
            "height": self.height,
            "created_at": self.created_at
        }

class FoodEntryDocument:
    """Food entry document structure"""
    def __init__(self, user_id: str, food_name: str, calories: float,
                 protein: Optional[float] = None, carbs: Optional[float] = None,
                 fat: Optional[float] = None, meal_type: str = "snack"):
        self.user_id = user_id
        self.food_name = food_name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.meal_type = meal_type
        self.consumed_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "food_name": self.food_name,
            "calories": self.calories,
            "protein": self.protein,
            "carbs": self.carbs,
            "fat": self.fat,
            "meal_type": self.meal_type,
            "consumed_at": self.consumed_at
        }

class ExerciseEntryDocument:
    """Exercise entry document structure"""
    def __init__(self, user_id: str, exercise_name: str, duration_minutes: int,
                 calories_burned: float, exercise_type: str = "cardio"):
        self.user_id = user_id
        self.exercise_name = exercise_name
        self.duration_minutes = duration_minutes
        self.calories_burned = calories_burned
        self.exercise_type = exercise_type
        self.performed_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "exercise_name": self.exercise_name,
            "duration_minutes": self.duration_minutes,
            "calories_burned": self.calories_burned,
            "exercise_type": self.exercise_type,
            "performed_at": self.performed_at
        }

class AIRecommendationDocument:
    """AI recommendation document structure"""
    def __init__(self, user_id: str, category: str, priority: str,
                 recommendation: str, action_items: List[str]):
        self.user_id = user_id
        self.category = category
        self.priority = priority
        self.recommendation = recommendation
        self.action_items = action_items
        self.is_read = False
        self.generated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "category": self.category,
            "priority": self.priority,
            "recommendation": self.recommendation,
            "action_items": self.action_items,
            "is_read": self.is_read,
            "generated_at": self.generated_at
        }
