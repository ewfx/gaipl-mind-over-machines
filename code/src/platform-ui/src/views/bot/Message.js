/* eslint-disable prettier/prettier */
// src/components/Message.js
import React from 'react';

const Message = ({ message, isUser }) => {
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: isUser ? 'row-reverse' : 'row',
        alignItems: 'flex-end',
        marginBottom: '10px',
      }}
    >
      {/* Avatar */}
      <div
        style={{
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          backgroundColor: isUser ? '#007bff' : '#ccc',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginLeft: isUser ? '10px' : '0',
          marginRight: isUser ? '0' : '10px',
        }}
      >
        {isUser ? '👤' : '🤖'} {/* User/Bot avatar */}
      </div>

      {/* Message Bubble */}
      <div
        style={{
          maxWidth: '70%',
          padding: '10px',
          borderRadius: '10px',
          backgroundColor: isUser ? '#dcf8c6' : '#ececec',
          position: 'relative',
        }}
      >
        <p style={{ margin: '0', wordBreak: 'break-word', color: '#000' }}>{message}</p>
        <span
          style={{
            fontSize: '10px',
            color: '#666',
            position: 'absolute',
            bottom: '2px',
            right: '5px',
          }}
        >
          {timestamp}
        </span>
      </div>
    </div>
  );
};

export default Message;