# 🏥 HealthNet MongoDB Setup Guide

This guide will help you set up MongoDB for your HealthNet AI-Powered Preventive Healthcare project.

## 🎯 Why MongoDB?

- **🆓 Completely Free** - MongoDB Community Edition
- **📊 Flexible Schema** - Perfect for evolving health data
- **🔍 Rich Queries** - Great for health analytics
- **📱 Easy Setup** - Simple installation and configuration
- **⚡ Fast Performance** - Excellent for real-time health tracking
- **🌐 Cloud Ready** - MongoDB Atlas (free tier available)

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (for version control)

## 🚀 Installation Steps

### Step 1: Install MongoDB

#### Windows:
```bash
# Option 1: Download installer
# Visit: https://www.mongodb.com/try/download/community

# Option 2: Using Chocolatey
choco install mongodb

# Option 3: Using winget
winget install MongoDB.Server
```

#### macOS:
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

#### Ubuntu/Debian:
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Create list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update package database
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Step 2: Verify MongoDB Installation

```bash
# Check MongoDB version
mongod --version

# Check if MongoDB is running
# Windows: Check Services app for "MongoDB" service
# Linux/macOS: sudo systemctl status mongod
```

### Step 3: Install Python Dependencies

```bash
cd healthnet-project/backend
pip install -r requirements.txt
```

### Step 4: Run Setup Script

```bash
python setup_mongodb.py
```

This script will:
- Check if MongoDB is installed
- Start MongoDB service
- Create a `.env` file with configuration

### Step 5: Start the Server

```bash
python run_server.py
```

## 🧪 Testing the Setup

### 1. Check API Documentation
Visit: http://localhost:8000/docs

### 2. Test Registration
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "password123",
       "name": "Test User",
       "age": 30,
       "gender": "Male"
     }'
```

### 3. Test Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "password123"
     }'
```

## 🗄️ Database Collections

The HealthNet MongoDB database includes the following collections:

### Users Collection
- `_id`: ObjectId (auto-generated)
- `email`: String (unique)
- `password_hash`: String (hashed password)
- `name`: String
- `age`: Integer
- `gender`: String
- `phone`: String (optional)
- `abha_id`: String (optional)
- `is_active`: Boolean
- `created_at`: Date
- `updated_at`: Date

### Health Assessments Collection
- `_id`: ObjectId (auto-generated)
- `user_id`: String (reference to user)
- `age`: Integer
- `avg_glucose_level`: Float
- `bmi`: Float
- `gender`: String
- `smoking_status`: String
- `diabetes_risk`: Float
- `hypertension_risk`: Float
- `overall_health_score`: Float
- `blood_pressure_systolic`: Integer (optional)
- `blood_pressure_diastolic`: Integer (optional)
- `heart_rate`: Integer (optional)
- `weight`: Float (optional)
- `height`: Float (optional)
- `created_at`: Date

### Food Entries Collection
- `_id`: ObjectId (auto-generated)
- `user_id`: String (reference to user)
- `food_name`: String
- `calories`: Float
- `protein`: Float (optional)
- `carbs`: Float (optional)
- `fat`: Float (optional)
- `meal_type`: String (breakfast, lunch, dinner, snack)
- `consumed_at`: Date

### Exercise Entries Collection
- `_id`: ObjectId (auto-generated)
- `user_id`: String (reference to user)
- `exercise_name`: String
- `duration_minutes`: Integer
- `calories_burned`: Float
- `exercise_type`: String (cardio, strength, flexibility)
- `performed_at`: Date

### AI Recommendations Collection
- `_id`: ObjectId (auto-generated)
- `user_id`: String (reference to user)
- `category`: String
- `priority`: String (high, medium, low)
- `recommendation`: String
- `action_items`: Array of strings
- `is_read`: Boolean
- `generated_at`: Date

## 🔧 Troubleshooting

### Common Issues:

#### 1. Connection Error
```
Error: could not connect to MongoDB
```
**Solution**: Ensure MongoDB service is running
- Windows: Check Services app for "MongoDB" service
- macOS: `brew services start mongodb/brew/mongodb-community`
- Linux: `sudo systemctl start mongod`

#### 2. Port Already in Use
```
Error: Address already in use
```
**Solution**: Check if MongoDB is already running on port 27017

#### 3. Permission Error
```
Error: permission denied
```
**Solution**: Ensure proper permissions for MongoDB data directory

#### 4. Python Dependencies Error
```
Error: No module named 'motor'
```
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## 🌐 MongoDB Atlas (Cloud Option)

For cloud deployment, you can use MongoDB Atlas (free tier):

1. **Sign up** at https://www.mongodb.com/atlas
2. **Create a cluster** (free tier available)
3. **Get connection string** from your cluster
4. **Update .env file**:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/healthnet
```

## 🎉 Success!

Once everything is working:

1. **Frontend**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Documentation**: http://localhost:8000/docs
4. **Health Check**: http://localhost:8000/

## 🔮 Next Steps

- Test user registration and login
- Submit health assessments
- Track nutrition and exercise
- View AI recommendations
- Explore the dashboard

## 💡 MongoDB Advantages for HealthNet

1. **Flexible Schema**: Easy to add new health metrics
2. **JSON-like Documents**: Natural fit for health records
3. **Rich Queries**: Powerful aggregation for health analytics
4. **Scalability**: Handles large datasets efficiently
5. **Real-time**: Excellent for live health tracking
6. **Free**: No licensing costs

Your HealthNet application is now running with MongoDB! 🏥✨
