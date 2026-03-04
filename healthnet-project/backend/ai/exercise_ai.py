import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class ExerciseAI:
    """AI-powered exercise recommendation system"""
    
    def __init__(self):
        # Exercise intensity levels
        self.intensity_levels = {
            'beginner': {'fitness_score': 0, 'max_hr_percentage': 0.6},
            'intermediate': {'fitness_score': 50, 'max_hr_percentage': 0.7},
            'advanced': {'fitness_score': 80, 'max_hr_percentage': 0.8}
        }
        
        # Exercise database
        self.exercise_database = {
            'cardio': {
                'walking': {
                    'calories_per_hour': 300,
                    'intensity': 'low',
                    'equipment': 'none',
                    'benefits': ['heart health', 'weight management', 'mood improvement'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                },
                'jogging': {
                    'calories_per_hour': 600,
                    'intensity': 'moderate',
                    'equipment': 'running shoes',
                    'benefits': ['cardiovascular fitness', 'weight loss', 'bone health'],
                    'suitable_for': ['intermediate', 'advanced']
                },
                'cycling': {
                    'calories_per_hour': 500,
                    'intensity': 'moderate',
                    'equipment': 'bicycle',
                    'benefits': ['leg strength', 'cardiovascular health', 'low impact'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                },
                'swimming': {
                    'calories_per_hour': 400,
                    'intensity': 'moderate',
                    'equipment': 'pool access',
                    'benefits': ['full body workout', 'low impact', 'flexibility'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                },
                'hiit': {
                    'calories_per_hour': 800,
                    'intensity': 'high',
                    'equipment': 'none',
                    'benefits': ['maximum calorie burn', 'metabolic boost', 'time efficient'],
                    'suitable_for': ['advanced']
                }
            },
            'strength': {
                'bodyweight_exercises': {
                    'calories_per_hour': 300,
                    'intensity': 'moderate',
                    'equipment': 'none',
                    'benefits': ['muscle building', 'functional strength', 'convenience'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                },
                'weight_training': {
                    'calories_per_hour': 400,
                    'intensity': 'moderate',
                    'equipment': 'weights/gym',
                    'benefits': ['muscle mass', 'bone density', 'metabolism boost'],
                    'suitable_for': ['intermediate', 'advanced']
                },
                'resistance_bands': {
                    'calories_per_hour': 250,
                    'intensity': 'low-moderate',
                    'equipment': 'resistance bands',
                    'benefits': ['muscle toning', 'portable', 'joint friendly'],
                    'suitable_for': ['beginner', 'intermediate']
                }
            },
            'flexibility': {
                'yoga': {
                    'calories_per_hour': 200,
                    'intensity': 'low',
                    'equipment': 'yoga mat',
                    'benefits': ['flexibility', 'stress relief', 'balance'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                },
                'stretching': {
                    'calories_per_hour': 150,
                    'intensity': 'low',
                    'equipment': 'none',
                    'benefits': ['flexibility', 'injury prevention', 'recovery'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                },
                'pilates': {
                    'calories_per_hour': 250,
                    'intensity': 'low-moderate',
                    'equipment': 'mat',
                    'benefits': ['core strength', 'posture', 'mind-body connection'],
                    'suitable_for': ['beginner', 'intermediate', 'advanced']
                }
            }
        }
        
        # Weekly exercise recommendations
        self.weekly_recommendations = {
            'cardio_minutes': 150,
            'strength_sessions': 2,
            'flexibility_sessions': 3,
            'rest_days': 1
        }
    
    def calculate_fitness_score(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> float:
        """Calculate overall fitness score (0-100)"""
        score = 0
        
        # Age factor (younger = better)
        age = health_data.get('age', 30)
        age_score = max(60, 100 - (age - 25) * 0.5)
        score += age_score * 0.2
        
        # BMI factor
        bmi = health_data.get('bmi', 25)
        if 18.5 <= bmi <= 25:
            bmi_score = 100
        elif 25 < bmi <= 30:
            bmi_score = 80
        elif bmi > 30:
            bmi_score = 60
        else:
            bmi_score = 70
        score += bmi_score * 0.3
        
        # Health risk factors
        diabetes_risk = predictions.get('diabetes_risk', 0)
        hypertension_risk = predictions.get('hypertension_risk', 0)
        heart_disease_risk = predictions.get('heart_disease_risk', 0)
        
        risk_score = 100 - (diabetes_risk + hypertension_risk + heart_disease_risk) * 50
        score += risk_score * 0.3
        
        # Overall health score
        overall_health = predictions.get('overall_health_score', 70)
        score += overall_health * 0.2
        
        return round(score, 1)
    
    def determine_fitness_level(self, fitness_score: float) -> str:
        """Determine fitness level based on score"""
        if fitness_score >= 80:
            return 'advanced'
        elif fitness_score >= 50:
            return 'intermediate'
        else:
            return 'beginner'
    
    def calculate_target_heart_rate(self, age: int, fitness_level: str) -> Dict[str, int]:
        """Calculate target heart rate zones"""
        max_hr = 220 - age
        intensity = self.intensity_levels[fitness_level]
        
        target_hr = int(max_hr * intensity['max_hr_percentage'])
        
        return {
            'max_hr': max_hr,
            'target_hr': target_hr,
            'hr_range': f"{target_hr - 10}-{target_hr + 10}"
        }
    
    def generate_weekly_workout_plan(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> Dict[str, Any]:
        """Generate personalized weekly workout plan"""
        fitness_score = self.calculate_fitness_score(health_data, predictions)
        fitness_level = self.determine_fitness_level(fitness_score)
        age = health_data.get('age', 30)
        heart_rate_info = self.calculate_target_heart_rate(age, fitness_level)
        
        # Determine exercise focus based on health data
        focus_areas = self.determine_exercise_focus(health_data, predictions)
        
        # Generate workout schedule
        workout_schedule = self.create_workout_schedule(fitness_level, focus_areas)
        
        # Calculate weekly calorie burn
        weekly_calories = self.calculate_weekly_calories(workout_schedule, fitness_level)
        
        return {
            'fitness_score': fitness_score,
            'fitness_level': fitness_level,
            'heart_rate_zones': heart_rate_info,
            'focus_areas': focus_areas,
            'weekly_schedule': workout_schedule,
            'weekly_calories': weekly_calories,
            'progression_plan': self.create_progression_plan(fitness_level),
            'safety_guidelines': self.get_safety_guidelines(health_data, predictions)
        }
    
    def determine_exercise_focus(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> List[str]:
        """Determine exercise focus areas based on health data"""
        focus_areas = []
        
        diabetes_risk = predictions.get('diabetes_risk', 0)
        hypertension_risk = predictions.get('hypertension_risk', 0)
        heart_disease_risk = predictions.get('heart_disease_risk', 0)
        bmi = health_data.get('bmi', 25)
        
        if diabetes_risk > 0.6:
            focus_areas.extend(['cardio', 'weight_management'])
        if hypertension_risk > 0.6:
            focus_areas.extend(['cardio', 'stress_management'])
        if heart_disease_risk > 0.6:
            focus_areas.extend(['cardio', 'strength'])
        if bmi > 30:
            focus_areas.extend(['weight_management', 'cardio'])
        if bmi < 18.5:
            focus_areas.extend(['strength', 'muscle_building'])
        
        # Always include general fitness
        if not focus_areas:
            focus_areas = ['general_fitness']
        
        return list(set(focus_areas))  # Remove duplicates
    
    def create_workout_schedule(self, fitness_level: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Create weekly workout schedule"""
        schedule = {
            'monday': self.generate_workout('monday', fitness_level, focus_areas),
            'tuesday': self.generate_workout('tuesday', fitness_level, focus_areas),
            'wednesday': self.generate_workout('wednesday', fitness_level, focus_areas),
            'thursday': self.generate_workout('thursday', fitness_level, focus_areas),
            'friday': self.generate_workout('friday', fitness_level, focus_areas),
            'saturday': self.generate_workout('saturday', fitness_level, focus_areas),
            'sunday': self.generate_workout('sunday', fitness_level, focus_areas)
        }
        
        return schedule
    
    def generate_workout(self, day: str, fitness_level: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Generate workout for specific day"""
        if day == 'sunday':  # Rest day
            return {
                'type': 'rest',
                'activities': ['Light stretching', 'Walking', 'Recovery'],
                'duration': 30,
                'intensity': 'low',
                'calories': 100
            }
        
        # Determine workout type based on day and focus areas
        if 'cardio' in focus_areas and day in ['monday', 'wednesday', 'friday']:
            workout_type = 'cardio'
        elif 'strength' in focus_areas and day in ['tuesday', 'thursday']:
            workout_type = 'strength'
        elif 'flexibility' in focus_areas and day == 'saturday':
            workout_type = 'flexibility'
        else:
            # Default rotation
            if day in ['monday', 'thursday']:
                workout_type = 'cardio'
            elif day in ['tuesday', 'friday']:
                workout_type = 'strength'
            else:
                workout_type = 'flexibility'
        
        return self.create_workout_details(workout_type, fitness_level, focus_areas)
    
    def create_workout_details(self, workout_type: str, fitness_level: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Create detailed workout plan"""
        if workout_type == 'cardio':
            return self.create_cardio_workout(fitness_level, focus_areas)
        elif workout_type == 'strength':
            return self.create_strength_workout(fitness_level, focus_areas)
        else:  # flexibility
            return self.create_flexibility_workout(fitness_level, focus_areas)
    
    def create_cardio_workout(self, fitness_level: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Create cardio workout plan"""
        if fitness_level == 'beginner':
            exercises = [
                {'name': 'Walking', 'duration': 20, 'intensity': 'low'},
                {'name': 'Light jogging', 'duration': 10, 'intensity': 'moderate'}
            ]
            total_duration = 30
        elif fitness_level == 'intermediate':
            exercises = [
                {'name': 'Jogging', 'duration': 25, 'intensity': 'moderate'},
                {'name': 'Cycling', 'duration': 15, 'intensity': 'moderate'}
            ]
            total_duration = 40
        else:  # advanced
            exercises = [
                {'name': 'Running', 'duration': 30, 'intensity': 'high'},
                {'name': 'HIIT intervals', 'duration': 15, 'intensity': 'high'}
            ]
            total_duration = 45
        
        return {
            'type': 'cardio',
            'exercises': exercises,
            'duration': total_duration,
            'intensity': 'moderate-high',
            'calories': self.calculate_workout_calories('cardio', total_duration, fitness_level),
            'tips': self.get_cardio_tips(fitness_level, focus_areas)
        }
    
    def create_strength_workout(self, fitness_level: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Create strength workout plan"""
        if fitness_level == 'beginner':
            exercises = [
                {'name': 'Push-ups', 'sets': 3, 'reps': 5, 'rest': 60},
                {'name': 'Squats', 'sets': 3, 'reps': 10, 'rest': 60},
                {'name': 'Plank', 'sets': 3, 'duration': 20, 'rest': 60},
                {'name': 'Lunges', 'sets': 3, 'reps': 8, 'rest': 60}
            ]
        elif fitness_level == 'intermediate':
            exercises = [
                {'name': 'Push-ups', 'sets': 4, 'reps': 12, 'rest': 45},
                {'name': 'Squats', 'sets': 4, 'reps': 15, 'rest': 45},
                {'name': 'Plank', 'sets': 4, 'duration': 30, 'rest': 45},
                {'name': 'Lunges', 'sets': 4, 'reps': 12, 'rest': 45},
                {'name': 'Dips', 'sets': 3, 'reps': 8, 'rest': 60}
            ]
        else:  # advanced
            exercises = [
                {'name': 'Push-ups', 'sets': 5, 'reps': 20, 'rest': 30},
                {'name': 'Squats', 'sets': 5, 'reps': 20, 'rest': 30},
                {'name': 'Plank', 'sets': 5, 'duration': 45, 'rest': 30},
                {'name': 'Lunges', 'sets': 5, 'reps': 15, 'rest': 30},
                {'name': 'Pull-ups', 'sets': 4, 'reps': 10, 'rest': 45},
                {'name': 'Burpees', 'sets': 3, 'reps': 10, 'rest': 60}
            ]
        
        return {
            'type': 'strength',
            'exercises': exercises,
            'duration': 45,
            'intensity': 'moderate',
            'calories': self.calculate_workout_calories('strength', 45, fitness_level),
            'tips': self.get_strength_tips(fitness_level, focus_areas)
        }
    
    def create_flexibility_workout(self, fitness_level: str, focus_areas: List[str]) -> Dict[str, Any]:
        """Create flexibility workout plan"""
        exercises = [
            {'name': 'Hamstring stretch', 'duration': 30, 'sets': 3},
            {'name': 'Quad stretch', 'duration': 30, 'sets': 3},
            {'name': 'Chest stretch', 'duration': 30, 'sets': 3},
            {'name': 'Shoulder stretch', 'duration': 30, 'sets': 3},
            {'name': 'Hip flexor stretch', 'duration': 30, 'sets': 3}
        ]
        
        if fitness_level == 'intermediate':
            exercises.extend([
                {'name': 'Yoga flow', 'duration': 15, 'sets': 1},
                {'name': 'Pilates core', 'duration': 10, 'sets': 1}
            ])
        
        if fitness_level == 'advanced':
            exercises.extend([
                {'name': 'Advanced yoga poses', 'duration': 20, 'sets': 1},
                {'name': 'Pilates full body', 'duration': 15, 'sets': 1}
            ])
        
        return {
            'type': 'flexibility',
            'exercises': exercises,
            'duration': 30,
            'intensity': 'low',
            'calories': self.calculate_workout_calories('flexibility', 30, fitness_level),
            'tips': self.get_flexibility_tips(fitness_level, focus_areas)
        }
    
    def calculate_workout_calories(self, workout_type: str, duration: int, fitness_level: str) -> int:
        """Calculate calories burned for workout"""
        base_calories = {
            'cardio': {'beginner': 300, 'intermediate': 400, 'advanced': 500},
            'strength': {'beginner': 200, 'intermediate': 250, 'advanced': 300},
            'flexibility': {'beginner': 100, 'intermediate': 120, 'advanced': 150}
        }
        
        base = base_calories[workout_type][fitness_level]
        return int(base * (duration / 60))
    
    def calculate_weekly_calories(self, workout_schedule: Dict[str, Any], fitness_level: str) -> int:
        """Calculate total weekly calories burned"""
        total_calories = 0
        for day, workout in workout_schedule.items():
            total_calories += workout.get('calories', 0)
        return total_calories
    
    def create_progression_plan(self, fitness_level: str) -> Dict[str, Any]:
        """Create progression plan for fitness improvement"""
        if fitness_level == 'beginner':
            return {
                'goal': 'Build consistent exercise habit',
                'timeline': '4-8 weeks',
                'milestones': [
                    'Week 1-2: Complete 3 workouts per week',
                    'Week 3-4: Increase workout duration by 10%',
                    'Week 5-6: Add one additional workout day',
                    'Week 7-8: Increase intensity gradually'
                ],
                'next_level': 'intermediate'
            }
        elif fitness_level == 'intermediate':
            return {
                'goal': 'Improve strength and endurance',
                'timeline': '6-12 weeks',
                'milestones': [
                    'Week 1-3: Increase workout intensity',
                    'Week 4-6: Add more challenging exercises',
                    'Week 7-9: Improve workout consistency',
                    'Week 10-12: Achieve advanced fitness markers'
                ],
                'next_level': 'advanced'
            }
        else:  # advanced
            return {
                'goal': 'Maintain peak fitness and performance',
                'timeline': 'Ongoing',
                'milestones': [
                    'Maintain current fitness level',
                    'Set new personal records',
                    'Try new exercise modalities',
                    'Help others achieve fitness goals'
                ],
                'next_level': 'elite'
            }
    
    def get_safety_guidelines(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> List[str]:
        """Get safety guidelines based on health data"""
        guidelines = [
            "Always warm up before exercise",
            "Stay hydrated during workouts",
            "Listen to your body and stop if you feel pain",
            "Consult a doctor before starting new exercise program"
        ]
        
        diabetes_risk = predictions.get('diabetes_risk', 0)
        hypertension_risk = predictions.get('hypertension_risk', 0)
        heart_disease_risk = predictions.get('heart_disease_risk', 0)
        
        if diabetes_risk > 0.6:
            guidelines.extend([
                "Monitor blood sugar before and after exercise",
                "Keep glucose tablets or juice nearby",
                "Exercise with a partner when possible"
            ])
        
        if hypertension_risk > 0.6:
            guidelines.extend([
                "Monitor blood pressure regularly",
                "Avoid heavy lifting and high-intensity exercise",
                "Focus on moderate, steady-state cardio"
            ])
        
        if heart_disease_risk > 0.6:
            guidelines.extend([
                "Get medical clearance before exercise",
                "Start with low-intensity activities",
                "Monitor heart rate during exercise",
                "Stop immediately if you experience chest pain"
            ])
        
        return guidelines
    
    def get_cardio_tips(self, fitness_level: str, focus_areas: List[str]) -> List[str]:
        """Get cardio workout tips"""
        tips = [
            "Start slow and gradually increase intensity",
            "Maintain proper form throughout",
            "Breathe rhythmically"
        ]
        
        if fitness_level == 'beginner':
            tips.extend([
                "Focus on consistency over intensity",
                "Take walking breaks as needed",
                "Aim for 30 minutes of activity"
            ])
        elif fitness_level == 'intermediate':
            tips.extend([
                "Include interval training",
                "Vary your cardio activities",
                "Monitor your heart rate"
            ])
        else:  # advanced
            tips.extend([
                "Push your limits safely",
                "Include high-intensity intervals",
                "Cross-train for variety"
            ])
        
        return tips
    
    def get_strength_tips(self, fitness_level: str, focus_areas: List[str]) -> List[str]:
        """Get strength workout tips"""
        tips = [
            "Focus on proper form over weight",
            "Breathe steadily during exercises",
            "Rest between sets"
        ]
        
        if fitness_level == 'beginner':
            tips.extend([
                "Start with bodyweight exercises",
                "Learn proper technique first",
                "Don't rush through movements"
            ])
        elif fitness_level == 'intermediate':
            tips.extend([
                "Gradually increase resistance",
                "Include compound movements",
                "Focus on progressive overload"
            ])
        else:  # advanced
            tips.extend([
                "Challenge yourself with advanced variations",
                "Include plyometric exercises",
                "Focus on functional strength"
            ])
        
        return tips
    
    def get_flexibility_tips(self, fitness_level: str, focus_areas: List[str]) -> List[str]:
        """Get flexibility workout tips"""
        tips = [
            "Hold stretches for 20-30 seconds",
            "Don't bounce during stretches",
            "Breathe deeply and relax"
        ]
        
        if fitness_level == 'beginner':
            tips.extend([
                "Start with basic stretches",
                "Don't force movements",
                "Be patient with progress"
            ])
        elif fitness_level == 'intermediate':
            tips.extend([
                "Include dynamic stretching",
                "Try yoga or Pilates",
                "Focus on mobility"
            ])
        else:  # advanced
            tips.extend([
                "Explore advanced yoga poses",
                "Include proprioceptive training",
                "Work on balance and stability"
            ])
        
        return tips

# Global instance
exercise_ai = ExerciseAI()
