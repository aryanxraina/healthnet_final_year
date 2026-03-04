// Unified Navigation and AI Assistant System
class UnifiedNavigation {
    constructor() {
        this.currentUser = null;
        this.aiAssistantOpen = false;

        this.init();
    }

    async init() {
        await this.checkAuthStatus();
        this.setupNavigation();
        this.setupSearch();
        this.setupAIAssistant();
        this.updateUserInfo();
    }

    async checkAuthStatus() {
        try {
            // Early development: do not gate navigation by auth
            this.currentUser = { name: 'User' };
            return;
        } catch (error) {
            // No-op in dev
        }
    }

    setupNavigation() {
        // Create unified navigation bar
        const navHTML = `
            <nav class="bg-white/90 backdrop-blur-md shadow-sm border-b border-gray-100 fixed w-full top-0 z-50 transition-all duration-300">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center h-20">
                        
                        <!-- Left Section: Logo & Nav Links -->
                        <div class="flex items-center space-x-8">
                            <!-- Logo -->
                            <a href="index.html" class="flex-shrink-0 flex items-center group">
                                <div class="bg-teal-50 p-2 rounded-lg group-hover:bg-teal-100 transition-colors duration-200">
                                    <svg class="h-8 w-8 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                    </svg>
                                </div>
                                <span class="ml-3 text-xl font-bold text-gray-900 tracking-tight">HealthNet</span>
                            </a>

                            <!-- Desktop Navigation Links -->
                            <div class="hidden md:flex items-center space-x-1">
                                <a href="index.html" class="nav-link" data-page="dashboard">
                                    Dashboard
                                </a>
                                <a href="questionnaire.html" class="nav-link" data-page="questionnaire">
                                    Assessment
                                </a>
                                <a href="ai-scan.html" class="nav-link" data-page="ai-scan">
                                    AI Scan
                                </a>
                                <a href="food%20tracker.html" class="nav-link" data-page="food-tracker">
                                    Food
                                </a>
                                <a href="ocr.html" class="nav-link" data-page="ocr">
                                    OCR
                                </a>
                            </div>
                        </div>

                        <!-- Right Section: Search & Profile -->
                        <div class="hidden md:flex items-center space-x-6">
                            <!-- Search Bar -->
                            <div class="relative group">
                                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <i class="fas fa-search text-gray-400 group-focus-within:text-teal-500 transition-colors"></i>
                                </div>
                                <input type="text" id="global-search" 
                                    class="block w-64 pl-10 pr-4 py-2 border border-gray-200 rounded-full leading-5 bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:bg-white focus:border-teal-500 focus:ring-2 focus:ring-teal-100 sm:text-sm transition-all duration-200 ease-in-out hover:bg-white hover:border-gray-300" 
                                    placeholder="Search features...">
                                <div id="search-results" class="hidden absolute mt-2 w-72 right-0 bg-white shadow-xl rounded-xl py-2 z-50 border border-gray-100 max-h-80 overflow-auto">
                                </div>
                            </div>

                            <!-- User Menu -->
                            <div class="relative ml-4">
                                <button id="user-menu-button" class="flex items-center space-x-3 focus:outline-none group">
                                    <div class="text-right hidden lg:block">
                                        <p class="text-sm font-medium text-gray-900" id="user-name">User</p>
                                        <p class="text-xs text-gray-500">Member</p>
                                    </div>
                                    <div class="h-10 w-10 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-200 ring-2 ring-white">
                                        <span class="text-white font-semibold text-lg" id="user-initial">U</span>
                                    </div>
                                </button>
                                <div id="user-menu" class="hidden absolute right-0 mt-3 w-56 bg-white rounded-xl shadow-xl py-2 z-50 border border-gray-100 transform origin-top-right transition-all duration-200">
                                    <div class="px-4 py-3 border-b border-gray-50">
                                        <p class="text-sm text-gray-900 font-medium">Signed in as</p>
                                        <p class="text-sm text-gray-500 truncate" id="user-email">user@healthnet.com</p>
                                    </div>
                                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-700 transition-colors">
                                        <i class="fas fa-user-circle mr-2 text-gray-400"></i>Profile
                                    </a>
                                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-teal-50 hover:text-teal-700 transition-colors">
                                        <i class="fas fa-cog mr-2 text-gray-400"></i>Settings
                                    </a>
                                    <div class="border-t border-gray-50 my-1"></div>
                                    <a href="#" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 hover:text-red-700 transition-colors" onclick="unifiedNav.logout()">
                                        <i class="fas fa-sign-out-alt mr-2"></i>Logout
                                    </a>
                                </div>
                            </div>
                        </div>

                        <!-- Mobile menu button -->
                        <div class="md:hidden flex items-center">
                            <button id="mobile-menu-button" class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-teal-500">
                                <i class="fas fa-bars text-xl"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Mobile Navigation -->
                <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-gray-100 shadow-lg">
                    <div class="px-4 pt-4 pb-4 space-y-2">
                        <!-- Mobile Search -->
                        <div class="mb-4">
                            <div class="relative">
                                <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <i class="fas fa-search text-gray-400"></i>
                                </span>
                                <input type="text" id="mobile-search-input" 
                                    class="block w-full pl-10 pr-3 py-2 border border-gray-200 rounded-lg leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:bg-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500 sm:text-sm" 
                                    placeholder="Search features...">
                                <div id="mobile-search-results" class="hidden mt-1 w-full bg-white shadow-lg rounded-md py-1 border border-gray-200"></div>
                            </div>
                        </div>
                        
                        <a href="index.html" class="mobile-nav-link" data-page="dashboard">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center mr-3 text-teal-600">
                                    <i class="fas fa-chart-line text-sm"></i>
                                </div>
                                <span class="font-medium">Dashboard</span>
                            </div>
                        </a>
                        <a href="questionnaire.html" class="mobile-nav-link" data-page="questionnaire">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center mr-3 text-teal-600">
                                    <i class="fas fa-clipboard-list text-sm"></i>
                                </div>
                                <span class="font-medium">Health Assessment</span>
                            </div>
                        </a>
                        <a href="ai-scan.html" class="mobile-nav-link" data-page="ai-scan">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center mr-3 text-teal-600">
                                    <i class="fas fa-brain text-sm"></i>
                                </div>
                                <span class="font-medium">AI Health Scan</span>
                            </div>
                        </a>
                        <a href="food%20tracker.html" class="mobile-nav-link" data-page="food-tracker">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center mr-3 text-teal-600">
                                    <i class="fas fa-utensils text-sm"></i>
                                </div>
                                <span class="font-medium">Food Tracker</span>
                            </div>
                        </a>
                        <a href="ocr.html" class="mobile-nav-link" data-page="ocr">
                            <div class="flex items-center">
                                <div class="w-8 h-8 rounded-full bg-teal-50 flex items-center justify-center mr-3 text-teal-600">
                                    <i class="fas fa-file-prescription text-sm"></i>
                                </div>
                                <span class="font-medium">Prescription OCR</span>
                            </div>
                        </a>
                        
                        <div class="border-t border-gray-100 my-2 pt-2">
                             <a href="#" class="mobile-nav-link text-red-600" onclick="unifiedNav.logout()">
                                <div class="flex items-center">
                                    <div class="w-8 h-8 rounded-full bg-red-50 flex items-center justify-center mr-3 text-red-600">
                                        <i class="fas fa-sign-out-alt text-sm"></i>
                                    </div>
                                    <span class="font-medium">Logout</span>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
            <!-- Spacer for fixed nav -->
            <div class="h-20"></div>
        `;

        // Insert navigation at the top of the body
        document.body.insertAdjacentHTML('afterbegin', navHTML);

        // Add event listeners
        this.setupNavigationEvents();
        this.highlightCurrentPage();
    }

    setupSearch() {
        const searchIndex = [
            { title: 'Dashboard', url: 'index.html', icon: 'fa-chart-line', keywords: 'home, stats, overview, analytics' },
            { title: 'Health Assessment', url: 'questionnaire.html', icon: 'fa-clipboard-list', keywords: 'questionnaire, survey, health check, assessment' },
            { title: 'AI Health Scan', url: 'ai-scan.html', icon: 'fa-brain', keywords: 'ai, scan, diagnosis, symptoms, doctor' },
            { title: 'Food Tracker', url: 'food%20tracker.html', icon: 'fa-utensils', keywords: 'diet, calories, nutrition, food, log, meal' },
            { title: 'Prescription OCR', url: 'ocr.html', icon: 'fa-file-prescription', keywords: 'ocr, prescription, scan, medicine, text' },
            { title: 'AI Insights', url: 'ai-insights.html', icon: 'fa-lightbulb', keywords: 'insights, analysis, reports, ai, health data' },
            { title: 'AI Assistant', action: 'toggle-ai', icon: 'fa-robot', keywords: 'chat, help, bot, assistant' }
        ];

        const handleSearch = (input, resultsContainer) => {
            const query = input.value.toLowerCase().trim();
            if (!query) {
                resultsContainer.classList.add('hidden');
                return;
            }

            const results = searchIndex.filter(item =>
                item.title.toLowerCase().includes(query) ||
                item.keywords.includes(query)
            );

            resultsContainer.innerHTML = '';

            if (results.length > 0) {
                results.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'px-4 py-2 hover:bg-teal-50 cursor-pointer flex items-center transition-colors duration-150';
                    div.innerHTML = `
                        <div class="flex-shrink-0 w-8">
                            <i class="fas ${item.icon} text-teal-600"></i>
                        </div>
                        <div class="text-sm font-medium text-gray-900">${item.title}</div>
                    `;
                    div.addEventListener('click', () => {
                        if (item.url) {
                            window.location.href = item.url;
                        } else if (item.action === 'toggle-ai') {
                            const chatButton = document.getElementById('ai-chat-button');
                            if (chatButton) chatButton.click();
                        }
                        resultsContainer.classList.add('hidden');
                        input.value = '';
                    });
                    resultsContainer.appendChild(div);
                });
                resultsContainer.classList.remove('hidden');
            } else {
                resultsContainer.innerHTML = '<div class="px-4 py-2 text-sm text-gray-500">No results found</div>';
                resultsContainer.classList.remove('hidden');
            }
        };

        // Desktop Search
        const globalSearch = document.getElementById('global-search');
        const searchResults = document.getElementById('search-results');

        if (globalSearch && searchResults) {
            globalSearch.addEventListener('input', () => handleSearch(globalSearch, searchResults));
            globalSearch.addEventListener('focus', () => handleSearch(globalSearch, searchResults));

            // Close on click outside
            document.addEventListener('click', (e) => {
                if (!globalSearch.contains(e.target) && !searchResults.contains(e.target)) {
                    searchResults.classList.add('hidden');
                }
            });
        }

        // Mobile Search
        const mobileSearch = document.getElementById('mobile-search-input');
        const mobileSearchResults = document.getElementById('mobile-search-results');

        if (mobileSearch && mobileSearchResults) {
            mobileSearch.addEventListener('input', () => handleSearch(mobileSearch, mobileSearchResults));
            mobileSearch.addEventListener('focus', () => handleSearch(mobileSearch, mobileSearchResults));
        }
    }

    setupNavigationEvents() {
        // User menu toggle
        const userMenuButton = document.getElementById('user-menu-button');
        const userMenu = document.getElementById('user-menu');

        userMenuButton?.addEventListener('click', () => {
            userMenu.classList.toggle('hidden');
        });

        // Close user menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!userMenuButton?.contains(e.target) && !userMenu?.contains(e.target)) {
                userMenu?.classList.add('hidden');
            }
        });

        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');

        mobileMenuButton?.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Navigation link hover effects
        document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
            link.addEventListener('mouseenter', () => {
                link.classList.add('text-teal-600', 'bg-teal-50');
            });
            link.addEventListener('mouseleave', () => {
                link.classList.remove('text-teal-600', 'bg-teal-50');
            });
        });
    }

    highlightCurrentPage() {
        const currentPage = this.getCurrentPage();
        document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
            if (link.getAttribute('data-page') === currentPage) {
                link.classList.add('text-teal-600', 'font-semibold');
            }
        });
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('dashboard')) return 'dashboard';
        if (path.includes('questionnaire')) return 'questionnaire';
        if (path.includes('food')) return 'food-tracker';
        if (path.includes('ai-insights')) return 'ai-insights';
        return 'dashboard';
    }

    updateUserInfo() {
        if (this.currentUser) {
            const userName = document.getElementById('user-name');
            const userInitial = document.getElementById('user-initial');

            if (userName) userName.textContent = this.currentUser.name || 'User';
            if (userInitial) userInitial.textContent = (this.currentUser.name || 'U').charAt(0).toUpperCase();
        }
    }

    setupAIAssistant() {
        // Create AI Assistant Chatbot
        const aiAssistantHTML = `
            <!-- AI Assistant Chatbot -->
            <div id="ai-assistant-container" class="fixed bottom-6 right-6 z-50">
                <!-- Chat Button -->
                <button id="ai-chat-button" class="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full p-4 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
                    <i class="fas fa-robot text-2xl"></i>
                </button>

                <!-- Chat Window -->
                <div id="ai-chat-window" class="hidden absolute bottom-16 right-0 w-96 h-[500px] bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col">
                    <!-- Chat Header -->
                    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-t-lg">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <i class="fas fa-robot text-xl mr-3"></i>
                                <div>
                                    <h3 class="font-semibold">HealthNet AI Assistant</h3>
                                    <p class="text-sm text-blue-100">Your Personal Health Guide</p>
                                </div>
                            </div>
                            <button id="ai-chat-close" class="text-white hover:text-blue-200">
                                <i class="fas fa-times text-lg"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Chat Messages -->
                    <div id="ai-chat-messages" class="flex-1 p-4 overflow-y-auto space-y-4">
                        <!-- Welcome message -->
                        <div class="flex items-start space-x-3">
                            <div class="flex-shrink-0">
                                <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                    <i class="fas fa-robot text-white text-sm"></i>
                                </div>
                            </div>
                            <div class="bg-blue-50 rounded-lg p-3 max-w-xs">
                                <p class="text-sm text-gray-800">
                                    Hello! I'm your HealthNet AI assistant. I can help you with health advice, nutrition tips, exercise recommendations, and answer any health-related questions. How can I assist you today?
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Chat Input -->
                    <div class="p-4 border-t border-gray-200">
                        <div class="flex space-x-2">
                            <input type="text" id="ai-chat-input" placeholder="Ask me anything about your health..." 
                                   class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            <button id="ai-chat-send" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', aiAssistantHTML);
        this.setupAIAssistantEvents();
    }

    setupAIAssistantEvents() {
        const chatButton = document.getElementById('ai-chat-button');
        const chatWindow = document.getElementById('ai-chat-window');
        const chatClose = document.getElementById('ai-chat-close');
        const chatInput = document.getElementById('ai-chat-input');
        const chatSend = document.getElementById('ai-chat-send');
        const chatMessages = document.getElementById('ai-chat-messages');

        // Toggle chat window
        chatButton?.addEventListener('click', () => {
            chatWindow.classList.toggle('hidden');
            if (!chatWindow.classList.contains('hidden')) {
                chatInput.focus();
            }
        });

        chatClose?.addEventListener('click', () => {
            chatWindow.classList.add('hidden');
        });

        // Send message
        const sendMessage = async () => {
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            this.addChatMessage(message, 'user');
            chatInput.value = '';

            // Show typing indicator
            this.showTypingIndicator();

            try {
                const response = await this.sendToAIAssistant(message);
                this.hideTypingIndicator();
                this.addChatMessage(response.response, 'assistant');
            } catch (error) {
                this.hideTypingIndicator();
                this.addChatMessage('Sorry, I encountered an error. Please try again.', 'assistant');
            }
        };

        chatSend?.addEventListener('click', sendMessage);
        chatInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    addChatMessage(message, sender) {
        const chatMessages = document.getElementById('ai-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start space-x-3';

        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="flex-1"></div>
                <div class="bg-blue-600 text-white rounded-lg p-3 max-w-xs">
                    <p class="text-sm">${message}</p>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                        <i class="fas fa-robot text-white text-sm"></i>
                    </div>
                </div>
                <div class="bg-blue-50 rounded-lg p-3 max-w-xs">
                    <p class="text-sm text-gray-800">${message}</p>
                </div>
            `;
        }

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('ai-chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'flex items-start space-x-3';
        typingDiv.innerHTML = `
            <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <i class="fas fa-robot text-white text-sm"></i>
                </div>
            </div>
            <div class="bg-blue-50 rounded-lg p-3">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async sendToAIAssistant(message) {
        const token = localStorage.getItem('token');
        if (!window.healthAPI?.baseURL) {
            // Dev fallback: return a mock response when backend is not configured
            return {
                response: `Dev assistant: I received your message: "${message}". In production, I'll provide personalized health insights here.`,
                intent: { intent: 'general_health', confidence: 0.5 },
                sentiment: { sentiment: 'neutral', score: 0 },
                personalized: false,
                confidence: 0.5,
                suggestions: [
                    'Explore the dashboard',
                    'Try the questionnaire',
                    'Open AI Insights'
                ],
                timestamp: new Date().toISOString()
            }
        }
        const response = await fetch(`${window.healthAPI.baseURL}/api/ai/assistant/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error('Failed to get AI response');
        }

        return await response.json();
    }

    logout() {
        localStorage.removeItem('token');
        window.location.href = 'index.html';
    }
}

// Initialize unified navigation
// Initialize unified navigation
document.addEventListener('DOMContentLoaded', () => {
    const unifiedNav = new UnifiedNavigation();
});

// Add CSS styles
const navStyles = `
<style>
    .nav-link {
        @apply text-gray-500 hover:text-teal-600 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 hover:bg-teal-50;
    }
    
    .nav-link.active {
        @apply text-teal-700 bg-teal-50 font-semibold shadow-sm ring-1 ring-teal-100;
    }
    
    .mobile-nav-link {
        @apply block w-full text-left px-4 py-3 rounded-xl text-gray-600 hover:bg-teal-50 hover:text-teal-700 transition-all duration-200;
    }

    .mobile-nav-link.active {
        @apply bg-teal-50 text-teal-700 font-semibold ring-1 ring-teal-100;
    }
    
    /* Smooth transitions */
    nav {
        transition: all 0.3s ease-in-out;
    }

    /* Search Input Focus Animation */
    #global-search:focus {
        width: 20rem;
    }

    /* Custom Scrollbar for Search Results */
    #search-results::-webkit-scrollbar {
        width: 6px;
    }
    #search-results::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    #search-results::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    #search-results::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    #ai-assistant-container {
        transition: all 0.3s ease;
    }
    
    #ai-chat-button {
        transition: all 0.3s ease;
    }
    
    #ai-chat-button:hover {
        transform: scale(1.1);
    }
    
    #ai-chat-window {
        transition: all 0.3s ease;
    }
    
    .chat-message {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
`;

document.head.insertAdjacentHTML('beforeend', navStyles);
