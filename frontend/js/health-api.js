// HealthNet API Client
class HealthNetAPI {
    constructor(baseURL = '') {
        // No default backend; endpoints must be provided by your real API
        this.baseURL = baseURL;
        this.token = localStorage.getItem('healthnet_token');
    }

    // Set authentication token
    setToken(token) {
        this.token = token;
        localStorage.setItem('healthnet_token', token);
    }

    // Clear authentication token
    clearToken() {
        this.token = null;
        localStorage.removeItem('healthnet_token');
    }

    // Get headers for API requests
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // Generic API request method
    async makeRequest(endpoint, options = {}) {
        if (!this.baseURL) {
            throw new Error('No API baseURL configured. Connect to a real backend.');
        }
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }



    // Authentication endpoints
    async register(userData) {
        return this.makeRequest('/api/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async login(credentials) {
        const response = await this.makeRequest('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
        
        if (response.access_token) {
            this.setToken(response.access_token);
        }
        
        return response;
    }

    async logout() {
        try {
            await this.makeRequest('/api/auth/logout', {
                method: 'POST'
            });
        } finally {
            this.clearToken();
        }
    }

    // Health assessment endpoints
    async submitHealthAssessment(healthData) {
        return this.makeRequest('/api/health/assessment', {
            method: 'POST',
            body: JSON.stringify(healthData)
        });
    }

    async getHealthDashboard() {
        return this.makeRequest('/api/health/dashboard');
    }

    // Nutrition endpoints
    async addFoodEntry(foodData) {
        return this.makeRequest('/api/nutrition/food', {
            method: 'POST',
            body: JSON.stringify(foodData)
        });
    }

    async getFoodEntries(date = null) {
        const endpoint = date ? `/api/nutrition/food?date=${date}` : '/api/nutrition/food';
        return this.makeRequest(endpoint);
    }

    async getNutritionSummary(date = null) {
        const endpoint = date ? `/api/nutrition/summary?date=${date}` : '/api/nutrition/summary';
        return this.makeRequest(endpoint);
    }

    // Exercise endpoints
    async addExerciseEntry(exerciseData) {
        return this.makeRequest('/api/exercise/entry', {
            method: 'POST',
            body: JSON.stringify(exerciseData)
        });
    }

    async getExerciseEntries(date = null) {
        const endpoint = date ? `/api/exercise/entries?date=${date}` : '/api/exercise/entries';
        return this.makeRequest(endpoint);
    }

    // AI recommendations
    async getAIRecommendations() {
        return this.makeRequest('/api/ai/recommendations');
    }

    // Health check
    async healthCheck() {
        return this.makeRequest('/');
    }
}

// Global API instance
const healthAPI = new HealthNetAPI();

// Utility functions for frontend integration
class HealthNetUI {
    constructor() {
        this.api = healthAPI;
        this.currentUser = null;
        this.init();
    }

    init() {
        this.checkAuthStatus();
        this.setupEventListeners();
    }

    checkAuthStatus() {
        // Early development: bypass auth gating and show UI
        this.showAuthenticatedUI();
    }

    showLoginUI() {
        const userSection = document.getElementById('userSection');
        const loginBtn = document.getElementById('loginBtn');
        
        if (userSection) userSection.classList.add('hidden');
        if (loginBtn) loginBtn.classList.remove('hidden');
    }

    showAuthenticatedUI() {
        const userSection = document.getElementById('userSection');
        const loginBtn = document.getElementById('loginBtn');
        
        if (userSection) userSection.classList.remove('hidden');
        if (loginBtn) loginBtn.classList.add('hidden');
    }

    setupEventListeners() {
        // Login form submission
        const signInBtn = document.getElementById('signInBtn');
        if (signInBtn) {
            signInBtn.addEventListener('click', () => this.handleLogin());
        }

        // Logout button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.handleLogout());
        }

        // Registration form (if exists)
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }
    }

    async handleLogin() {
        // Early development: simulate successful login without backend
        const nameInput = document.getElementById('name');
        const name = nameInput && nameInput.value ? nameInput.value : 'User';
        this.api.setToken('dev-token');
        this.currentUser = { name };
        this.showAuthenticatedUI();
        this.updateUserName(name);
        this.closeLoginModal();
        this.showNotification('Login successful! (dev mode)', 'success');
    }

    async handleLogout() {
        try {
            // In dev, just clear token/UI
            this.api.clearToken();
            this.currentUser = null;
            this.showLoginUI();
            this.showNotification('Logged out (dev mode)', 'success');
        } catch (error) {
            this.showNotification('Logout failed: ' + error.message, 'error');
        }
    }

    async handleRegister(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const userData = {
            email: formData.get('email'),
            password: formData.get('password'),
            name: formData.get('name'),
            age: parseInt(formData.get('age')),
            gender: formData.get('gender'),
            phone: formData.get('phone')
        };

        try {
            await this.api.register(userData);
            this.showNotification('Registration successful! Please log in.', 'success');
        } catch (error) {
            this.showNotification('Registration failed: ' + error.message, 'error');
        }
    }

    updateUserName(name) {
        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = name;
        }
    }

    closeLoginModal() {
        const loginModal = document.getElementById('loginModal');
        if (loginModal) {
            loginModal.classList.add('hidden');
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'error' ? 'bg-red-500 text-white' :
            'bg-blue-500 text-white'
        }`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Health assessment form submission
    async submitHealthAssessment(formData) {
        try {
            const response = await this.api.submitHealthAssessment(formData);
            this.showNotification('Health assessment submitted successfully!', 'success');
            return response;
        } catch (error) {
            this.showNotification('Failed to submit health assessment: ' + error.message, 'error');
            throw error;
        }
    }

    // Food tracking
    async addFoodEntry(foodData) {
        try {
            const response = await this.api.addFoodEntry(foodData);
            this.showNotification('Food entry added successfully!', 'success');
            return response;
        } catch (error) {
            this.showNotification('Failed to add food entry: ' + error.message, 'error');
            throw error;
        }
    }

    // Exercise tracking
    async addExerciseEntry(exerciseData) {
        try {
            const response = await this.api.addExerciseEntry(exerciseData);
            this.showNotification('Exercise entry added successfully!', 'success');
            return response;
        } catch (error) {
            this.showNotification('Failed to add exercise entry: ' + error.message, 'error');
            throw error;
        }
    }

    // Get dashboard data
    async loadDashboardData() {
        try {
            const dashboardData = await this.api.getHealthDashboard();
            this.updateDashboardUI(dashboardData);
            return dashboardData;
        } catch (error) {
            this.showNotification('Failed to load dashboard data: ' + error.message, 'error');
            throw error;
        }
    }

    updateDashboardUI(data) {
        // Update health metrics
        if (data.latest_health_data) {
            const healthData = data.latest_health_data;
            
            // Update heart rate
            const heartRateElement = document.querySelector('[data-metric="heart-rate"]');
            if (heartRateElement && healthData.heart_rate) {
                heartRateElement.textContent = healthData.heart_rate;
            }

            // Update blood glucose
            const glucoseElement = document.querySelector('[data-metric="glucose"]');
            if (glucoseElement && healthData.avg_glucose_level) {
                glucoseElement.textContent = Math.round(healthData.avg_glucose_level);
            }

            // Update blood pressure
            const bpElement = document.querySelector('[data-metric="blood-pressure"]');
            if (bpElement && healthData.blood_pressure_systolic && healthData.blood_pressure_diastolic) {
                bpElement.textContent = `${healthData.blood_pressure_systolic}/${healthData.blood_pressure_diastolic}`;
            }
        }

        // Update predictions
        if (data.predictions) {
            const predictions = data.predictions;
            
            // Update risk indicators
            const diabetesRiskElement = document.querySelector('[data-risk="diabetes"]');
            if (diabetesRiskElement) {
                const risk = predictions.diabetes_risk || 0;
                diabetesRiskElement.textContent = `${(risk * 100).toFixed(1)}%`;
                diabetesRiskElement.className = risk > 0.6 ? 'text-red-600' : risk > 0.3 ? 'text-yellow-600' : 'text-green-600';
            }

            const hypertensionRiskElement = document.querySelector('[data-risk="hypertension"]');
            if (hypertensionRiskElement) {
                const risk = predictions.hypertension_risk || 0;
                hypertensionRiskElement.textContent = `${(risk * 100).toFixed(1)}%`;
                hypertensionRiskElement.className = risk > 0.6 ? 'text-red-600' : risk > 0.3 ? 'text-yellow-600' : 'text-green-600';
            }

            // Update health score
            const healthScoreElement = document.querySelector('[data-metric="health-score"]');
            if (healthScoreElement && predictions.overall_health_score) {
                healthScoreElement.textContent = predictions.overall_health_score;
            }
        }
    }
}

// Initialize UI when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.healthNetUI = new HealthNetUI();
});

// Export for use in other scripts
window.HealthNetAPI = HealthNetAPI;
window.healthAPI = healthAPI;
