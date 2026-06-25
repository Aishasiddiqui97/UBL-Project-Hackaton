// API Configuration for Django Backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// API Service Class
class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
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

  // Generic API call method
  async apiCall(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    console.log('API Call:', { url, method: options.method || 'GET', headers: config.headers });

    try {
      const response = await fetch(url, config);
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
      throw error;
    }
  }

  async logout() {
    const refresh_token = localStorage.getItem('refresh_token');
    return this.apiCall('/auth/logout/', {
      method: 'POST',
      body: JSON.stringify({ refresh_token })
    });
  }

  async refreshToken() {
    const refresh_token = localStorage.getItem('refresh_token');
    return this.apiCall('/auth/token/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refresh_token })
    });
  }

  // User endpoints - FIXED: use correct endpoint
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
}

// Export singleton instance
export default new ApiService();