import React from 'react';

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  
  const messageStyle = {
    marginBottom: '16px',
    display: 'flex',
    justifyContent: isUser ? 'flex-end' : 'flex-start',
  };

  const bubbleStyle = {
    maxWidth: '70%',
    padding: '12px 16px',
    borderRadius: '18px',
    backgroundColor: isUser ? '#007bff' : '#f1f3f4',
    color: isUser ? 'white' : '#333',
    wordWrap: 'break-word',
    whiteSpace: 'pre-wrap',
    fontSize: '14px',
    lineHeight: '1.4',
  };

  const labelStyle = {
    fontSize: '12px',
    color: '#666',
    marginBottom: '4px',
    textAlign: isUser ? 'right' : 'left',
  };

  return (
    <div style={messageStyle}>
      <div>
        <div style={labelStyle}>
          {isUser ? 'You' : 'Assistant'}
        </div>
        <div style={bubbleStyle}>
          {message.content}
        </div>
      </div>
    </div>
  );
};

export default Message; 