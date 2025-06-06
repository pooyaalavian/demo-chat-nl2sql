// API Configuration
// This file centralizes all API-related configuration

const config = {
  // Backend API base URL - can be overridden by environment variable
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:4000',
  
  // API timeout in milliseconds
  API_TIMEOUT: process.env.REACT_APP_API_TIMEOUT || 30000,
  
  // Retry attempts for failed requests
  API_RETRY_ATTEMPTS: process.env.REACT_APP_API_RETRY_ATTEMPTS || 3,
  
  // Development mode flag
  IS_DEVELOPMENT: process.env.NODE_ENV === 'development',
};

export default config; 