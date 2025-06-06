import React from 'react';
import ChatWindow from './components/ChatWindow';

function App() {
  const appStyle = {
    height: '100vh',
    backgroundColor: '#f5f5f5',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  return (
    <div style={appStyle}>
      <ChatWindow />
    </div>
  );
}

export default App; 