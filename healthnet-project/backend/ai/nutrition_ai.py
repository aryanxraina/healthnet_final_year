import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class NutritionAI:
    """AI-powered nutrition recommendation system"""
    
    def __init__(self):
        # Daily calorie needs based on age, gender, activity level
        self.base_calories = {
            'male': {
                'sedentary': 2000,
                'lightly_active': 2200,
                'moderately_active': 2400,
                'very_active': 2800
            },
            'female': {
                'sedentary': 1600,
                'lightly_active': 1800,
                'moderately_active': 2000,
                'very_active': 2400
            }
        }
        
        # Macronutrient ratios
        self.macro_ratios = {
            'balanced': {'protein': 0.25, 'carbs': 0.45, 'fat': 0.30},
            'low_carb': {'protein': 0.30, 'carbs': 0.25, 'fat': 0.45},
            'high_protein': {'protein': 0.35, 'carbs': 0.40, 'fat': 0.25},
            'diabetic': {'protein': 0.25, 'carbs': 0.40, 'fat': 0.35}
        }
        
        # Food database with nutritional information
        self.food_database = {
            'proteins': {
                'chicken_breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
                'salmon': {'calories': 208, 'protein': 25, 'carbs': 0, 'fat': 12},
                'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11},
                'tofu': {'calories': 76, 'protein': 8, 'carbs': 1.9, 'fat': 4.8},
                'lentils': {'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4},
                'greek_yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4}
            },
            'carbs': {
                'brown_rice': {'calories': 111, 'protein': 2.6, 'carbs': 23, 'fat': 0.9},
                'quinoa': {'calories': 120, 'protein': 4.4, 'carbs': 22, 'fat': 1.9},
                'sweet_potato': {'calories': 103, 'protein': 2, 'carbs': 24, 'fat': 0.2},
                'oats': {'calories': 68, 'protein': 2.4, 'carbs': 12, 'fat': 1.4},
                'whole_wheat_bread': {'calories': 69, 'protein': 3.6, 'carbs': 12, 'fat': 1.1}
            },
            'vegetables': {
                'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 7, 'fat': 0.4},
                'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4},
                'carrots': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2},
                'bell_peppers': {'calories': 31, 'protein': 1, 'carbs': 7, 'fat': 0.3},
                'tomatoes': {'calories': 22, 'protein': 1.1, 'carbs': 4.8, 'fat': 0.2}
            },
            'fruits': {
                'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2},
                'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3},
                'berries': {'calories': 57, 'protein': 0.7, 'carbs': 14, 'fat': 0.3},
                'orange': {'calories': 47, 'protein': 0.9, 'carbs': 12, 'fat': 0.1}
            },
            'fats': {
                'avocado': {'calories': 160, 'protein': 2, 'carbs': 9, 'fat': 15},
                'nuts': {'calories': 607, 'protein': 20, 'carbs': 23, 'fat': 54},
                'olive_oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100},
                'cheese': {'calories': 113, 'protein': 7, 'carbs': 1.3, 'fat': 9}
            }
        }
    
    def calculate_daily_calories(self, health_data: Dict[str, Any], activity_level: str = 'moderately_active') -> int:
        """Calculate daily calorie needs based on health data"""
        age = health_data.get('age', 30)
        gender = health_data.get('gender', 'male').lower()
        weight = health_data.get('weight', 70)  # kg
        height = health_data.get('height', 170)  # cm
        
        # Base metabolic rate (BMR) using Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # Adjust based on health goals
        bmi = health_data.get('bmi', 25)
        if bmi > 30:  # Weight loss
            tdee *= 0.85
        elif bmi < 18.5:  # Weight gain
            tdee *= 1.15
        
        return int(tdee)
    
    def determine_diet_type(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> str:
        """Determine optimal diet type based on health data and risk predictions"""
        diabetes_risk = predictions.get('diabetes_risk', 0)
        hypertension_risk = predictions.get('hypertension_risk', 0)
        bmi = health_data.get('bmi', 25)
        
        if diabetes_risk > 0.6:
            return 'diabetic'
        elif bmi > 30:
            return 'low_carb'
        elif hypertension_risk > 0.6:
            return 'balanced'
        else:
            return 'balanced'
    
    def generate_meal_plan(self, health_data: Dict[str, Any], predictions: Dict[str, float], 
                          daily_calories: int) -> Dict[str, Any]:
        """Generate personalized meal plan"""
        diet_type = self.determine_diet_type(health_data, predictions)
        macro_ratios = self.macro_ratios[diet_type]
        
        # Calculate macro targets
        protein_cals = daily_calories * macro_ratios['protein']
        carbs_cals = daily_calories * macro_ratios['carbs']
        fat_cals = daily_calories * macro_ratios['fat']
        
        # Convert to grams
        protein_g = int(protein_cals / 4)
        carbs_g = int(carbs_cals / 4)
        fat_g = int(fat_cals / 9)
        
        # Distribute calories across meals
        meal_distribution = {
            'breakfast': 0.25,
            'lunch': 0.30,
            'dinner': 0.30,
            'snacks': 0.15
        }
        
        meal_plans = {}
        for meal, ratio in meal_distribution.items():
            meal_calories = int(daily_calories * ratio)
            meal_plans[meal] = self.generate_meal(meal_calories, meal, diet_type)
        
        return {
            'daily_calories': daily_calories,
            'macro_targets': {
                'protein_g': protein_g,
                'carbs_g': carbs_g,
                'fat_g': fat_g
            },
            'diet_type': diet_type,
            'meals': meal_plans,
            'nutritional_goals': self.get_nutritional_goals(health_data, predictions)
        }
    
    def generate_meal(self, target_calories: int, meal_type: str, diet_type: str) -> Dict[str, Any]:
        """Generate a specific meal"""
        if meal_type == 'breakfast':
            return self.generate_breakfast(target_calories, diet_type)
        elif meal_type == 'lunch':
            return self.generate_lunch(target_calories, diet_type)
        elif meal_type == 'dinner':
            return self.generate_dinner(target_calories, diet_type)
        else:  # snacks
            return self.generate_snacks(target_calories, diet_type)
    
    def generate_breakfast(self, calories: int, diet_type: str) -> Dict[str, Any]:
        """Generate breakfast meal"""
        if diet_type == 'diabetic':
            foods = [
                {'name': 'Greek yogurt', 'portion': '1 cup', 'calories': 130},
                {'name': 'Berries', 'portion': '1/2 cup', 'calories': 40},
                {'name': 'Nuts', 'portion': '1/4 cup', 'calories': 160},
                {'name': 'Oats', 'portion': '1/2 cup', 'calories': 150}
            ]
        elif diet_type == 'low_carb':
            foods = [
                {'name': 'Eggs', 'portion': '3 whole eggs', 'calories': 210},
                {'name': 'Avocado', 'portion': '1/2 medium', 'calories': 120},
                {'name': 'Spinach', 'portion': '1 cup', 'calories': 7}
            ]
        else:  # balanced
            foods = [
                {'name': 'Oatmeal', 'portion': '1 cup', 'calories': 150},
                {'name': 'Banana', 'portion': '1 medium', 'calories': 105},
                {'name': 'Almonds', 'portion': '1/4 cup', 'calories': 160}
            ]
        
        return {
            'meal_type': 'breakfast',
            'foods': foods,
            'total_calories': sum(food['calories'] for food in foods),
            'tips': self.get_breakfast_tips(diet_type)
        }
    
    def generate_lunch(self, calories: int, diet_type: str) -> Dict[str, Any]:
        """Generate lunch meal"""
        if diet_type == 'diabetic':
            foods = [
                {'name': 'Grilled chicken breast', 'portion': '4 oz', 'calories': 180},
                {'name': 'Quinoa', 'portion': '1/2 cup', 'calories': 110},
                {'name': 'Mixed vegetables', 'portion': '1 cup', 'calories': 50},
                {'name': 'Olive oil', 'portion': '1 tbsp', 'calories': 120}
            ]
        elif diet_type == 'low_carb':
            foods = [
                {'name': 'Salmon', 'portion': '4 oz', 'calories': 200},
                {'name': 'Cauliflower rice', 'portion': '1 cup', 'calories': 25},
                {'name': 'Broccoli', 'portion': '1 cup', 'calories': 30},
                {'name': 'Avocado', 'portion': '1/4 medium', 'calories': 60}
            ]
        else:  # balanced
            foods = [
                {'name': 'Turkey sandwich', 'portion': '1 whole wheat', 'calories': 300},
                {'name': 'Apple', 'portion': '1 medium', 'calories': 95},
                {'name': 'Carrot sticks', 'portion': '1 cup', 'calories': 50}
            ]
        
        return {
            'meal_type': 'lunch',
            'foods': foods,
            'total_calories': sum(food['calories'] for food in foods),
            'tips': self.get_lunch_tips(diet_type)
        }
    
    def generate_dinner(self, calories: int, diet_type: str) -> Dict[str, Any]:
        """Generate dinner meal"""
        if diet_type == 'diabetic':
            foods = [
                {'name': 'Baked fish', 'portion': '4 oz', 'calories': 150},
                {'name': 'Brown rice', 'portion': '1/3 cup', 'calories': 80},
                {'name': 'Steamed vegetables', 'portion': '1 cup', 'calories': 50},
                {'name': 'Greek yogurt', 'portion': '1/2 cup', 'calories': 65}
            ]
        elif diet_type == 'low_carb':
            foods = [
                {'name': 'Grilled steak', 'portion': '4 oz', 'calories': 250},
                {'name': 'Zucchini noodles', 'portion': '1 cup', 'calories': 20},
                {'name': 'Bell peppers', 'portion': '1 cup', 'calories': 30},
                {'name': 'Cheese', 'portion': '1 oz', 'calories': 110}
            ]
        else:  # balanced
            foods = [
                {'name': 'Lean beef', 'portion': '3 oz', 'calories': 180},
                {'name': 'Sweet potato', 'portion': '1 medium', 'calories': 100},
                {'name': 'Green beans', 'portion': '1 cup', 'calories': 40},
                {'name': 'Mixed salad', 'portion': '1 cup', 'calories': 20}
            ]
        
        return {
            'meal_type': 'dinner',
            'foods': foods,
            'total_calories': sum(food['calories'] for food in foods),
            'tips': self.get_dinner_tips(diet_type)
        }
    
    def generate_snacks(self, calories: int, diet_type: str) -> Dict[str, Any]:
        """Generate snack suggestions"""
        if diet_type == 'diabetic':
            snacks = [
                {'name': 'Nuts', 'portion': '1/4 cup', 'calories': 160},
                {'name': 'Greek yogurt', 'portion': '1/2 cup', 'calories': 65},
                {'name': 'Berries', 'portion': '1/2 cup', 'calories': 40}
            ]
        elif diet_type == 'low_carb':
            snacks = [
                {'name': 'Cheese', 'portion': '1 oz', 'calories': 110},
                {'name': 'Hard-boiled egg', 'portion': '1 egg', 'calories': 70},
                {'name': 'Avocado', 'portion': '1/4 medium', 'calories': 60}
            ]
        else:  # balanced
            snacks = [
                {'name': 'Apple with peanut butter', 'portion': '1 medium + 1 tbsp', 'calories': 200},
                {'name': 'Hummus with vegetables', 'portion': '2 tbsp + 1 cup', 'calories': 100},
                {'name': 'Trail mix', 'portion': '1/4 cup', 'calories': 150}
            ]
        
        return {
            'meal_type': 'snacks',
            'foods': snacks,
            'total_calories': sum(snack['calories'] for snack in snacks),
            'tips': self.get_snack_tips(diet_type)
        }
    
    def get_nutritional_goals(self, health_data: Dict[str, Any], predictions: Dict[str, float]) -> Dict[str, Any]:
        """Get nutritional goals based on health data"""
        goals = {
            'focus_areas': [],
            'foods_to_limit': [],
            'foods_to_include': [],
            'hydration_goal': '8-10 glasses of water daily'
        }
        
        diabetes_risk = predictions.get('diabetes_risk', 0)
        hypertension_risk = predictions.get('hypertension_risk', 0)
        bmi = health_data.get('bmi', 25)
        
        if diabetes_risk > 0.6:
            goals['focus_areas'].append('Blood sugar management')
            goals['foods_to_limit'].extend(['Refined sugars', 'White bread', 'Sugary beverages'])
            goals['foods_to_include'].extend(['Whole grains', 'Fiber-rich foods', 'Lean proteins'])
        
        if hypertension_risk > 0.6:
            goals['focus_areas'].append('Blood pressure control')
            goals['foods_to_limit'].extend(['High-sodium foods', 'Processed meats', 'Canned soups'])
            goals['foods_to_include'].extend(['Potassium-rich foods', 'Low-sodium options', 'Fresh vegetables'])
        
        if bmi > 30:
            goals['focus_areas'].append('Weight management')
            goals['foods_to_limit'].extend(['High-calorie snacks', 'Fried foods', 'Sugary drinks'])
            goals['foods_to_include'].extend(['High-fiber foods', 'Lean proteins', 'Vegetables'])
        
        return goals
    
    def get_breakfast_tips(self, diet_type: str) -> List[str]:
        """Get breakfast tips based on diet type"""
        if diet_type == 'diabetic':
            return [
                "Include protein to stabilize blood sugar",
                "Choose whole grains over refined grains",
                "Add fiber-rich foods like berries",
                "Avoid sugary cereals and pastries"
            ]
        elif diet_type == 'low_carb':
            return [
                "Focus on protein and healthy fats",
                "Include non-starchy vegetables",
                "Avoid bread, cereals, and fruits",
                "Consider intermittent fasting"
            ]
        else:
            return [
                "Include a mix of protein, carbs, and healthy fats",
                "Choose whole grain options",
                "Add fruits for natural sweetness",
                "Stay hydrated with water or tea"
            ]
    
    def get_lunch_tips(self, diet_type: str) -> List[str]:
        """Get lunch tips based on diet type"""
        if diet_type == 'diabetic':
            return [
                "Balance carbs with protein and fiber",
                "Choose lean protein sources",
                "Include non-starchy vegetables",
                "Monitor portion sizes"
            ]
        elif diet_type == 'low_carb':
            return [
                "Focus on protein and vegetables",
                "Use healthy fats for satiety",
                "Avoid rice, pasta, and bread",
                "Include fiber-rich vegetables"
            ]
        else:
            return [
                "Include lean protein, whole grains, and vegetables",
                "Choose healthy fats like avocado or nuts",
                "Stay hydrated",
                "Avoid processed foods"
            ]
    
    def get_dinner_tips(self, diet_type: str) -> List[str]:
        """Get dinner tips based on diet type"""
        if diet_type == 'diabetic':
            return [
                "Keep dinner light and balanced",
                "Include protein and non-starchy vegetables",
                "Limit carbs in the evening",
                "Avoid eating too close to bedtime"
            ]
        elif diet_type == 'low_carb':
            return [
                "Focus on protein and vegetables",
                "Use healthy cooking methods (grill, bake, steam)",
                "Include healthy fats",
                "Avoid starchy sides"
            ]
        else:
            return [
                "Include lean protein, whole grains, and vegetables",
                "Use healthy cooking methods",
                "Practice portion control",
                "Avoid heavy, fried foods"
            ]
    
    def get_snack_tips(self, diet_type: str) -> List[str]:
        """Get snack tips based on diet type"""
        if diet_type == 'diabetic':
            return [
                "Choose protein-rich snacks",
                "Include fiber for satiety",
                "Avoid sugary snacks",
                "Monitor blood sugar response"
            ]
        elif diet_type == 'low_carb':
            return [
                "Focus on protein and healthy fats",
                "Choose low-carb vegetables",
                "Avoid fruits and grains",
                "Stay hydrated"
            ]
        else:
            return [
                "Choose nutrient-dense options",
                "Include protein and fiber",
                "Avoid processed snacks",
                "Practice portion control"
            ]

# Global instance
nutrition_ai = NutritionAI()
