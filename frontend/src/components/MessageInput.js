import React, { useState } from 'react';

const MessageInput = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const containerStyle = {
    display: 'flex',
    padding: '16px',
    borderTop: '1px solid #e0e0e0',
    backgroundColor: '#fff',
    gap: '8px',
  };

  const inputStyle = {
    flex: 1,
    padding: '12px 16px',
    border: '1px solid #ddd',
    borderRadius: '24px',
    fontSize: '14px',
    outline: 'none',
    resize: 'none',
    minHeight: '20px',
    maxHeight: '120px',
    fontFamily: 'inherit',
  };

  const buttonStyle = {
    padding: '12px 24px',
    backgroundColor: disabled ? '#ccc' : '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '24px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'background-color 0.2s',
  };

  return (
    <form onSubmit={handleSubmit} style={containerStyle}>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={disabled ? "Processing..." : "Ask me about your sales data..."}
        disabled={disabled}
        style={inputStyle}
        rows={1}
      />
      <button
        type="submit"
        disabled={!message.trim() || disabled}
        style={buttonStyle}
      >
        {disabled ? '...' : 'Send'}
      </button>
    </form>
  );
};

export default MessageInput; 