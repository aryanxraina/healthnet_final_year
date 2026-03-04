import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import math

class HealthRiskModels:
    """AI-powered health risk assessment and recommendation system"""
    
    def __init__(self):
        self.risk_thresholds = {
            'diabetes': 0.6,
            'hypertension': 0.6,
            'heart_disease': 0.5,
            'obesity': 0.7,
            'stroke': 0.4
        }
        
        # Health score weights
        self.health_weights = {
            'bmi': 0.2,
            'glucose': 0.25,
            'blood_pressure': 0.2,
            'heart_rate': 0.15,
            'age': 0.1,
            'smoking': 0.1
        }
    
    def calculate_bmi_score(self, bmi: float) -> float:
        """Calculate BMI health score (0-100)"""
        if bmi < 18.5:  # Underweight
            return max(60, 100 - (18.5 - bmi) * 10)
        elif 18.5 <= bmi < 25:  # Normal
            return 100
        elif 25 <= bmi < 30:  # Overweight
            return max(70, 100 - (bmi - 25) * 6)
        else:  # Obese
            return max(40, 100 - (bmi - 30) * 8)
    
    def calculate_glucose_score(self, glucose: float) -> float:
        """Calculate glucose health score (0-100)"""
        if glucose < 70:  # Low
            return max(60, 100 - (70 - glucose) * 5)
        elif 70 <= glucose <= 140:  # Normal
            return 100
        elif 140 < glucose <= 200:  # Pre-diabetic
            return max(50, 100 - (glucose - 140) * 0.8)
        else:  # Diabetic
            return max(20, 100 - (glucose - 200) * 0.6)
    
    def calculate_blood_pressure_score(self, systolic: Optional[int], diastolic: Optional[int]) -> float:
        """Calculate blood pressure health score (0-100)"""
        if not systolic or not diastolic:
            return 70  # Default score if data missing
        
        if systolic < 90 or diastolic < 60:  # Low
            return 80
        elif 90 <= systolic <= 120 and 60 <= diastolic <= 80:  # Normal
            return 100
        elif 120 < systolic <= 140 or 80 < diastolic <= 90:  # Pre-hypertension
            return 80
        elif 140 < systolic <= 160 or 90 < diastolic <= 100:  # Stage 1 hypertension
            return 60
        else:  # Stage 2 hypertension
            return 40
    
    def calculate_heart_rate_score(self, heart_rate: Optional[int]) -> float:
        """Calculate heart rate health score (0-100)"""
        if not heart_rate:
            return 70  # Default score if data missing
        
        if 60 <= heart_rate <= 100:  # Normal
            return 100
        elif 50 <= heart_rate < 60 or 100 < heart_rate <= 110:  # Borderline
            return 80
        else:  # Abnormal
            return 60
    
    def predict_diabetes_risk(self, health_data: Dict[str, Any]) -> float:
        """Predict diabetes risk (0-1)"""
        risk_score = 0.0
        
        # Age factor
        age = health_data.get('age', 30)
        if age > 45:
            risk_score += 0.2
        elif age > 35:
            risk_score += 0.1
        
        # BMI factor
        bmi = health_data.get('bmi', 25)
        if bmi > 30:
            risk_score += 0.3
        elif bmi > 25:
            risk_score += 0.15
        
        # Glucose factor
        glucose = health_data.get('avg_glucose_level', 100)
        if glucose > 140:
            risk_score += 0.4
        elif glucose > 126:
            risk_score += 0.25
        
        # Blood pressure factor
        systolic = health_data.get('blood_pressure_systolic')
        diastolic = health_data.get('blood_pressure_diastolic')
        if systolic and diastolic:
            if systolic > 140 or diastolic > 90:
                risk_score += 0.2
        
        # Smoking factor
        if health_data.get('smoking_status') == 'yes':
            risk_score += 0.1
        
        return min(1.0, risk_score)
    
    def predict_hypertension_risk(self, health_data: Dict[str, Any]) -> float:
        """Predict hypertension risk (0-1)"""
        risk_score = 0.0
        
        # Age factor
        age = health_data.get('age', 30)
        if age > 50:
            risk_score += 0.3
        elif age > 40:
            risk_score += 0.2
        
        # BMI factor
        bmi = health_data.get('bmi', 25)
        if bmi > 30:
            risk_score += 0.25
        elif bmi > 25:
            risk_score += 0.15
        
        # Current blood pressure
        systolic = health_data.get('blood_pressure_systolic')
        diastolic = health_data.get('blood_pressure_diastolic')
        if systolic and diastolic:
            if systolic > 140 or diastolic > 90:
                risk_score += 0.4
            elif systolic > 120 or diastolic > 80:
                risk_score += 0.2
        
        # Smoking factor
        if health_data.get('smoking_status') == 'yes':
            risk_score += 0.15
        
        return min(1.0, risk_score)
    
    def predict_heart_disease_risk(self, health_data: Dict[str, Any]) -> float:
        """Predict heart disease risk (0-1)"""
        risk_score = 0.0
        
        # Age factor
        age = health_data.get('age', 30)
        if age > 55:
            risk_score += 0.3
        elif age > 45:
            risk_score += 0.2
        
        # BMI factor
        bmi = health_data.get('bmi', 25)
        if bmi > 30:
            risk_score += 0.2
        elif bmi > 25:
            risk_score += 0.1
        
        # Blood pressure factor
        systolic = health_data.get('blood_pressure_systolic')
        diastolic = health_data.get('blood_pressure_diastolic')
        if systolic and diastolic:
            if systolic > 140 or diastolic > 90:
                risk_score += 0.25
        
        # Smoking factor
        if health_data.get('smoking_status') == 'yes':
            risk_score += 0.3
        
        # Heart rate factor
        heart_rate = health_data.get('heart_rate')
        if heart_rate and (heart_rate > 100 or heart_rate < 60):
            risk_score += 0.15
        
        return min(1.0, risk_score)
    
    def calculate_overall_health_score(self, health_data: Dict[str, Any]) -> float:
        """Calculate overall health score (0-100)"""
        scores = {}
        
        # Calculate individual component scores
        scores['bmi'] = self.calculate_bmi_score(health_data.get('bmi', 25))
        scores['glucose'] = self.calculate_glucose_score(health_data.get('avg_glucose_level', 100))
        scores['blood_pressure'] = self.calculate_blood_pressure_score(
            health_data.get('blood_pressure_systolic'),
            health_data.get('blood_pressure_diastolic')
        )
        scores['heart_rate'] = self.calculate_heart_rate_score(health_data.get('heart_rate'))
        
        # Age score (younger = better)
        age = health_data.get('age', 30)
        scores['age'] = max(60, 100 - (age - 25) * 0.5)
        
        # Smoking score
        scores['smoking'] = 100 if health_data.get('smoking_status') != 'yes' else 50
        
        # Calculate weighted average
        total_score = 0
        total_weight = 0
        
        for component, weight in self.health_weights.items():
            if component in scores:
                total_score += scores[component] * weight
                total_weight += weight
        
        return round(total_score / total_weight, 1) if total_weight > 0 else 70
    
    def generate_personalized_recommendations(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate personalized health recommendations"""
        recommendations = []
        
        # Diabetes recommendations
        diabetes_risk = predictions.get('diabetes_risk', 0)
        if diabetes_risk > self.risk_thresholds['diabetes']:
            recommendations.append({
                "category": "Diabetes Prevention",
                "priority": "high",
                "risk_level": "high",
                "recommendation": "Your diabetes risk is elevated. Focus on blood glucose management.",
                "action_items": [
                    "Monitor blood glucose 2-3 times daily",
                    "Reduce refined sugar and simple carbohydrates",
                    "Exercise for 30 minutes daily",
                    "Maintain healthy weight",
                    "Schedule regular checkups with your doctor"
                ],
                "lifestyle_tips": [
                    "Choose whole grains over refined grains",
                    "Eat smaller, more frequent meals",
                    "Stay hydrated with water",
                    "Get adequate sleep (7-8 hours)"
                ]
            })
        elif diabetes_risk > 0.3:
            recommendations.append({
                "category": "Diabetes Prevention",
                "priority": "medium",
                "risk_level": "moderate",
                "recommendation": "Take preventive measures to reduce diabetes risk.",
                "action_items": [
                    "Monitor blood glucose weekly",
                    "Maintain healthy diet",
                    "Exercise regularly",
                    "Keep weight in healthy range"
                ],
                "lifestyle_tips": [
                    "Limit sugary beverages",
                    "Include fiber-rich foods",
                    "Stay physically active"
                ]
            })
        
        # Hypertension recommendations
        hypertension_risk = predictions.get('hypertension_risk', 0)
        if hypertension_risk > self.risk_thresholds['hypertension']:
            recommendations.append({
                "category": "Blood Pressure Management",
                "priority": "high",
                "risk_level": "high",
                "recommendation": "Your blood pressure risk is elevated. Focus on BP control.",
                "action_items": [
                    "Monitor blood pressure daily",
                    "Reduce sodium intake to <2,300mg/day",
                    "Practice stress management techniques",
                    "Exercise regularly",
                    "Limit alcohol consumption"
                ],
                "lifestyle_tips": [
                    "Use herbs and spices instead of salt",
                    "Practice deep breathing exercises",
                    "Get regular physical activity",
                    "Maintain healthy weight"
                ]
            })
        
        # Heart disease recommendations
        heart_disease_risk = predictions.get('heart_disease_risk', 0)
        if heart_disease_risk > self.risk_thresholds['heart_disease']:
            recommendations.append({
                "category": "Heart Health",
                "priority": "high",
                "risk_level": "high",
                "recommendation": "Focus on cardiovascular health and risk reduction.",
                "action_items": [
                    "Quit smoking immediately",
                    "Exercise 150 minutes/week",
                    "Eat heart-healthy diet",
                    "Monitor cholesterol levels",
                    "Manage stress effectively"
                ],
                "lifestyle_tips": [
                    "Choose lean proteins",
                    "Include omega-3 rich foods",
                    "Practice meditation or yoga",
                    "Get regular cardiovascular exercise"
                ]
            })
        
        # BMI-based recommendations
        bmi = health_data.get('bmi', 25)
        if bmi > 30:
            recommendations.append({
                "category": "Weight Management",
                "priority": "high",
                "risk_level": "high",
                "recommendation": "Focus on healthy weight loss to improve overall health.",
                "action_items": [
                    "Create a calorie deficit of 500-750 calories/day",
                    "Exercise 45-60 minutes daily",
                    "Track food intake",
                    "Set realistic weight loss goals",
                    "Consult with a nutritionist"
                ],
                "lifestyle_tips": [
                    "Eat more vegetables and fruits",
                    "Choose whole foods over processed",
                    "Practice portion control",
                    "Stay consistent with exercise"
                ]
            })
        elif bmi > 25:
            recommendations.append({
                "category": "Weight Management",
                "priority": "medium",
                "risk_level": "moderate",
                "recommendation": "Maintain healthy weight through balanced lifestyle.",
                "action_items": [
                    "Exercise 30 minutes daily",
                    "Eat balanced meals",
                    "Monitor portion sizes",
                    "Stay active throughout the day"
                ],
                "lifestyle_tips": [
                    "Take stairs instead of elevator",
                    "Walk during breaks",
                    "Choose healthy snacks",
                    "Stay hydrated"
                ]
            })
        
        # General health recommendations
        overall_score = predictions.get('overall_health_score', 70)
        if overall_score < 80:
            recommendations.append({
                "category": "General Health",
                "priority": "medium",
                "risk_level": "moderate",
                "recommendation": "Focus on improving overall health and wellness.",
                "action_items": [
                    "Get 7-8 hours of quality sleep",
                    "Stay hydrated (8 glasses water/day)",
                    "Eat balanced, nutritious meals",
                    "Exercise regularly",
                    "Schedule annual checkups"
                ],
                "lifestyle_tips": [
                    "Practice good sleep hygiene",
                    "Include variety in your diet",
                    "Find physical activities you enjoy",
                    "Manage stress through hobbies"
                ]
            })
        
        # Add positive reinforcement for good health
        if overall_score >= 85:
            recommendations.append({
                "category": "Health Maintenance",
                "priority": "low",
                "risk_level": "low",
                "recommendation": "Excellent health! Keep up the great work.",
                "action_items": [
                    "Continue current healthy habits",
                    "Stay consistent with exercise",
                    "Maintain balanced diet",
                    "Regular health checkups"
                ],
                "lifestyle_tips": [
                    "Try new healthy recipes",
                    "Explore new physical activities",
                    "Share healthy habits with others",
                    "Set new health goals"
                ]
            })
        
        return recommendations
    
    def analyze_health_trends(self, health_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze health trends over time"""
        if len(health_history) < 2:
            return {"trend": "insufficient_data", "message": "Need more data points for trend analysis"}
        
        trends = {}
        
        # BMI trends
        bmi_values = [entry.get('bmi') for entry in health_history if entry.get('bmi')]
        if len(bmi_values) >= 2:
            bmi_change = bmi_values[-1] - bmi_values[0]
            trends['bmi'] = {
                'change': round(bmi_change, 2),
                'direction': 'improving' if bmi_change < 0 else 'worsening' if bmi_change > 0 else 'stable',
                'trend': 'decreasing' if bmi_change < -0.5 else 'increasing' if bmi_change > 0.5 else 'stable'
            }
        
        # Glucose trends
        glucose_values = [entry.get('avg_glucose_level') for entry in health_history if entry.get('avg_glucose_level')]
        if len(glucose_values) >= 2:
            glucose_change = glucose_values[-1] - glucose_values[0]
            trends['glucose'] = {
                'change': round(glucose_change, 2),
                'direction': 'improving' if glucose_change < 0 else 'worsening' if glucose_change > 0 else 'stable',
                'trend': 'decreasing' if glucose_change < -5 else 'increasing' if glucose_change > 5 else 'stable'
            }
        
        # Blood pressure trends
        systolic_values = [entry.get('blood_pressure_systolic') for entry in health_history if entry.get('blood_pressure_systolic')]
        if len(systolic_values) >= 2:
            systolic_change = systolic_values[-1] - systolic_values[0]
            trends['blood_pressure'] = {
                'systolic_change': round(systolic_change, 2),
                'direction': 'improving' if systolic_change < 0 else 'worsening' if systolic_change > 0 else 'stable',
                'trend': 'decreasing' if systolic_change < -5 else 'increasing' if systolic_change > 5 else 'stable'
            }
        
        return trends
    
    def predict_health_risks(self, health_data: Dict[str, Any]) -> Dict[str, float]:
        """Predict all health risks and calculate overall health score"""
        predictions = {
            'diabetes_risk': self.predict_diabetes_risk(health_data),
            'hypertension_risk': self.predict_hypertension_risk(health_data),
            'heart_disease_risk': self.predict_heart_disease_risk(health_data),
            'overall_health_score': self.calculate_overall_health_score(health_data)
        }
        
        return predictions

# Global instance
health_models = HealthRiskModels()
