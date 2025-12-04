// Authentication and Session Management
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.sessionToken = null;
        this.init();
    }

    init() {
        // Check for existing session
        const savedSession = localStorage.getItem('cabgo_session');
        if (savedSession) {
            try {
                const session = JSON.parse(savedSession);
                if (this.isValidSession(session)) {
                    this.currentUser = session.user;
                    this.sessionToken = session.token;
                    return true;
                }
            } catch (e) {
                localStorage.removeItem('cabgo_session');
            }
        }
        return false;
    }

    isValidSession(session) {
        if (!session.token || !session.user || !session.expiresAt) return false;
        return new Date().getTime() < session.expiresAt;
    }

    async login(email, password) {
        // Mock authentication for demo
        const mockUsers = [
            { id: 1, name: 'John Doe', email: 'john@example.com', password: '123456' },
            { id: 2, name: 'Jane Smith', email: 'jane@example.com', password: '123456' },
            { id: 3, name: 'Admin User', email: 'admin@cabgo.com', password: 'admin123' }
        ];
        
        const user = mockUsers.find(u => u.email === email && u.password === password);
        
        if (user) {
            this.currentUser = { id: user.id, name: user.name, email: user.email };
            this.sessionToken = 'mock_token_' + Date.now();
            
            // Save session
            const session = {
                user: this.currentUser,
                token: this.sessionToken,
                expiresAt: new Date().getTime() + (24 * 60 * 60 * 1000) // 24 hours
            };
            localStorage.setItem('cabgo_session', JSON.stringify(session));
            
            return { success: true, user: this.currentUser };
        } else {
            return { success: false, message: 'Invalid email or password' };
        }
    }

    async register(userData) {
        // Mock registration for demo
        if (userData.email && userData.password && userData.name && userData.phone) {
            return { success: true, message: 'Registration successful' };
        } else {
            return { success: false, message: 'Please fill all fields' };
        }
    }

    logout() {
        this.currentUser = null;
        this.sessionToken = null;
        localStorage.removeItem('cabgo_session');
        window.location.reload();
    }

    isLoggedIn() {
        return this.currentUser !== null && this.sessionToken !== null;
    }

    getAuthHeaders() {
        return {
            'Authorization': `Bearer ${this.sessionToken}`,
            'Content-Type': 'application/json'
        };
    }

    requireAuth() {
        if (!this.isLoggedIn()) {
            this.showLoginModal();
            return false;
        }
        return true;
    }

    showLoginModal() {
        document.getElementById('loginModal').style.display = 'flex';
    }

    hideLoginModal() {
        document.getElementById('loginModal').style.display = 'none';
    }
}

// Initialize auth manager
const authManager = new AuthManager();

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!authManager.isLoggedIn()) {
        authManager.showLoginModal();
    } else {
        initializeApp();
    }
});