import axios from 'axios';
import config from '../config/api.config';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: config.API_BASE_URL,
      timeout: config.API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    // Add request interceptor for logging in development
    if (config.IS_DEVELOPMENT) {
      this.client.interceptors.request.use(request => {
        console.log('API Request:', request.method?.toUpperCase(), request.url);
        return request;
      });
    }
  }

  // Test the backend connection
  async testConnection() {
    try {
      const response = await this.client.get('/test');
      return response.data;
    } catch (error) {
      console.error('Test connection failed:', error);
      throw error;
    }
  }

  // Create a new conversation
  async createConversation() {
    try {
      const response = await this.client.post('/conversation');
      return response.data.conversation;
    } catch (error) {
      console.error('Failed to create conversation:', error);
      throw error;
    }
  }

  // Get conversation by ID
  async getConversation(conversationId) {
    try {
      const response = await this.client.get(`/conversation/${conversationId}`);
      return response.data.conversation;
    } catch (error) {
      console.error('Failed to get conversation:', error);
      throw error;
    }
  }

  // Send a message to a conversation
  async sendMessage(conversationId, message) {
    try {
      const response = await this.client.post(`/conversation/${conversationId}`, {
        message: message
      });
      return response.data.conversation;
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    }
  }

  // Run a direct SQL query
  async runSqlQuery(query, params = []) {
    try {
      const response = await this.client.post('/sql/query', {
        query: query,
        params: params
      });
      return response.data.results;
    } catch (error) {
      console.error('Failed to run SQL query:', error);
      throw error;
    }
  }
}

export default new ApiService(); 