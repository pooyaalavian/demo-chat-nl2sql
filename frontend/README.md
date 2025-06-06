# NL2SQL Chat Frontend

A React-based chat interface for the NL2SQL assistant that allows users to ask natural language questions about their sales data.

## Features

- 💬 **Real-time Chat Interface**: Clean, modern chat UI with message bubbles
- 🔄 **Auto-scroll**: Messages automatically scroll to show the latest conversation
- 🔗 **Backend Integration**: Seamlessly connects to the Flask backend API
- ⚡ **Connection Status**: Shows real-time connection status with the backend
- 🎯 **Error Handling**: User-friendly error messages and retry functionality
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Flask backend running on port 4000

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will open in your browser at `http://localhost:3000`.

### Backend Connection

The frontend is configured to connect to the Flask backend at `http://localhost:4000`. Make sure your backend server is running before starting the frontend.

## Usage

1. **Start a Conversation**: The app automatically creates a new conversation when you load the page
2. **Ask Questions**: Type natural language questions about your sales data
3. **View Responses**: The AI assistant will respond with answers and can execute SQL queries to fetch data
4. **Error Handling**: If there are connection issues, use the retry button to reconnect

### Example Questions

- "How many customers do we have?"
- "Show me sales by region"
- "What are our top-selling products?"
- "Break down sales by salesperson"

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   ├── ChatWindow.js   # Main chat interface
│   │   ├── Message.js      # Individual message component
│   │   └── MessageInput.js # Message input form
│   ├── services/
│   │   └── api.js          # API service for backend communication
│   ├── App.js              # Main app component
│   └── index.js            # App entry point
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

## Technologies Used

- **React 18** - UI framework
- **Axios** - HTTP client for API calls
- **CSS-in-JS** - Inline styling for components
- **Create React App** - Build tooling and development server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues

**Connection Error**: If you see "Failed to connect to the backend":
- Ensure the Flask backend is running on port 4000
- Check that CORS is properly configured in the backend
- Verify your network connection

**Build Errors**: If npm install fails:
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility

**Performance Issues**: If the app is slow:
- Check browser developer tools for network issues
- Ensure backend responses are timely
- Consider implementing message pagination for long conversations 