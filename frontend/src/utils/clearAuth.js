/**
 * Clear all authentication data from localStorage
 * Use this if you're having token issues
 */
export const clearAllAuthData = () => {
  console.log('Clearing all authentication data...');
  
  // Clear all possible auth keys
  const authKeys = [
    'access_token',
    'refresh_token', 
    'isAuthenticated',
    'user',
    'token',
    'authToken',
    'jwt_token'
  ];
  
  authKeys.forEach(key => {
    localStorage.removeItem(key);
  });
  
  // Clear session storage too
  authKeys.forEach(key => {
    sessionStorage.removeItem(key);
  });
  
  console.log('All authentication data cleared');
  
  // Reload page to start fresh
  window.location.reload();
};

// Auto-clear invalid tokens on app load
export const checkAndClearInvalidTokens = () => {
  const token = localStorage.getItem('access_token');
  
  if (token && (token === 'undefined' || token === 'null' || token === '')) {
    console.log('Invalid token detected, clearing...');
    clearAllAuthData();
  }
};