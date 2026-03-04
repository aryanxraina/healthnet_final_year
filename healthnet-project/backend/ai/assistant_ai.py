import numpy as np
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio

# For Hugging Face integration (will be installed via requirements.txt)
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    from sentence_transformers import SentenceTransformer
    import torch
    HUGGING_FACE_AVAILABLE = True
except ImportError:
    HUGGING_FACE_AVAILABLE = False
    print("⚠️ Hugging Face models not available. Install with: pip install transformers torch sentence-transformers")

@dataclass
class UserContext:
    """User context and health data for personalized responses"""
    user_id: str
    name: str
    age: int
    gender: str
    health_data: Dict[str, Any]
    health_risks: Dict[str, Any]
    nutrition_data: List[Dict[str, Any]]
    exercise_data: List[Dict[str, Any]]
    conversation_history: List[Dict[str, Any]]
    last_interaction: datetime
    preferences: Dict[str, Any]

class HealthNetAssistant:
    """
    AI Assistant for HealthNet that provides personalized health guidance
    based on user context and health data
    """
    
    def __init__(self):
        self.name = "HealthNet AI Assistant"
        self.version = "1.0.0"
        self.context_memory = {}  # Store user contexts
        self.conversation_memory = {}  # Store conversation history
        
        # Initialize AI models
        self.initialize_models()
        
        # Predefined response templates
        self.response_templates = {
            "greeting": [
                "Hello {name}! I'm your HealthNet AI assistant. How can I help you today?",
                "Hi {name}! I'm here to support your health journey. What would you like to know?",
                "Welcome back {name}! I've been monitoring your health data. How are you feeling today?"
            ],
            "health_concern": [
                "I understand your concern about {topic}. Based on your health data, {personalized_advice}",
                "Looking at your health profile, {personalized_advice} regarding {topic}.",
                "Given your current health status, here's what I recommend for {topic}: {personalized_advice}"
            ],
            "motivation": [
                "Great progress {name}! Your {achievement} shows real dedication to your health.",
                "I'm impressed by your {achievement}! Keep up the excellent work.",
                "Your commitment to {achievement} is inspiring! You're making great strides."
            ],
            "nutrition_advice": [
                "Based on your health goals and current data, I recommend {nutrition_advice}",
                "For your specific health profile, consider {nutrition_advice}",
                "Given your {health_condition}, here's my nutrition advice: {nutrition_advice}"
            ],
            "exercise_advice": [
                "Considering your fitness level and health data, I suggest {exercise_advice}",
                "For your current health status, try {exercise_advice}",
                "Based on your goals, here's my exercise recommendation: {exercise_advice}"
            ]
        }
    
    def initialize_models(self):
        """Initialize AI models for natural language processing"""
        try:
            if HUGGING_FACE_AVAILABLE:
                # Sentiment analysis for understanding user emotions
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    device=-1  # Use CPU
                )
                
                # Text classification for intent recognition
                self.intent_classifier = pipeline(
                    "text-classification",
                    model="facebook/bart-large-mnli",
                    device=-1
                )
                
                # Sentence embeddings for semantic similarity
                self.sentence_encoder = SentenceTransformer('all-MiniLM-L6-v2')
                
                print("✅ AI models initialized successfully")
            else:
                print("⚠️ Using fallback text processing (no Hugging Face models)")
                self.sentiment_analyzer = None
                self.intent_classifier = None
                self.sentence_encoder = None
                
        except Exception as e:
            print(f"⚠️ Error initializing AI models: {e}")
            self.sentiment_analyzer = None
            self.intent_classifier = None
            self.sentence_encoder = None
    
    async def process_user_message(self, user_id: str, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user message and generate personalized response
        """
        try:
            # Update user context
            context = self.update_user_context(user_id, user_context)
            
            # Analyze message intent and sentiment
            intent = await self.analyze_intent(message)
            sentiment = await self.analyze_sentiment(message)
            
            # Generate personalized response
            response = await self.generate_response(
                user_id, message, intent, sentiment, context
            )
            
            # Update conversation history
            self.update_conversation_history(user_id, message, response)
            
            return {
                "response": response["text"],
                "intent": intent,
                "sentiment": sentiment,
                "personalized": response["personalized"],
                "confidence": response["confidence"],
                "suggestions": response.get("suggestions", []),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again.",
                "intent": "error",
                "sentiment": "neutral",
                "personalized": False,
                "confidence": 0.0,
                "suggestions": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def update_user_context(self, user_id: str, user_data: Dict[str, Any]) -> UserContext:
        """Update and return user context"""
        # Get existing context or create new one
        if user_id in self.context_memory:
            context = self.context_memory[user_id]
            # Update with new data
            context.health_data.update(user_data.get("health_data", {}))
            context.nutrition_data.extend(user_data.get("nutrition_data", []))
            context.exercise_data.extend(user_data.get("exercise_data", []))
            context.last_interaction = datetime.now()
        else:
            # Create new context
            context = UserContext(
                user_id=user_id,
                name=user_data.get("name", "User"),
                age=user_data.get("age", 30),
                gender=user_data.get("gender", "Unknown"),
                health_data=user_data.get("health_data", {}),
                health_risks=user_data.get("health_risks", {}),
                nutrition_data=user_data.get("nutrition_data", []),
                exercise_data=user_data.get("exercise_data", []),
                conversation_history=[],
                last_interaction=datetime.now(),
                preferences=user_data.get("preferences", {})
            )
            self.context_memory[user_id] = context
        
        return context
    
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user message intent"""
        message_lower = message.lower()
        
        # Define intent patterns
        intent_patterns = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "health_concern": ["pain", "symptom", "problem", "issue", "concern", "worried", "anxious"],
            "nutrition_advice": ["diet", "food", "nutrition", "meal", "eating", "calories", "protein", "vitamins"],
            "exercise_advice": ["workout", "exercise", "fitness", "training", "cardio", "strength", "gym"],
            "progress_check": ["progress", "improvement", "results", "achievement", "goal"],
            "motivation": ["motivated", "tired", "lazy", "difficult", "hard", "struggling"],
            "general_health": ["health", "wellness", "lifestyle", "habits", "routine"],
            "medication": ["medicine", "medication", "pill", "prescription", "drug"],
            "sleep": ["sleep", "insomnia", "rest", "tired", "energy"],
            "stress": ["stress", "anxiety", "depression", "mental", "mood"],
            "goodbye": ["bye", "goodbye", "see you", "later", "thanks", "thank you"]
        }
        
        # Check for intent patterns
        detected_intents = []
        for intent, patterns in intent_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                detected_intents.append(intent)
        
        # Use AI model for intent classification if available
        if self.intent_classifier and HUGGING_FACE_AVAILABLE:
            try:
                # Define candidate labels for classification
                candidate_labels = list(intent_patterns.keys())
                result = self.intent_classifier(message, candidate_labels)
                
                # Get the most likely intent
                ai_intent = result[0]["label"]
                confidence = result[0]["score"]
                
                # Combine with pattern matching
                if ai_intent not in detected_intents:
                    detected_intents.append(ai_intent)
                    
            except Exception as e:
                print(f"AI intent analysis failed: {e}")
        
        # Return primary intent
        primary_intent = detected_intents[0] if detected_intents else "general_inquiry"
        
        return {
            "primary": primary_intent,
            "all": detected_intents,
            "confidence": 0.8 if detected_intents else 0.3
        }
    
    async def analyze_sentiment(self, message: str) -> Dict[str, Any]:
        """Analyze message sentiment"""
        if self.sentiment_analyzer and HUGGING_FACE_AVAILABLE:
            try:
                result = self.sentiment_analyzer(message)
                return {
                    "label": result[0]["label"],
                    "score": result[0]["score"],
                    "confidence": result[0]["score"]
                }
            except Exception as e:
                print(f"AI sentiment analysis failed: {e}")
        
        # Fallback sentiment analysis
        message_lower = message.lower()
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy", "excited", "motivated"]
        negative_words = ["bad", "terrible", "awful", "sad", "angry", "frustrated", "worried", "anxious"]
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.8, positive_count / len(positive_words))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.8, negative_count / len(negative_words))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "label": sentiment,
            "score": confidence,
            "confidence": confidence
        }
    
    async def generate_response(self, user_id: str, message: str, intent: Dict[str, Any], 
                              sentiment: Dict[str, Any], context: UserContext) -> Dict[str, Any]:
        """Generate personalized response based on context and intent"""
        
        primary_intent = intent["primary"]
        sentiment_label = sentiment["label"]
        
        # Get personalized health insights
        health_insights = self.get_health_insights(context)
        nutrition_insights = self.get_nutrition_insights(context)
        exercise_insights = self.get_exercise_insights(context)
        
        # Generate response based on intent
        if primary_intent == "greeting":
            response_text = self.generate_greeting_response(context, sentiment_label)
            suggestions = ["How can I help with your health today?", "Would you like to check your progress?", "Any health concerns I can address?"]
            
        elif primary_intent == "health_concern":
            response_text = self.generate_health_concern_response(message, context, health_insights)
            suggestions = ["Would you like me to analyze your health data?", "Should we review your risk factors?", "Would you like personalized recommendations?"]
            
        elif primary_intent == "nutrition_advice":
            response_text = self.generate_nutrition_response(message, context, nutrition_insights)
            suggestions = ["Would you like a personalized meal plan?", "Should we review your nutrition goals?", "Would you like food recommendations?"]
            
        elif primary_intent == "exercise_advice":
            response_text = self.generate_exercise_response(message, context, exercise_insights)
            suggestions = ["Would you like a custom workout plan?", "Should we review your fitness goals?", "Would you like exercise recommendations?"]
            
        elif primary_intent == "progress_check":
            response_text = self.generate_progress_response(context)
            suggestions = ["Would you like to see your health trends?", "Should we set new goals?", "Would you like to compare with previous data?"]
            
        elif primary_intent == "motivation":
            response_text = self.generate_motivation_response(context, sentiment_label)
            suggestions = ["Would you like to see your achievements?", "Should we set smaller, achievable goals?", "Would you like some positive reinforcement?"]
            
        elif primary_intent == "sleep":
            response_text = self.generate_sleep_response(context)
            suggestions = ["Would you like sleep hygiene tips?", "Should we analyze your sleep patterns?", "Would you like relaxation techniques?"]
            
        elif primary_intent == "stress":
            response_text = self.generate_stress_response(context, sentiment_label)
            suggestions = ["Would you like stress management techniques?", "Should we review your stress triggers?", "Would you like relaxation exercises?"]
            
        elif primary_intent == "goodbye":
            response_text = self.generate_goodbye_response(context)
            suggestions = []
            
        else:
            response_text = self.generate_general_response(message, context, health_insights)
            suggestions = ["How can I help with your health?", "Would you like to check your progress?", "Any specific health questions?"]
        
        return {
            "text": response_text,
            "personalized": True,
            "confidence": intent["confidence"],
            "suggestions": suggestions,
            "health_insights": health_insights,
            "nutrition_insights": nutrition_insights,
            "exercise_insights": exercise_insights
        }
    
    def get_health_insights(self, context: UserContext) -> Dict[str, Any]:
        """Generate health insights from user data"""
        insights = {
            "overall_health_score": 0,
            "risk_factors": [],
            "improvements": [],
            "concerns": [],
            "recommendations": []
        }
        
        health_data = context.health_data
        
        # Calculate overall health score
        if health_data:
            bmi = health_data.get("bmi", 25)
            glucose = health_data.get("avg_glucose_level", 100)
            bp_systolic = health_data.get("blood_pressure_systolic", 120)
            bp_diastolic = health_data.get("blood_pressure_diastolic", 80)
            heart_rate = health_data.get("heart_rate", 70)
            
            # Simple health scoring
            bmi_score = max(0, 100 - abs(bmi - 22) * 5)  # Optimal BMI around 22
            glucose_score = max(0, 100 - abs(glucose - 90) * 2)  # Optimal glucose around 90
            bp_score = max(0, 100 - abs(bp_systolic - 120) - abs(bp_diastolic - 80))
            hr_score = max(0, 100 - abs(heart_rate - 70))
            
            insights["overall_health_score"] = (bmi_score + glucose_score + bp_score + hr_score) / 4
            
            # Identify risk factors
            if bmi > 25:
                insights["risk_factors"].append("Elevated BMI")
            if glucose > 100:
                insights["risk_factors"].append("Elevated glucose levels")
            if bp_systolic > 130 or bp_diastolic > 85:
                insights["risk_factors"].append("Elevated blood pressure")
            if heart_rate > 100:
                insights["risk_factors"].append("Elevated heart rate")
        
        # Add health risks from context
        if context.health_risks:
            for risk_type, risk_data in context.health_risks.items():
                if risk_data.get("risk_level", "low") in ["medium", "high"]:
                    insights["concerns"].append(f"Elevated {risk_type} risk")
        
        return insights
    
    def get_nutrition_insights(self, context: UserContext) -> Dict[str, Any]:
        """Generate nutrition insights from user data"""
        insights = {
            "calorie_intake": 0,
            "nutritional_balance": "balanced",
            "recommendations": [],
            "achievements": []
        }
        
        # Analyze nutrition data
        if context.nutrition_data:
            total_calories = sum(entry.get("calories", 0) for entry in context.nutrition_data[-7:])  # Last 7 days
            insights["calorie_intake"] = total_calories / 7
            
            # Check for balanced nutrition
            protein_count = sum(1 for entry in context.nutrition_data if "protein" in entry.get("food_name", "").lower())
            if protein_count > len(context.nutrition_data) * 0.3:
                insights["achievements"].append("Good protein intake")
            
            if insights["calorie_intake"] < 1500:
                insights["recommendations"].append("Consider increasing calorie intake")
            elif insights["calorie_intake"] > 2500:
                insights["recommendations"].append("Consider reducing calorie intake")
        
        return insights
    
    def get_exercise_insights(self, context: UserContext) -> Dict[str, Any]:
        """Generate exercise insights from user data"""
        insights = {
            "weekly_activity": 0,
            "fitness_level": "beginner",
            "recommendations": [],
            "achievements": []
        }
        
        # Analyze exercise data
        if context.exercise_data:
            weekly_minutes = sum(entry.get("duration", 0) for entry in context.exercise_data[-7:])
            insights["weekly_activity"] = weekly_minutes
            
            if weekly_minutes >= 150:
                insights["achievements"].append("Meeting weekly exercise guidelines")
                insights["fitness_level"] = "active"
            elif weekly_minutes >= 75:
                insights["fitness_level"] = "moderate"
            else:
                insights["recommendations"].append("Aim for at least 150 minutes of exercise per week")
        
        return insights
    
    def generate_greeting_response(self, context: UserContext, sentiment: str) -> str:
        """Generate personalized greeting response"""
        name = context.name
        time_of_day = self.get_time_of_day()
        
        if sentiment == "positive":
            return f"Hello {name}! I'm so glad to see you in such good spirits! How can I support your health journey today?"
        elif sentiment == "negative":
            return f"Hi {name}. I sense you might be having a tough day. I'm here to help - what's on your mind regarding your health?"
        else:
            return f"Hello {name}! I'm your HealthNet AI assistant. How can I help you with your health today?"
    
    def generate_health_concern_response(self, message: str, context: UserContext, health_insights: Dict[str, Any]) -> str:
        """Generate response for health concerns"""
        concerns = health_insights.get("concerns", [])
        recommendations = health_insights.get("recommendations", [])
        
        if concerns:
            concern_text = ", ".join(concerns[:2])  # Limit to 2 concerns
            return f"I understand your concern. Based on your health data, I've identified: {concern_text}. Let me provide some personalized recommendations to address these."
        else:
            return "I understand your health concern. While your current health metrics look good, it's always important to address any symptoms. Could you tell me more about what you're experiencing?"
    
    def generate_nutrition_response(self, message: str, context: UserContext, nutrition_insights: Dict[str, Any]) -> str:
        """Generate response for nutrition questions"""
        calorie_intake = nutrition_insights.get("calorie_intake", 0)
        achievements = nutrition_insights.get("achievements", [])
        
        if achievements:
            achievement_text = ", ".join(achievements)
            return f"Great news! I can see you're making progress with your nutrition: {achievement_text}. Your current daily calorie intake is around {calorie_intake:.0f} calories. Would you like personalized meal recommendations?"
        else:
            return f"Based on your health profile, I can help you with nutrition advice. Your current daily calorie intake is around {calorie_intake:.0f} calories. What specific nutrition guidance are you looking for?"
    
    def generate_exercise_response(self, message: str, context: UserContext, exercise_insights: Dict[str, Any]) -> str:
        """Generate response for exercise questions"""
        weekly_activity = exercise_insights.get("weekly_activity", 0)
        fitness_level = exercise_insights.get("fitness_level", "beginner")
        
        if weekly_activity >= 150:
            return f"Excellent! You're already meeting the recommended 150 minutes of weekly exercise with {weekly_activity} minutes. As a {fitness_level} level, you're doing great! What type of exercise guidance do you need?"
        else:
            return f"I can see you're currently getting {weekly_activity} minutes of exercise per week. As a {fitness_level}, I'd recommend aiming for 150 minutes weekly. What specific exercise advice are you looking for?"
    
    def generate_progress_response(self, context: UserContext) -> str:
        """Generate response for progress inquiries"""
        health_insights = self.get_health_insights(context)
        health_score = health_insights.get("overall_health_score", 0)
        
        if health_score > 80:
            return f"Fantastic progress! Your overall health score is {health_score:.0f}/100, which is excellent! You're clearly making great choices for your health."
        elif health_score > 60:
            return f"Good progress! Your overall health score is {health_score:.0f}/100. You're on the right track, and there's room for continued improvement."
        else:
            return f"Your current health score is {health_score:.0f}/100. This gives us a great baseline to work from! Let's focus on areas where we can make improvements."
    
    def generate_motivation_response(self, context: UserContext, sentiment: str) -> str:
        """Generate motivational response"""
        name = context.name
        
        if sentiment == "negative":
            return f"I understand it can be challenging, {name}. Remember, every small step counts toward your health goals. You don't have to be perfect - just consistent. What's one small thing you can do today to feel better?"
        else:
            return f"That's the spirit, {name}! Your dedication to your health is inspiring. Keep up the great work, and remember that progress, not perfection, is the goal."
    
    def generate_sleep_response(self, context: UserContext) -> str:
        """Generate response for sleep-related questions"""
        return "Sleep is crucial for your health! Based on your profile, I can help you with sleep hygiene tips, relaxation techniques, or analyzing your sleep patterns. What specific sleep support do you need?"
    
    def generate_stress_response(self, context: UserContext, sentiment: str) -> str:
        """Generate response for stress-related questions"""
        if sentiment == "negative":
            return "I can sense you're feeling stressed. This is completely normal, and I'm here to help. Would you like some stress management techniques, breathing exercises, or just someone to talk to about what's on your mind?"
        else:
            return "Managing stress is an important part of overall health. I can help you with stress management techniques, mindfulness practices, or lifestyle adjustments. What would be most helpful for you?"
    
    def generate_goodbye_response(self, context: UserContext) -> str:
        """Generate goodbye response"""
        name = context.name
        return f"Take care, {name}! Remember, I'm here whenever you need health support. Keep up the great work on your health journey!"
    
    def generate_general_response(self, message: str, context: UserContext, health_insights: Dict[str, Any]) -> str:
        """Generate general response for other inquiries"""
        health_score = health_insights.get("overall_health_score", 0)
        
        if health_score > 80:
            return "Your health is looking great! I'm here to help you maintain and improve your wellness. What would you like to know more about?"
        else:
            return "I'm here to support your health journey! I can help with nutrition advice, exercise recommendations, health monitoring, or any other health-related questions. What's on your mind?"
    
    def get_time_of_day(self) -> str:
        """Get current time of day"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def update_conversation_history(self, user_id: str, user_message: str, assistant_response: Dict[str, Any]):
        """Update conversation history"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "assistant_response": assistant_response["text"],
            "intent": assistant_response.get("intent", "unknown"),
            "sentiment": assistant_response.get("sentiment", "neutral")
        })
        
        # Keep only last 50 conversations
        if len(self.conversation_memory[user_id]) > 50:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-50:]
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        if user_id in self.conversation_memory:
            return self.conversation_memory[user_id][-limit:]
        return []
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user insights"""
        if user_id not in self.context_memory:
            return {}
        
        context = self.context_memory[user_id]
        health_insights = self.get_health_insights(context)
        nutrition_insights = self.get_nutrition_insights(context)
        exercise_insights = self.get_exercise_insights(context)
        conversation_history = self.get_conversation_history(user_id)
        
        return {
            "user_profile": {
                "name": context.name,
                "age": context.age,
                "gender": context.gender,
                "last_interaction": context.last_interaction.isoformat()
            },
            "health_insights": health_insights,
            "nutrition_insights": nutrition_insights,
            "exercise_insights": exercise_insights,
            "conversation_summary": {
                "total_conversations": len(conversation_history),
                "common_intents": self.get_common_intents(conversation_history),
                "sentiment_trend": self.get_sentiment_trend(conversation_history)
            }
        }
    
    def get_common_intents(self, conversation_history: List[Dict[str, Any]]) -> List[str]:
        """Get most common conversation intents"""
        intents = [conv.get("intent", "unknown") for conv in conversation_history]
        intent_counts = {}
        for intent in intents:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        # Return top 3 most common intents
        sorted_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)
        return [intent for intent, count in sorted_intents[:3]]
    
    def get_sentiment_trend(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Get sentiment trend from conversation history"""
        if not conversation_history:
            return "neutral"
        
        recent_sentiments = [conv.get("sentiment", "neutral") for conv in conversation_history[-10:]]
        positive_count = recent_sentiments.count("positive")
        negative_count = recent_sentiments.count("negative")
        
        if positive_count > negative_count:
            return "improving"
        elif negative_count > positive_count:
            return "declining"
        else:
            return "stable"

# Global instance
healthnet_assistant = HealthNetAssistant()
