import React, { useState } from 'react';
import { Button, TextInput } from 'flowbite-react';

const ChatMessage = ({ message, isUser }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
    <div className={`max-w-[70%] rounded-lg p-3 ${
      isUser ? 'bg-blue-600 text-white' : 'bg-gray-100'
    }`}>
      {message}
    </div>
  </div>
);

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    
    setMessages([...messages, { text: inputText, isUser: true }]);
    setInputText('');
    // Add AI response logic here
  };

  const toggleVoiceRecording = () => {
    setIsRecording(!isRecording);
    // Add voice recording logic here
  };

  return (
    <div className="flex flex-col h-full max-w-2xl mx-auto">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            message={msg.text}
            isUser={msg.isUser}
          />
        ))}
      </div>
      
      <div className="border-t p-4">
        <div className="flex gap-2">
          <TextInput
            className="flex-1"
            placeholder="Ask me anything..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <Button
            color={isRecording ? 'failure' : 'light'}
            onClick={toggleVoiceRecording}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
              />
            </svg>
          </Button>
          <Button onClick={handleSendMessage}>Send</Button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 