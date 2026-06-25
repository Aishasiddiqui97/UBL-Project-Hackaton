import apiService from '../services/api';

// Token refresh utility
export const refreshAuthToken = async () => {
  try {
    const response = await apiService.refreshToken();
    
    if (response.access) {
      localStorage.setItem('access_token', response.access);
      return response.access;
    }
    
    throw new Error('No access token in response');
  } catch (error) {
    // Refresh failed, logout user
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('user');
    
    window.location.href = '/login';
    throw error;
  }
};

// Check if token is expired (rough check)
export const isTokenExpired = (token) => {
  if (!token) return true;
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000 < Date.now();
  } catch (error) {
    return true;
  }
};

// Setup automatic token refresh
export const setupTokenRefresh = () => {
  setInterval(async () => {
    const token = localStorage.getItem('access_token');
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    
    if (isAuthenticated && token && isTokenExpired(token)) {
      try {
        await refreshAuthToken();
        console.log('Token refreshed successfully');
      } catch (error) {
        console.error('Token refresh failed:', error);
      }
    }
  }, 5 * 60 * 1000); // Check every 5 minutes
};