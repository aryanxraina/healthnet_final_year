# HealthNet - AI-Powered Preventive Healthcare

A comprehensive healthcare platform that combines user health data with advanced AI to provide personalized health insights, nutrition plans, and exercise recommendations.

## 🚀 Features

### Core Functionality
- **🔐 Secure Authentication** - JWT-based user registration, login, and session management
- **📊 Health Assessment** - Comprehensive health data collection and AI-powered risk prediction
- **🍎 Nutrition Tracking** - Food logging with AI-generated personalized meal plans
- **💪 Exercise Tracking** - Workout logging with AI-generated exercise routines
- **📈 Health Dashboard** - Real-time health metrics and trend analysis
- **🤖 AI Insights** - Advanced AI-powered health recommendations and analysis

### AI-Powered Features
- **Health Risk Prediction** - Diabetes, hypertension, and heart disease risk assessment
- **Personalized Nutrition Plans** - AI-generated meal plans based on health profile
- **Custom Exercise Routines** - Tailored workout plans for fitness goals
- **Health Trend Analysis** - Comprehensive health pattern recognition
- **Lifestyle Recommendations** - Personalized health and wellness advice

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database for flexible data storage
- **Motor** - Async MongoDB driver for Python
- **JWT** - Secure authentication and authorization
- **Pydantic** - Data validation and serialization

### AI/ML
- **NumPy** - Numerical computing for health calculations
- **Custom AI Models** - Health risk prediction algorithms
- **Nutrition AI** - Personalized meal planning system
- **Exercise AI** - Workout routine generation

### Frontend
- **HTML5/CSS3** - Modern, responsive web interface
- **JavaScript** - Dynamic client-side functionality
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Interactive data visualization

## 📋 Prerequisites

- **Python 3.8+**
- **MongoDB** (local installation or MongoDB Atlas)
- **pip** (Python package manager)
- **Web browser** (for frontend)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Navigate to project directory
cd "FINAL YEAR PROJECT 2"

# Install Python dependencies
cd healthnet-project/backend
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run MongoDB setup (if not already installed)
python setup_mongodb.py
```

### 3. Start the Application
```bash
# From project root directory
python start_healthnet.py
```

This will start:
- **Backend Server** on `http://localhost:8000`
- **Frontend** on `http://localhost:3000`
- **API Documentation** on `http://localhost:8000/docs`

## 📚 API Documentation

### Interactive API Docs
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Core Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

#### Health Assessment
- `POST /api/health/assessment` - Submit health data with AI predictions
- `GET /api/health/dashboard` - Get comprehensive health dashboard

#### Nutrition & Exercise
- `POST /api/nutrition/food` - Add food entry
- `GET /api/nutrition/food` - Get food entries
- `GET /api/nutrition/summary` - Get nutrition summary
- `POST /api/exercise` - Add exercise entry
- `GET /api/exercise` - Get exercise entries

#### AI-Powered Features
- `GET /api/ai/recommendations` - Get personalized health recommendations
- `GET /api/ai/nutrition-plan` - Get AI-generated nutrition plan
- `GET /api/ai/exercise-plan` - Get AI-generated exercise plan
- `GET /api/ai/health-analysis` - Get comprehensive AI health analysis

## 🏗️ Project Structure

```
📁 HealthNet Project/
├── 📁 frontend/
│   ├── 📄 home.html              # Landing page
│   ├── 📄 questionnaire.html     # Health assessment form
│   ├── 📄 dashboard.html         # Main dashboard
│   ├── 📄 ai-insights.html       # AI-powered insights
│   ├── 📄 food tracker.html      # Nutrition tracking
│   └── 📁 js/
│       └── 📄 health-api.js      # API client
├── 📁 healthnet-project/
│   ├── 📁 backend/
│   │   ├── 📄 main.py            # FastAPI application
│   │   ├── 📄 database.py        # MongoDB connection & models
│   │   ├── 📄 auth.py            # Authentication logic
│   │   ├── 📄 requirements.txt   # Python dependencies
│   │   ├── 📄 setup_mongodb.py   # MongoDB setup script
│   │   ├── 📄 MONGODB_SETUP.md   # MongoDB documentation
│   │   ├── 📄 README.md          # This file
│   │   └── 📁 ai/
│   │       ├── 📄 health_models.py    # Health risk prediction
│   │       ├── 📄 nutrition_ai.py     # Nutrition planning
│   │       └── 📄 exercise_ai.py      # Exercise routines
│   └── 📁 venv/                  # Python virtual environment
└── 📄 start_healthnet.py         # Application startup script
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/healthnet

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Testing the Application

### 1. User Registration & Login
1. Open `http://localhost:3000` in your browser
2. Click "Get Started" to register
3. Fill in your details and create an account
4. Login with your credentials

### 2. Health Assessment
1. Complete the health questionnaire
2. Submit your health data
3. View AI-generated health insights

### 3. AI Features
1. Navigate to "AI Insights" from the dashboard
2. Explore personalized nutrition plans
3. View custom exercise routines
4. Review health risk assessments

### 4. API Testing
```bash
# Health check
curl http://localhost:8000/

# Register user
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123"}'
```

## 🤖 AI Features Deep Dive

### Health Risk Models
- **Diabetes Risk Prediction** - Based on glucose levels, BMI, age, and lifestyle
- **Hypertension Risk Assessment** - Using blood pressure, age, and health factors
- **Heart Disease Risk Analysis** - Comprehensive cardiovascular health evaluation
- **Overall Health Score** - Combined health risk assessment

### Nutrition AI
- **Daily Calorie Calculation** - Personalized based on age, weight, activity level
- **Meal Plan Generation** - Breakfast, lunch, dinner, and snacks
- **Diet Type Determination** - Balanced, low-carb, high-protein, etc.
- **Nutritional Goals** - Protein, carbs, fats, vitamins, and minerals

### Exercise AI
- **Fitness Level Assessment** - Beginner, intermediate, advanced
- **Workout Plan Generation** - Weekly exercise routines
- **Exercise Focus Areas** - Cardio, strength, flexibility, balance
- **Safety Guidelines** - Injury prevention and proper form

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   ```bash
   # Ensure MongoDB is running
   # Windows: Check Services app for MongoDB
   # Or run: net start MongoDB
   ```

2. **Port Already in Use**
   ```bash
   # Change port in start_healthnet.py
   # Or kill existing process
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

3. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd "FINAL YEAR PROJECT 2"
   python start_healthnet.py
   ```

4. **Frontend Not Loading**
   - Ensure Live Server is running on port 5500
   - Check browser console for CORS errors
   - Verify backend is running on port 8000

### Debug Mode
- Check browser console (F12) for frontend errors
- Monitor terminal for backend logs
- Use API documentation at `/docs` for endpoint testing

## 🔮 Future Enhancements

- [ ] **Real-time Health Monitoring** - IoT device integration
- [ ] **Telemedicine Features** - Video consultations
- [ ] **Advanced AI Models** - Machine learning model training
- [ ] **Mobile App** - React Native or Flutter
- [ ] **Social Features** - Health challenges and communities
- [ ] **Integration APIs** - Fitness trackers, smart scales
- [ ] **Advanced Analytics** - Predictive health insights
- [ ] **Multi-language Support** - Internationalization

## 📞 Support & Documentation

- **API Documentation:** http://localhost:8000/docs
- **HealthNet Dashboard:** http://localhost:3000
- **MongoDB Setup:** See `MONGODB_SETUP.md`
- **Backend Logs:** Check terminal output

## 📄 License

This project is part of the HealthNet AI-Powered Preventive Healthcare platform.

---

**🏥 HealthNet - Empowering Health Through AI**
