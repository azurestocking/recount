import React, { useState, useEffect, useRef } from 'react';
import { Button, TextInput, Spinner, Alert } from 'flowbite-react';
import { chatAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

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
  const { user, isGuest } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  
  // Get user ID from auth context
  const userId = user?.id || 'guest';

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history if conversationId exists
  useEffect(() => {
    const loadConversationHistory = async () => {
      if (conversationId) {
        try {
          setLoading(true);
          const response = await chatAPI.getConversationHistory(conversationId);
          if (response.data.history) {
            const formattedMessages = response.data.history.map(msg => ({
              text: msg.content,
              isUser: msg.sender === userId
            }));
            setMessages(formattedMessages);
          }
        } catch (error) {
          console.error('Error loading conversation history:', error);
          setError('Failed to load conversation history. Please try again later.');
        } finally {
          setLoading(false);
        }
      }
    };

    loadConversationHistory();
  }, [conversationId, userId]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    
    const newMessage = { text: inputText, isUser: true };
    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setLoading(true);
    setError(null);
    
    try {
      console.log("Sending message:", inputText);
      const response = await chatAPI.sendMessage({
        user_id: userId,
        message: inputText,
        conversation_id: conversationId
      });
      
      // If this is the first message, set the conversation ID
      if (!conversationId && response.data.conversation_id) {
        setConversationId(response.data.conversation_id);
      }
      
      // Add AI response to messages
      if (response.data.message) {
        setMessages(prev => [...prev, { 
          text: response.data.message, 
          isUser: false 
        }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message. Please try again later.');
      // Add error message
      setMessages(prev => [...prev, { 
        text: 'Sorry, there was an error processing your message. Please try again.', 
        isUser: false 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const toggleVoiceRecording = () => {
    setIsRecording(!isRecording);
    // Voice recording logic would go here
  };

  return (
    <div className="flex flex-col h-full max-w-2xl mx-auto">
      {isGuest() && (
        <Alert color="info" className="mb-4">
          <span className="font-medium">Guest Mode:</span> Your conversations will not be saved permanently.
        </Alert>
      )}
      
      {error && (
        <Alert color="failure" className="mb-4">
          {error}
        </Alert>
      )}
      
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            message={msg.text}
            isUser={msg.isUser}
          />
        ))}
        {loading && (
          <div className="flex justify-center my-4">
            <Spinner size="sm" />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="border-t p-4">
        <div className="flex gap-2">
          <TextInput
            className="flex-1"
            placeholder="Ask me anything..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            disabled={loading}
          />
          <Button
            color={isRecording ? 'failure' : 'light'}
            onClick={toggleVoiceRecording}
            disabled={loading}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
              />
            </svg>
          </Button>
          <Button onClick={handleSendMessage} disabled={loading}>
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 