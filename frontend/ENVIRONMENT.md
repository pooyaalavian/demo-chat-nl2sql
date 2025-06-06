# Frontend Environment Configuration

This document explains how to configure environment variables for the React frontend.

## Environment Variables

React only recognizes environment variables that start with `REACT_APP_`. Create a `.env` file in the `frontend/` directory with the following variables:

### Required Variables

```bash
# Backend API Configuration
REACT_APP_API_BASE_URL=http://localhost:4000

# Optional Configuration
REACT_APP_API_TIMEOUT=10000
REACT_APP_API_RETRY_ATTEMPTS=3
```

### Example .env File

Create `frontend/.env`:

```bash
# Backend API URL - Change this for production deployment
REACT_APP_API_BASE_URL=http://localhost:4000

# API timeout in milliseconds (optional, defaults to 10000)
REACT_APP_API_TIMEOUT=10000

# Number of retry attempts for failed API calls (optional, defaults to 3)
REACT_APP_API_RETRY_ATTEMPTS=3
```

## Production Configuration

For production deployment, update `REACT_APP_API_BASE_URL` to point to your deployed backend:

```bash
# Example for Azure App Service
REACT_APP_API_BASE_URL=https://your-app-name.azurewebsites.net

# Example for custom domain
REACT_APP_API_BASE_URL=https://api.yourdomain.com
```

## Security Notes

- ⚠️ **Never put sensitive data in frontend environment variables**
- All `REACT_APP_*` variables are embedded in the built JavaScript and are visible to users
- Only put configuration that's safe to be public (like API endpoints)
- Never put API keys, passwords, or secrets in frontend environment variables

## Configuration Validation

The frontend will automatically:
- Use `http://localhost:4000` as the default API URL if not specified
- Log API requests in development mode
- Handle connection errors gracefully
- Retry failed requests according to configuration

## Troubleshooting

If environment variables aren't working:

1. Ensure the variable name starts with `REACT_APP_`
2. Restart the development server after adding new variables
3. Check the browser's Network tab to verify the API URL being used
4. Verify the `.env` file is in the `frontend/` directory (not the project root)

## File Structure

```
frontend/
├── .env                    # Environment variables (create this)
├── src/
│   └── config/
│       └── api.config.js   # Configuration logic
└── ENVIRONMENT.md          # This file
``` 