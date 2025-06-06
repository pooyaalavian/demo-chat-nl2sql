import React, { useState, useEffect, useRef } from 'react';
import Message from './Message';
import MessageInput from './MessageInput';
import ApiService from '../services/api';

const ChatWindow = () => {
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    initializeChat();
  }, []);

  const initializeChat = async () => {
    try {
      setConnectionStatus('connecting');
      
      // Test backend connection
      await ApiService.testConnection();
      setConnectionStatus('connected');
      
      // Create a new conversation
      const newConversation = await ApiService.createConversation();
      setConversation(newConversation);
      setMessages(newConversation.messages || []);
      setError(null);
    } catch (err) {
      console.error('Failed to initialize chat:', err);
      setConnectionStatus('error');
      setError('Failed to connect to the backend. Please ensure the Flask server is running on port 4000.');
    }
  };

  const handleSendMessage = async (messageText) => {
    if (!conversation) {
      setError('No active conversation. Please refresh the page.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const updatedConversation = await ApiService.sendMessage(conversation.conversation_id, messageText);
      setMessages(updatedConversation.messages || []);
    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    initializeChat();
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    maxWidth: '800px',
    margin: '0 auto',
    backgroundColor: '#fff',
    boxShadow: '0 0 20px rgba(0,0,0,0.1)',
  };

  const headerStyle = {
    padding: '16px 24px',
    backgroundColor: '#007bff',
    color: 'white',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '1px solid #e0e0e0',
  };

  const statusStyle = {
    fontSize: '12px',
    padding: '4px 8px',
    borderRadius: '12px',
    backgroundColor: connectionStatus === 'connected' ? '#28a745' : 
                    connectionStatus === 'error' ? '#dc3545' : '#ffc107',
    color: 'white',
  };

  const messagesStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '16px 24px',
    backgroundColor: '#f8f9fa',
  };

  const errorStyle = {
    padding: '12px 16px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    border: '1px solid #f5c6cb',
    borderRadius: '4px',
    margin: '16px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  const emptyStateStyle = {
    textAlign: 'center',
    color: '#666',
    fontSize: '16px',
    marginTop: '48px',
  };

  const retryButtonStyle = {
    padding: '6px 12px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
  };

  if (connectionStatus === 'error') {
    return (
      <div style={containerStyle}>
        <div style={headerStyle}>
          <h1 style={{ margin: 0, fontSize: '20px' }}>NL2SQL Chat</h1>
          <span style={statusStyle}>Connection Error</span>
        </div>
        <div style={errorStyle}>
          <span>{error}</span>
          <button onClick={handleRetry} style={retryButtonStyle}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h1 style={{ margin: 0, fontSize: '20px' }}>NL2SQL Chat Assistant</h1>
        <span style={statusStyle}>
          {connectionStatus === 'connected' ? 'Connected' : 'Connecting...'}
        </span>
      </div>

      {error && (
        <div style={errorStyle}>
          <span>{error}</span>
          <button onClick={() => setError(null)} style={retryButtonStyle}>
            Dismiss
          </button>
        </div>
      )}

      <div style={messagesStyle}>
        {messages.length === 0 ? (
          <div style={emptyStateStyle}>
            <p>👋 Welcome to your NL2SQL Assistant!</p>
            <p>Ask me questions about your sales data and I'll help you find the answers.</p>
            <p style={{ fontSize: '14px', color: '#999' }}>
              Example: "How many customers do we have?" or "Show me sales by region"
            </p>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <Message key={index} message={message} />
            ))}
            {isLoading && (
              <div style={{ textAlign: 'center', color: '#666', padding: '16px' }}>
                <span>🤔 Thinking...</span>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={isLoading || connectionStatus !== 'connected'}
      />
    </div>
  );
};

export default ChatWindow; 