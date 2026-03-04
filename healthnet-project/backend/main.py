from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
# Import database and auth
from database import (
    get_users_collection, get_health_assessments_collection, 
    get_food_entries_collection, get_exercise_entries_collection,
    get_ai_recommendations_collection, UserDocument, HealthAssessmentDocument,
    FoodEntryDocument, ExerciseEntryDocument, AIRecommendationDocument,
    init_database, close_mongo_connection, serialize_mongo_document
)
from auth import get_password_hash, verify_password, create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Import AI systems
from ai.health_models import health_models
from ai.nutrition_ai import nutrition_ai
from ai.exercise_ai import exercise_ai
from ai.assistant_ai import healthnet_assistant

# Initialize FastAPI app
app = FastAPI(
    title="HealthNet API",
    description="AI-Powered Preventive Healthcare API",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500", 
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models for request/response
class UserRegistration(BaseModel):
    email: str
    password: str
    name: str
    age: int
    gender: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class HealthData(BaseModel):
    age: int
    avg_glucose_level: float
    bmi: float
    gender: str
    smoking_status: str
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None

class FoodEntry(BaseModel):
    food_name: str
    calories: float
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    meal_type: str  # breakfast, lunch, dinner, snack
    timestamp: Optional[datetime] = None

class ExerciseEntry(BaseModel):
    exercise_name: str
    duration_minutes: int
    calories_burned: float
    exercise_type: str  # cardio, strength, flexibility
    timestamp: Optional[datetime] = None

# Authentication helper
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    users_collection = get_users_collection()
    user = await users_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# Health risk prediction
def predict_health_risks(health_data: HealthData) -> Dict[str, Any]:
    """Predict health risks using trained AI models"""
    try:
        # Prepare data for prediction
        user_data = {
            'age': health_data.age,
            'avg_glucose_level': health_data.avg_glucose_level,
            'bmi': health_data.bmi,
            'gender': health_data.gender,
            'smoking_status': health_data.smoking_status
        }
        
        # Load models (you'll need to train them first)
        models_path = Path(__file__).parent / "models"
        
        # For now, return mock predictions
        # In production, load and use actual trained models
        diabetes_risk = min(0.8, max(0.1, (health_data.avg_glucose_level - 70) / 100))
        hypertension_risk = min(0.9, max(0.1, (health_data.blood_pressure_systolic - 90) / 50)) if health_data.blood_pressure_systolic else 0.3
        
        return {
            "diabetes_risk": round(diabetes_risk, 3),
            "hypertension_risk": round(hypertension_risk, 3),
            "overall_health_score": round(100 - (diabetes_risk + hypertension_risk) * 50, 1),
            "recommendations": [
                "Monitor blood glucose levels regularly",
                "Maintain a balanced diet",
                "Exercise regularly",
                "Reduce salt intake" if hypertension_risk > 0.5 else "Maintain current lifestyle"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongo_connection()

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "HealthNet API is running!", "status": "healthy"}

@app.post("/api/auth/register")
async def register_user(user: UserRegistration):
    """Register a new user"""
    users_collection = get_users_collection()
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    user_doc = UserDocument(
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        age=user.age,
        gender=user.gender,
        phone=user.phone
    )
    
    result = await users_collection.insert_one(user_doc.to_dict())
    
    return {"message": "User registered successfully", "email": user.email}

@app.post("/api/auth/login")
async def login_user(user: UserLogin):
    """Login user and return access token"""
    users_collection = get_users_collection()
    
    # Find user in database
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["email"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": db_user["email"],
            "name": db_user["name"]
        }
    }

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "user": {
            "email": current_user["email"],
            "name": current_user["name"],
            "age": current_user["age"],
            "gender": current_user["gender"]
        }
    }

@app.post("/api/auth/logout")
async def logout_user(current_user: dict = Depends(get_current_user)):
    """Logout user"""
    # For JWT tokens, we don't need to maintain a session database
    # The token will be invalidated by the frontend removing it
    return {"message": "Logged out successfully"}

@app.post("/api/health/assessment")
async def health_assessment(
    health_data: HealthData,
    current_user: dict = Depends(get_current_user)
):
    """Submit health data and get AI-powered risk assessment"""
    # Store health data in MongoDB
    health_assessments_collection = get_health_assessments_collection()
    
    # Create health assessment document
    assessment_doc = HealthAssessmentDocument(
        user_id=current_user["email"],  # Using email as user_id for now
        age=health_data.age,
        avg_glucose_level=health_data.avg_glucose_level,
        bmi=health_data.bmi,
        gender=health_data.gender,
        smoking_status=health_data.smoking_status,
        blood_pressure_systolic=health_data.blood_pressure_systolic,
        blood_pressure_diastolic=health_data.blood_pressure_diastolic,
        heart_rate=health_data.heart_rate,
        weight=health_data.weight,
        height=health_data.height
    )
    
    # Insert into database
    result = await health_assessments_collection.insert_one(assessment_doc.to_dict())
    
    # Get AI predictions
    health_data_dict = {
        "age": health_data.age,
        "avg_glucose_level": health_data.avg_glucose_level,
        "bmi": health_data.bmi,
        "gender": health_data.gender,
        "smoking_status": health_data.smoking_status,
        "blood_pressure_systolic": health_data.blood_pressure_systolic,
        "blood_pressure_diastolic": health_data.blood_pressure_diastolic,
        "heart_rate": health_data.heart_rate,
        "weight": health_data.weight,
        "height": health_data.height
    }
    predictions = health_models.predict_health_risks(health_data_dict)
    
    return {
        "message": "Health assessment completed",
        "predictions": predictions,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health/dashboard")
async def get_health_dashboard(current_user: dict = Depends(get_current_user)):
    """Get comprehensive health dashboard data"""
    health_assessments_collection = get_health_assessments_collection()
    
    # Get latest health data from MongoDB
    latest_assessment = await health_assessments_collection.find_one(
        {"user_id": current_user["email"]},
        sort=[("created_at", -1)]
    )
    
    if not latest_assessment:
        # Return default data if no health assessment found
        return {
            "user_info": {
                "name": current_user["name"],
                "email": current_user["email"],
                "age": current_user["age"],
                "gender": current_user["gender"]
            },
            "latest_health_data": None,
            "predictions": {
                "diabetes_risk": 0.3,
                "hypertension_risk": 0.3,
                "overall_health_score": 70.0,
                "recommendations": ["Complete your health assessment to get personalized insights"]
            },
            "trends": {
                "heart_rate": {"current": 72, "trend": "stable", "history": [70, 72, 71, 73, 72]},
                "blood_glucose": {"current": 98, "trend": "decreasing", "history": [105, 102, 100, 99, 98]},
                "blood_pressure": {"current": "120/80", "trend": "stable", "history": ["118/78", "120/80", "119/79", "121/81", "120/80"]},
                "activity": {"current": 7245, "trend": "increasing", "history": [6500, 6800, 7000, 7100, 7245]}
            },
            "last_updated": datetime.now().isoformat()
        }
    
    # Convert MongoDB document to dict for AI analysis
    health_data = {
        "age": latest_assessment["age"],
        "avg_glucose_level": latest_assessment["avg_glucose_level"],
        "bmi": latest_assessment["bmi"],
        "gender": latest_assessment["gender"],
        "smoking_status": latest_assessment["smoking_status"],
        "blood_pressure_systolic": latest_assessment.get("blood_pressure_systolic"),
        "blood_pressure_diastolic": latest_assessment.get("blood_pressure_diastolic"),
        "heart_rate": latest_assessment.get("heart_rate"),
        "weight": latest_assessment.get("weight"),
        "height": latest_assessment.get("height")
    }
    
    # Get AI predictions
    predictions = health_models.predict_health_risks(health_data)
    
    # Get health trends from AI
    health_history = await health_assessments_collection.find(
        {"user_id": current_user["email"]}
    ).sort("created_at", -1).limit(5).to_list(length=5)
    
    trends = health_models.analyze_health_trends(health_history)
    
    return {
        "user_info": {
            "name": current_user["name"],
            "email": current_user["email"],
            "age": current_user["age"],
            "gender": current_user["gender"]
        },
        "latest_health_data": serialize_mongo_document(latest_assessment) if latest_assessment else None,
        "predictions": predictions,
        "trends": trends,
        "last_updated": datetime.now().isoformat()
    }

@app.post("/api/nutrition/food")
async def add_food_entry(
    food: FoodEntry,
    current_user: dict = Depends(get_current_user)
):
    """Add food entry to nutrition tracker"""
    food_entries_collection = get_food_entries_collection()
    
    # Create food entry document
    food_doc = FoodEntryDocument(
        user_id=current_user["email"],  # Using email as user_id for now
        food_name=food.food_name,
        calories=food.calories,
        protein=food.protein,
        carbs=food.carbs,
        fat=food.fat,
        meal_type=food.meal_type
    )
    
    # Insert into database
    result = await food_entries_collection.insert_one(food_doc.to_dict())
    
    return {
        "message": "Food entry added successfully",
        "entry": food_doc.to_dict()
    }

@app.get("/api/nutrition/food")
async def get_food_entries(
    current_user: dict = Depends(get_current_user),
    date: Optional[str] = None
):
    """Get food entries for a user"""
    food_entries_collection = get_food_entries_collection()
    
    # Build query
    query = {"user_id": current_user["email"]}
    
    # Get entries from database
    cursor = food_entries_collection.find(query).sort("created_at", -1)
    entries = await cursor.to_list(length=100)  # Limit to 100 entries
    
    if date:
        # Filter by date
        target_date = datetime.fromisoformat(date).date()
        entries = [
            entry for entry in entries 
            if entry.get("created_at") and entry["created_at"].date() == target_date
        ]
    
    return {"entries": [serialize_mongo_document(entry) for entry in entries]}

@app.post("/api/exercise")
async def add_exercise_entry(
    exercise: ExerciseEntry,
    current_user: dict = Depends(get_current_user)
):
    """Add exercise entry"""
    exercise_entries_collection = get_exercise_entries_collection()
    
    # Create exercise entry document
    exercise_doc = ExerciseEntryDocument(
        user_id=current_user["email"],  # Using email as user_id for now
        exercise_name=exercise.exercise_name,
        duration_minutes=exercise.duration_minutes,
        calories_burned=exercise.calories_burned,
        exercise_type=exercise.exercise_type
    )
    
    # Insert into database
    result = await exercise_entries_collection.insert_one(exercise_doc.to_dict())
    
    return {
        "message": "Exercise entry added successfully",
        "entry": exercise_doc.to_dict()
    }

@app.get("/api/exercise")
async def get_exercise_entries(
    current_user: dict = Depends(get_current_user),
    date: Optional[str] = None
):
    """Get exercise entries for a user"""
    exercise_entries_collection = get_exercise_entries_collection()
    
    # Build query
    query = {"user_id": current_user["email"]}
    
    # Get entries from database
    cursor = exercise_entries_collection.find(query).sort("created_at", -1)
    entries = await cursor.to_list(length=100)  # Limit to 100 entries
    
    if date:
        # Filter by date
        target_date = datetime.fromisoformat(date).date()
        entries = [
            entry for entry in entries 
            if entry.get("created_at") and entry["created_at"].date() == target_date
        ]
    
    return {"entries": [serialize_mongo_document(entry) for entry in entries]}

@app.get("/api/nutrition/summary")
async def get_nutrition_summary(
    current_user: dict = Depends(get_current_user),
    date: Optional[str] = None
):
    """Get nutrition summary for a user"""
    food_entries_collection = get_food_entries_collection()
    
    # Build query
    query = {"user_id": current_user["email"]}
    
    # Get entries from database
    cursor = food_entries_collection.find(query).sort("created_at", -1)
    entries = await cursor.to_list(length=100)  # Limit to 100 entries
    
    if date:
        target_date = datetime.fromisoformat(date).date()
        entries = [
            entry for entry in entries 
            if entry.get("created_at") and entry["created_at"].date() == target_date
        ]
    
    summary = {
        "total_calories": sum(entry.get("calories", 0) for entry in entries),
        "total_protein": sum(entry.get("protein", 0) for entry in entries),
        "total_carbs": sum(entry.get("carbs", 0) for entry in entries),
        "total_fat": sum(entry.get("fat", 0) for entry in entries),
        "entries_count": len(entries)
    }
    
    return summary

@app.get("/api/ai/recommendations")
async def get_ai_recommendations(current_user: dict = Depends(get_current_user)):
    """Get AI-powered health recommendations"""
    health_assessments_collection = get_health_assessments_collection()
    
    # Get latest health data from MongoDB
    latest_assessment = await health_assessments_collection.find_one(
        {"user_id": current_user["email"]},
        sort=[("created_at", -1)]
    )
    
    if not latest_assessment:
        # Return default recommendations if no health data
        return {
            "recommendations": [
                {
                    "category": "Health Assessment",
                    "priority": "high",
                    "recommendation": "Complete your health assessment to get personalized recommendations",
                    "action_items": ["Fill out the health questionnaire", "Upload medical reports", "Schedule a checkup"]
                }
            ],
            "health_score": 70.0,
            "generated_at": datetime.now().isoformat()
        }
    
    # Convert MongoDB document to dict for AI analysis
    health_data = {
        "age": latest_assessment["age"],
        "avg_glucose_level": latest_assessment["avg_glucose_level"],
        "bmi": latest_assessment["bmi"],
        "gender": latest_assessment["gender"],
        "smoking_status": latest_assessment["smoking_status"],
        "blood_pressure_systolic": latest_assessment.get("blood_pressure_systolic"),
        "blood_pressure_diastolic": latest_assessment.get("blood_pressure_diastolic"),
        "heart_rate": latest_assessment.get("heart_rate"),
        "weight": latest_assessment.get("weight"),
        "height": latest_assessment.get("height")
    }
    
    # Get AI predictions and recommendations
    predictions = health_models.predict_health_risks(health_data)
    recommendations = health_models.generate_personalized_recommendations(health_data, predictions)
    
    return {
        "recommendations": recommendations,
        "health_score": predictions.get("overall_health_score", 0),
        "predictions": {
            "diabetes_risk": predictions.get("diabetes_risk", 0),
            "hypertension_risk": predictions.get("hypertension_risk", 0),
            "heart_disease_risk": predictions.get("heart_disease_risk", 0)
        },
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/ai/nutrition-plan")
async def get_ai_nutrition_plan(current_user: dict = Depends(get_current_user)):
    """Get AI-powered personalized nutrition plan"""
    health_assessments_collection = get_health_assessments_collection()
    
    # Get latest health data from MongoDB
    latest_assessment = await health_assessments_collection.find_one(
        {"user_id": current_user["email"]},
        sort=[("created_at", -1)]
    )
    
    if not latest_assessment:
        return {
            "error": "No health assessment data found. Please complete the health questionnaire first."
        }
    
    # Convert MongoDB document to dict for AI analysis
    health_data = {
        "age": latest_assessment["age"],
        "avg_glucose_level": latest_assessment["avg_glucose_level"],
        "bmi": latest_assessment["bmi"],
        "gender": latest_assessment["gender"],
        "smoking_status": latest_assessment["smoking_status"],
        "blood_pressure_systolic": latest_assessment.get("blood_pressure_systolic"),
        "blood_pressure_diastolic": latest_assessment.get("blood_pressure_diastolic"),
        "heart_rate": latest_assessment.get("heart_rate"),
        "weight": latest_assessment.get("weight"),
        "height": latest_assessment.get("height")
    }
    
    # Get AI predictions
    predictions = health_models.predict_health_risks(health_data)
    
    # Calculate daily calorie needs
    daily_calories = nutrition_ai.calculate_daily_calories(health_data)
    
    # Generate personalized meal plan
    meal_plan = nutrition_ai.generate_meal_plan(health_data, predictions, daily_calories)
    
    return {
        "daily_calories": daily_calories,
        "meal_plan": meal_plan,
        "health_data": health_data,
        "predictions": predictions,
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/ai/exercise-plan")
async def get_ai_exercise_plan(current_user: dict = Depends(get_current_user)):
    """Get AI-powered personalized exercise plan"""
    health_assessments_collection = get_health_assessments_collection()
    
    # Get latest health data from MongoDB
    latest_assessment = await health_assessments_collection.find_one(
        {"user_id": current_user["email"]},
        sort=[("created_at", -1)]
    )
    
    if not latest_assessment:
        return {
            "error": "No health assessment data found. Please complete the health questionnaire first."
        }
    
    # Convert MongoDB document to dict for AI analysis
    health_data = {
        "age": latest_assessment["age"],
        "avg_glucose_level": latest_assessment["avg_glucose_level"],
        "bmi": latest_assessment["bmi"],
        "gender": latest_assessment["gender"],
        "smoking_status": latest_assessment["smoking_status"],
        "blood_pressure_systolic": latest_assessment.get("blood_pressure_systolic"),
        "blood_pressure_diastolic": latest_assessment.get("blood_pressure_diastolic"),
        "heart_rate": latest_assessment.get("heart_rate"),
        "weight": latest_assessment.get("weight"),
        "height": latest_assessment.get("height")
    }
    
    # Get AI predictions
    predictions = health_models.predict_health_risks(health_data)
    
    # Generate personalized workout plan
    workout_plan = exercise_ai.generate_weekly_workout_plan(health_data, predictions)
    
    return {
        "workout_plan": workout_plan,
        "health_data": health_data,
        "predictions": predictions,
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/ai/health-analysis")
async def get_ai_health_analysis(current_user: dict = Depends(get_current_user)):
    """Get comprehensive AI health analysis"""
    health_assessments_collection = get_health_assessments_collection()
    
    # Get latest health data from MongoDB
    latest_assessment = await health_assessments_collection.find_one(
        {"user_id": current_user["email"]},
        sort=[("created_at", -1)]
    )
    
    if not latest_assessment:
        return {
            "error": "No health assessment data found. Please complete the health questionnaire first."
        }
    
    # Convert MongoDB document to dict for AI analysis
    health_data = {
        "age": latest_assessment["age"],
        "avg_glucose_level": latest_assessment["avg_glucose_level"],
        "bmi": latest_assessment["bmi"],
        "gender": latest_assessment["gender"],
        "smoking_status": latest_assessment["smoking_status"],
        "blood_pressure_systolic": latest_assessment.get("blood_pressure_systolic"),
        "blood_pressure_diastolic": latest_assessment.get("blood_pressure_diastolic"),
        "heart_rate": latest_assessment.get("heart_rate"),
        "weight": latest_assessment.get("weight"),
        "height": latest_assessment.get("height")
    }
    
    # Get comprehensive AI analysis
    predictions = health_models.predict_health_risks(health_data)
    recommendations = health_models.generate_personalized_recommendations(health_data, predictions)
    
    # Get nutrition analysis
    daily_calories = nutrition_ai.calculate_daily_calories(health_data)
    nutrition_goals = nutrition_ai.get_nutritional_goals(health_data, predictions)
    
    # Get exercise analysis
    fitness_score = exercise_ai.calculate_fitness_score(health_data, predictions)
    fitness_level = exercise_ai.determine_fitness_level(fitness_score)
    
    return {
        "health_summary": {
            "overall_health_score": predictions.get("overall_health_score", 0),
            "fitness_score": fitness_score,
            "fitness_level": fitness_level,
            "daily_calories_needed": daily_calories
        },
        "risk_assessment": {
            "diabetes_risk": predictions.get("diabetes_risk", 0),
            "hypertension_risk": predictions.get("hypertension_risk", 0),
            "heart_disease_risk": predictions.get("heart_disease_risk", 0)
        },
        "recommendations": recommendations,
        "nutrition_goals": nutrition_goals,
        "health_data": health_data,
        "generated_at": datetime.now().isoformat()
    }

# AI Assistant Endpoints
class AssistantMessage(BaseModel):
    message: str

class AssistantResponse(BaseModel):
    response: str
    intent: Dict[str, Any]
    sentiment: Dict[str, Any]
    personalized: bool
    confidence: float
    suggestions: List[str]
    timestamp: str

@app.post("/api/ai/assistant/chat", response_model=AssistantResponse)
async def chat_with_assistant(
    message_data: AssistantMessage,
    current_user: dict = Depends(get_current_user)
):
    """Chat with the AI assistant for personalized health guidance"""
    try:
        # Get user context from database
        health_assessments_collection = get_health_assessments_collection()
        food_entries_collection = get_food_entries_collection()
        exercise_entries_collection = get_exercise_entries_collection()
        
        # Get latest health assessment
        latest_assessment = await health_assessments_collection.find_one(
            {"user_id": current_user["email"]},
            sort=[("created_at", -1)]
        )
        
        # Get recent food entries (last 7 days)
        food_entries = await food_entries_collection.find(
            {"user_id": current_user["email"]},
            sort=[("timestamp", -1)]
        ).limit(7).to_list(length=7)
        
        # Get recent exercise entries (last 7 days)
        exercise_entries = await exercise_entries_collection.find(
            {"user_id": current_user["email"]},
            sort=[("timestamp", -1)]
        ).limit(7).to_list(length=7)
        
        # Prepare user context
        user_context = {
            "name": current_user.get("name", "User"),
            "age": current_user.get("age", 30),
            "gender": current_user.get("gender", "Unknown"),
            "health_data": latest_assessment if latest_assessment else {},
            "health_risks": {},  # Will be populated by AI assistant
            "nutrition_data": food_entries,
            "exercise_data": exercise_entries,
            "preferences": {}
        }
        
        # Process message with AI assistant
        response = await healthnet_assistant.process_user_message(
            user_id=current_user["email"],
            message=message_data.message,
            user_context=user_context
        )
        
        return AssistantResponse(**response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )

@app.get("/api/ai/assistant/insights")
async def get_assistant_insights(current_user: dict = Depends(get_current_user)):
    """Get comprehensive user insights from the AI assistant"""
    try:
        insights = healthnet_assistant.get_user_insights(current_user["email"])
        return insights
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting insights: {str(e)}"
        )

@app.get("/api/ai/assistant/conversation-history")
async def get_conversation_history(
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get conversation history with the AI assistant"""
    try:
        history = healthnet_assistant.get_conversation_history(
            user_id=current_user["email"],
            limit=limit
        )
        return {"conversation_history": history}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting conversation history: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
