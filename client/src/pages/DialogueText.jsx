import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from 'flowbite-react';

const DialogueText = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const userId = user?.id || 'guest';
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef(null);
  const hasSentInitialMessage = useRef(false);
  const isFirstRender = useRef(true);

  // Scroll behavior: top on first render, bottom on new messages
  useEffect(() => {
    if (isFirstRender.current) {
      // On first render, scroll to top
      if (messagesEndRef.current && messagesEndRef.current.parentNode) {
        messagesEndRef.current.parentNode.scrollTop = 0;
      }
      isFirstRender.current = false;
    } else {
      // On subsequent updates, scroll to bottom
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // On mount, if initialMessage exists, add it and get AI response
  useEffect(() => {
    if (
      !hasSentInitialMessage.current &&
      location.state &&
      location.state.initialMessage
    ) {
      hasSentInitialMessage.current = true;
      const userMsg = { text: location.state.initialMessage, isUser: true };
      setMessages([userMsg]);
      setLoading(true);
      fetch('http://localhost:8000/api/v1/chat/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          message: location.state.initialMessage,
          conversation_id: conversationId
        })
      })
        .then(res => res.json())
        .then(data => {
          setMessages(prev => [...prev, { text: data.message || 'AI response here (mock)', isUser: false }]);
          if (data.conversation_id) setConversationId(data.conversation_id);
        })
        .catch(() => {
          setMessages(prev => [...prev, { text: 'Error getting AI response.', isUser: false }]);
        })
        .finally(() => setLoading(false));
    }
    // eslint-disable-next-line
  }, [location.state]);

  // Handle switching from voice mode with existing conversation
  useEffect(() => {
    if (location.state && location.state.messages) {
      setMessages(location.state.messages);
      if (location.state.conversationId) {
        setConversationId(location.state.conversationId);
      }
    }
  }, [location.state]);

  const handleSend = () => {
    if (!inputText.trim()) return;
    const userMsg = { text: inputText, isUser: true };
    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setLoading(true);
    fetch('http://localhost:8000/api/v1/chat/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        message: inputText,
        conversation_id: conversationId
      })
    })
      .then(res => res.json())
      .then(data => {
        setMessages(prev => [...prev, { text: data.message || 'AI response here (mock)', isUser: false }]);
        if (data.conversation_id) setConversationId(data.conversation_id);
      })
      .catch(() => {
        setMessages(prev => [...prev, { text: 'Error getting AI response.', isUser: false }]);
      })
      .finally(() => setLoading(false));
  };

  const toggleVoiceRecording = () => {
    setIsRecording(!isRecording);
    // Navigate to /dialogue/voice
    navigate('/dialogue/voice');
    // Voice recording logic would go here
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 relative">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-2 flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`rounded-lg px-4 py-2 ${msg.isUser ? 'bg-pink-600 text-white' : 'bg-gray-200'}`}>{msg.text}</div>
          </div>
        ))}
        {loading && <div className="text-center text-gray-400">AI is typing...</div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="border-t p-4 bg-white flex items-center fixed bottom-0 left-0 w-full z-10">
        <input
          type="text"
          placeholder="Ask me anything..."
          className="flex-1 border rounded-l-full px-4 py-2 focus:outline-none"
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          disabled={loading}
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
        <button className="bg-teal-700 text-white px-6 py-2 rounded-r-full ml-1" onClick={handleSend} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default DialogueText; 