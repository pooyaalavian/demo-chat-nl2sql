# 🚀 Deployment Guide - Environment Variables Setup

This guide explains how to configure environment variables for both the backend and frontend components of your NL2SQL Chat application.

## 📋 Overview

Your application now uses environment variables for all configuration, making it easy to deploy across different environments while keeping sensitive data secure.

## 🔧 Backend Configuration

### Environment Variables Required

The backend requires these environment variables in your `.env` file:

```bash
# Azure OpenAI Configuration (Responses API)
AZURE_OPENAI_ENDPOINT=https://cajo-m6jmk8i6-eastus2.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
AZURE_OPENAI_API_VERSION=preview

# Azure SQL Database Configuration
AZURE_SQL_SERVER=api-sqltestserver.database.windows.net
AZURE_SQL_DATABASE=api-sqltest
AZURE_SQL_USERNAME=apigtesting
AZURE_SQL_PASSWORD=your-password-here
```

### ✅ What's Been Updated

1. **Responses API Integration**: Updated to use Azure OpenAI's new stateful Responses API
2. **Configuration Validation**: The backend now validates all required environment variables on startup
3. **Centralized Config**: New `src/config.py` module manages all configuration
4. **Error Handling**: Clear error messages if environment variables are missing
5. **Startup Logging**: Configuration status is logged when the server starts
6. **Function Calling**: Enhanced function calling support with the Responses API

### Running the Backend

```bash
cd backend
python main.py
```

You'll see output like:
```
🚀 Starting NL2SQL Chat Backend...
✅ Environment configuration loaded successfully:
   Azure OpenAI Endpoint: https://cajo-m6jmk8i6-eastus2.openai.azure.com/
   Azure OpenAI Deployment: gpt-4.1
   Azure OpenAI API Version: 2024-12-01-preview
   Azure SQL Server: api-sqltestserver.database.windows.net
   Azure SQL Database: api-sqltest
   Azure SQL Username: apigtesting
   🔒 Sensitive credentials loaded but not displayed
🌐 Starting Flask server on port 4000...
```

### 🔄 Responses API Integration

Your application now uses Azure OpenAI's **Responses API**, which is a new stateful API that provides:

- **Enhanced function calling** with better context management
- **Stateful conversations** that maintain context across interactions
- **Improved tool integration** for SQL queries and database operations
- **Better error handling** and response management

**Key Changes:**
- API endpoint format: `https://your-resource.openai.azure.com/openai/v1/`
- API version: `preview` (instead of date-based versions)
- Client configuration uses `base_url` instead of `azure_endpoint`
- Response format includes richer output structures

**Testing Your Configuration:**
```bash
python test_responses_api.py
```

## 🎨 Frontend Configuration

### Environment Variables (Optional)

The frontend has sensible defaults but can be customized. Create `frontend/.env`:

```bash
# Backend API URL (defaults to http://localhost:4000)
REACT_APP_API_BASE_URL=http://localhost:4000

# Optional: API timeout in milliseconds
REACT_APP_API_TIMEOUT=10000

# Optional: Retry attempts for failed requests
REACT_APP_API_RETRY_ATTEMPTS=3
```

### ✅ What's Been Updated

1. **Configuration Module**: New `src/config/api.config.js` centralizes frontend config
2. **Environment Support**: Uses `REACT_APP_*` variables with fallbacks
3. **Development Logging**: API requests are logged in development mode
4. **Flexible API URLs**: Easy to change for different deployment environments

### Running the Frontend

```bash
cd frontend
npm install
npm start
```

## 🌐 Production Deployment

### Backend (Azure App Service)

1. **Deploy to Azure App Service**
2. **Set Environment Variables** in App Service Configuration:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-production-key
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
   AZURE_SQL_SERVER=your-prod-server.database.windows.net
   AZURE_SQL_DATABASE=your-prod-database
   AZURE_SQL_USERNAME=your-prod-username
   AZURE_SQL_PASSWORD=your-prod-password
   ```

### Frontend (Azure Static Web Apps)

1. **Build the frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Set build-time environment variables** (if needed):
   ```bash
   REACT_APP_API_BASE_URL=https://your-backend.azurewebsites.net
   ```

3. **Deploy to Azure Static Web Apps**

## 🔒 Security Best Practices

### Backend Security
- ✅ Environment variables are loaded from `.env` file
- ✅ Sensitive data never appears in logs
- ✅ Configuration validation prevents startup with missing credentials
- ✅ SQL connection uses encrypted connections

### Frontend Security
- ✅ Only non-sensitive configuration exposed to frontend
- ✅ API keys never included in frontend code
- ✅ CORS configured for security
- ✅ Environment variables properly scoped

## 🧪 Testing Your Configuration

### Backend Test
```bash
python test.py
```

### Frontend Test
1. Open browser to `http://localhost:3000`
2. Check browser console for API requests
3. Verify connection status indicator shows "Connected"

## 🐛 Troubleshooting

### Backend Issues

**"Missing required environment variables"**
- Check your `.env` file exists in the project root
- Verify all required variables are present
- Ensure there are no typos in variable names

**SQL Connection Errors**
- Verify Azure SQL server allows connections
- Check firewall settings
- Confirm credentials are correct

**Azure OpenAI Errors**
- Verify API key is valid
- Check deployment name matches your Azure resource
- Ensure endpoint URL is correct
- For Responses API: Use `api_version=preview` instead of date-based versions
- Ensure your model supports the Responses API (gpt-4.1, gpt-4o, etc.)

### Frontend Issues

**"Failed to connect to backend"**
- Ensure backend is running on port 4000
- Check `REACT_APP_API_BASE_URL` if using custom configuration
- Verify CORS is enabled in backend

**Environment variables not working**
- Restart React development server after changing `.env`
- Ensure variables start with `REACT_APP_`
- Check browser Network tab for actual API URLs being used

## 📁 File Structure Summary

```
demo-chat-nl2sql/
├── .env                     # Backend environment variables
├── backend/
│   ├── src/
│   │   ├── config.py       # ✅ NEW: Configuration management
│   │   ├── conversation.py # ✅ UPDATED: Uses config module
│   │   └── sqlutil.py      # ✅ UPDATED: Uses config module
│   └── main.py             # ✅ UPDATED: Logs configuration
├── frontend/
│   ├── .env                # Frontend environment variables (optional)
│   ├── src/
│   │   ├── config/
│   │   │   └── api.config.js # ✅ NEW: Frontend configuration
│   │   └── services/
│   │       └── api.js      # ✅ UPDATED: Uses config module
│   └── ENVIRONMENT.md      # ✅ NEW: Frontend config guide
└── DEPLOYMENT.md           # ✅ NEW: This file
```

## 🎉 Benefits of This Setup

- **🔧 Easy Configuration**: Change settings without touching code
- **🔒 Secure**: Sensitive data in environment variables, not source code
- **🚀 Deployment Ready**: Works across development, staging, and production
- **🐛 Debug Friendly**: Clear error messages and logging
- **📈 Scalable**: Easy to add new configuration options

Your application is now properly configured to use environment variables! 🎊 