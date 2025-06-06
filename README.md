# NL2SQL Chat Application

A full-stack Natural Language to SQL chat application that allows users to ask questions about their sales data in plain English. The AI assistant converts natural language queries into SQL and executes them against your database.

## 🚀 Features

- **Natural Language Processing**: Ask questions in plain English
- **SQL Query Generation**: Automatically converts questions to SQL queries
- **Real-time Chat Interface**: Modern, responsive chat UI
- **Database Integration**: Connects to Microsoft SQL Server
- **Azure OpenAI Integration**: Uses Azure OpenAI for intelligent responses
- **Function Calling**: AI can execute SQL queries and analyze data
- **Error Handling**: Comprehensive error handling and user feedback

## 🏗️ Architecture

```
demo-chat-nl2sql/
├── backend/                 # Flask API server
│   ├── src/
│   │   ├── conversation.py  # Chat conversation management
│   │   ├── sqlutil.py      # SQL database utilities
│   │   └── __init__.py
│   └── main.py             # Flask application entry point
├── frontend/               # React web application
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── requirements.txt        # Python dependencies
├── test.py                # Backend testing script
└── README.md              # This file
```

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **Azure OpenAI** - AI/ML service for natural language processing
- **pyodbc** - SQL Server database connectivity
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - User interface framework
- **Axios** - HTTP client for API communication
- **CSS-in-JS** - Component styling

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- Microsoft SQL Server (or Azure SQL Database)
- Azure OpenAI account and API key

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd demo-chat-nl2sql
```

### 2. Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```bash
   # Azure OpenAI Configuration
   OPENAI_ENDPOINT_URL=https://your-resource.openai.azure.com/
   OPENAI_DEPLOYMENT_NAME=your-deployment-name
   OPENAI_API_KEY=your-api-key

   # SQL Server Configuration
   SQL_SERVER_CONN_STR=Driver={ODBC Driver 17 for SQL Server};Server=your-server;Database=your-database;Uid=your-username;Pwd=your-password;
   ```

3. **Start the Flask server:**
   ```bash
   cd backend
   python main.py
   ```
   
   The backend will run on `http://localhost:4000`

### 3. Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will open in your browser at `http://localhost:3000`

## 💡 Usage

1. **Start the Application**: 
   - Ensure both backend and frontend servers are running
   - Open your browser to `http://localhost:3000`

2. **Begin Chatting**:
   - The app automatically creates a new conversation
   - Type natural language questions about your sales data

3. **Example Questions**:
   - "How many customers do we have?"
   - "Show me sales by region"
   - "What are our top-selling products this month?"
   - "Break down revenue by salesperson"

## 🔧 API Endpoints

### Backend API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/test` | Health check endpoint |
| POST | `/conversation` | Create new conversation |
| GET | `/conversation/<id>` | Get conversation by ID |
| POST | `/conversation/<id>` | Send message to conversation |
| POST | `/sql/query` | Execute direct SQL query |

## 🧪 Testing

### Backend Testing

Use the provided test script:

```bash
python test.py
```

This script demonstrates:
- Creating conversations
- Sending messages
- Direct SQL query execution

### Frontend Testing

```bash
cd frontend
npm test
```

## 🔒 Security Considerations

- **Environment Variables**: Store sensitive data in `.env` files
- **SQL Injection**: The application uses parameterized queries
- **CORS**: Configured for development; adjust for production
- **API Keys**: Never commit API keys to version control

## 🚀 Deployment

### Backend Deployment (Azure)

1. **Azure App Service**:
   - Deploy Flask app to Azure App Service
   - Configure environment variables in App Service settings
   - Ensure SQL Server connectivity

2. **Azure Functions** (Alternative):
   - Convert Flask routes to Azure Functions
   - Use Azure Functions for serverless deployment

### Frontend Deployment

1. **Build for production**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Azure Static Web Apps**:
   - Connect your GitHub repository
   - Configure build settings
   - Deploy automatically on push

## 🐛 Troubleshooting

### Common Issues

**Backend Connection Error**:
- Verify Azure OpenAI credentials
- Check SQL Server connection string
- Ensure all environment variables are set

**Frontend Connection Error**:
- Confirm backend is running on port 4000
- Check CORS configuration
- Verify API endpoints are accessible

**Database Connection Issues**:
- Test SQL Server connectivity
- Verify ODBC driver installation
- Check firewall settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Azure OpenAI team for the powerful AI capabilities
- Flask and React communities for excellent frameworks
- Microsoft for SQL Server integration tools

---

**Need Help?** Create an issue in the repository or contact the development team. 