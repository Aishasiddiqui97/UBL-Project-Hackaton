// API Configuration for Django Backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// API Service Class
class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.isRefreshing = false;
    this.refreshQueue = [];
  }

  // Helper method to get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    const headers = {
      'Content-Type': 'application/json'
    };
    
    // Only add auth header if we have a valid token and we're not on login endpoint
    if (token && token !== 'undefined' && token !== 'null') {
      headers.Authorization = `Bearer ${token}`;
    }
    
    return headers;
  }

  // Save auth data
  saveAuth(accessToken, refreshToken, user) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('isAuthenticated', 'true');
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    }
  }

  // Clear auth data
  clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('user');
  }

  // Refresh token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch(`${this.baseURL}/auth/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (!response.ok) {
        throw new Error('Token refresh failed');
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      if (data.refresh) {
        localStorage.setItem('refresh_token', data.refresh);
      }
      return data;
    } catch (error) {
      this.clearAuth();
      throw error;
    }
  }

  // Generic API call method with automatic token refresh
  async apiCall(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    console.log('API Call:', { url, method: options.method || 'GET', headers: config.headers });

    try {
      const response = await fetch(url, config);
      
      // Check content type before parsing JSON
      const contentType = response.headers.get('content-type');
      
      if (!contentType || !contentType.includes('application/json')) {
        console.error('Backend returned non-JSON response:', contentType);
        throw new Error('Backend server error. Expected JSON but got ' + (contentType || 'unknown'));
      }
      
      // If 401, try to refresh token
      if (response.status === 401 && !endpoint.includes('/auth/')) {
        if (!this.isRefreshing) {
          this.isRefreshing = true;
          try {
            await this.refreshToken();
            // Retry the original request
            config.headers = this.getAuthHeaders();
            const retryResponse = await fetch(url, config);
            
            // Check content type for retry
            const retryContentType = retryResponse.headers.get('content-type');
            if (!retryContentType || !retryContentType.includes('application/json')) {
              throw new Error('Backend server error on retry');
            }
            
            const retryData = await retryResponse.json();
            
            if (!retryResponse.ok) {
              const errorMessage = retryData.message || retryData.detail || `HTTP error! status: ${retryResponse.status}`;
              throw new Error(errorMessage);
            }
            
            return retryData.data ? retryData : retryData;
          } finally {
            this.isRefreshing = false;
          }
        }
      }

      const data = await response.json();

      console.log('API Response:', { status: response.status, data });

      if (!response.ok) {
        const errorMessage = data.message || data.detail || data.errors || `HTTP error! status: ${response.status}`;
        console.error('API Error:', errorMessage);
        throw new Error(errorMessage);
      }

      // Django wraps responses in {success, message, data} - return just data for easier access
      return data.data ? data : data;
    } catch (error) {
      console.error('API call failed:', error);
      // Better error message for JSON parse errors
      if (error.message.includes('JSON') || error.message.includes('Unexpected token')) {
        throw new Error('Backend error: Server returned invalid response. Check if Django is running.');
      }
      throw error;
    }
  }

  // Authentication endpoints
  async login(email, password) {
    // Don't use auth headers for login
    const url = `${this.baseURL}/auth/login/`;
    const config = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    };

    console.log('Login API Call:', { url, email });

    try {
      const response = await fetch(url, config);
      
      // Check content type to avoid JSON parse error on HTML responses
      const contentType = response.headers.get('content-type');
      console.log('Response content-type:', contentType, 'Status:', response.status);
      
      if (!contentType || !contentType.includes('application/json')) {
        // Backend returned HTML instead of JSON (error page)
        console.error('Backend returned non-JSON response. Backend may be down or URL is wrong.');
        throw new Error('Backend server error. Please check if backend is running on port 8000.');
      }

      const data = await response.json();
      console.log('Login API Response:', { status: response.status, data });

      if (!response.ok) {
        const errorMessage = data.message || data.detail || data.errors || `HTTP error! status: ${response.status}`;
        console.error('Login API Error:', errorMessage);
        throw new Error(errorMessage);
      }

      // Return full response since LoginForm expects response.data structure
      return { data: data.data || data };
    } catch (error) {
      console.error('Login API call failed:', error);
      // If it's a JSON parse error, give a clearer message
      if (error.message.includes('JSON') || error.message.includes('Unexpected token')) {
        throw new Error('Backend is not responding correctly. Please ensure Django server is running on http://localhost:8000');
      }
      throw error;
    }
  }

  async logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    try {
      await this.apiCall('/auth/logout/', {
        method: 'POST',
        body: JSON.stringify({ refresh_token: refreshToken })
      });
    } finally {
      this.clearAuth();
    }
  }

  // User endpoints
  async getCurrentUser() {
    return this.apiCall('/users/me/');
  }

  // Products endpoints
  async getProducts() {
    return this.apiCall('/products/');
  }

  async createProduct(productData) {
    return this.apiCall('/products/', {
      method: 'POST',
      body: JSON.stringify(productData)
    });
  }

  // Orders endpoints  
  async getOrders() {
    return this.apiCall('/orders/');
  }

  async createOrder(orderData) {
    return this.apiCall('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData)
    });
  }

  async getOrder(orderId) {
    return this.apiCall(`/orders/${orderId}/`);
  }

  // Transactions endpoints
  async getTransactions() {
    return this.apiCall('/transactions/');
  }

  async getTransaction(transactionId) {
    return this.apiCall(`/transactions/${transactionId}/`);
  }
  
  async createTransaction(transactionData) {
    return this.apiCall('/transactions/', {
      method: 'POST',
      body: JSON.stringify(transactionData)
    });
  }
  
  async getSuspiciousTransactions() {
    return this.apiCall('/transactions/suspicious/');
  }
  
  async getFraudStats() {
    return this.apiCall('/transactions/fraud_stats/');
  }
  
  async reviewFraudTransaction(transactionId, status) {
    return this.apiCall(`/transactions/${transactionId}/review_fraud/`, {
      method: 'POST',
      body: JSON.stringify({ status })
    });
  }
  
  // Analyze transaction for fraud using ML
  async analyzeTransaction(transactionData) {
    return this.apiCall('/transactions/analyze/', {
      method: 'POST',
      body: JSON.stringify(transactionData)
    });
  }
  
  // Fraud Detection endpoints
  async getFraudAlerts() {
    return this.apiCall('/transactions/fraud-alerts/');
  }
  
  async resolveFraudAlert(alertId) {
    return this.apiCall(`/transactions/fraud-alerts/${alertId}/resolve/`, {
      method: 'POST'
    });
  }

  // Payments endpoints
  async getPayments() {
    return this.apiCall('/payments/');
  }

  async createPayment(paymentData) {
    return this.apiCall('/payments/', {
      method: 'POST',
      body: JSON.stringify(paymentData)
    });
  }

  // Notifications endpoints
  async getNotifications() {
    return this.apiCall('/notifications/');
  }

  async markNotificationRead(notificationId) {
    return this.apiCall(`/notifications/${notificationId}/mark_read/`, {
      method: 'POST'
    });
  }

  // Cases endpoints
  async getCases() {
    return this.apiCall('/cases/');
  }

  async getCase(caseId) {
    return this.apiCall(`/cases/${caseId}/`);
  }

  async createCase(caseData) {
    return this.apiCall('/cases/', {
      method: 'POST',
      body: JSON.stringify(caseData)
    });
  }

  async updateCase(caseId, caseData) {
    return this.apiCall(`/cases/${caseId}/`, {
      method: 'PATCH',
      body: JSON.stringify(caseData)
    });
  }

  async assignCase(caseId, userId) {
    return this.apiCall(`/cases/${caseId}/assign/`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId })
    });
  }

  async updateCaseStatus(caseId, status, resolution = '') {
    return this.apiCall(`/cases/${caseId}/update_status/`, {
      method: 'POST',
      body: JSON.stringify({ status, resolution })
    });
  }

  async addCaseComment(caseId, content) {
    return this.apiCall(`/cases/${caseId}/add_comment/`, {
      method: 'POST',
      body: JSON.stringify({ content })
    });
  }

  async getCaseStats() {
    return this.apiCall('/cases/stats/');
  }

  async getMyCases() {
    return this.apiCall('/cases/my_cases/');
  }

  // KYC endpoints
  async getKYCProfiles() {
    return this.apiCall('/kyc/profiles/');
  }

  async getKYCProfile(profileId) {
    return this.apiCall(`/kyc/profiles/${profileId}/`);
  }

  async createKYCProfile(profileData) {
    return this.apiCall('/kyc/profiles/', {
      method: 'POST',
      body: JSON.stringify(profileData)
    });
  }

  async reviewKYCProfile(profileId, reviewData) {
    return this.apiCall(`/kyc/profiles/${profileId}/review/`, {
      method: 'POST',
      body: JSON.stringify(reviewData)
    });
  }

  async getKYCStats() {
    return this.apiCall('/kyc/profiles/stats/');
  }

  async getMyKYC() {
    return this.apiCall('/kyc/profiles/my_kyc/');
  }

  // Compliance endpoints
  async getComplianceRules() {
    return this.apiCall('/compliance/rules/');
  }

  async getComplianceChecks() {
    return this.apiCall('/compliance/checks/');
  }

  async getComplianceReports() {
    return this.apiCall('/compliance/reports/');
  }

  async getComplianceStats() {
    return this.apiCall('/compliance/checks/stats/');
  }

  // Audit Trail endpoints
  async getAuditTrail() {
    return this.apiCall('/audit-trail/');
  }

  async getAuditStats() {
    return this.apiCall('/audit-trail/stats/');
  }

  async exportAuditTrail() {
    return this.apiCall('/audit-trail/export/');
  }
}

// Export singleton instance
export default new ApiService();
