import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button } from 'flowbite-react';
import { useAuth } from '../context/AuthContext';

const DialogueVoice = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const userId = user?.id || 'guest';
  
  const [isRecording, setIsRecording] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const speechSynthesisRef = useRef(window.speechSynthesis);
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
      sendMessageToAI(location.state.initialMessage);
    }
    // eslint-disable-next-line
  }, [location.state]);

  // Clean up speech synthesis on unmount
  useEffect(() => {
    return () => {
      if (speechSynthesisRef.current.speaking) {
        speechSynthesisRef.current.cancel();
      }
    };
  }, []);

  const sendMessageToAI = async (message) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/chat/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          message: message,
          conversation_id: conversationId
        })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { text: data.message || 'AI response here (mock)', isUser: false }]);
      if (data.conversation_id) setConversationId(data.conversation_id);
      
      // Speak the AI response
      console.log("Speaking text:", data.message || 'AI response here (mock)');
      speakText(data.message || 'AI response here (mock)');
    } catch (error) {
      console.error('Error sending message to AI:', error);
      setMessages(prev => [...prev, { text: 'Error getting AI response.', isUser: false }]);
    } finally {
      setLoading(false);
    }
  };

  const speakText = (text) => {
    if (speechSynthesisRef.current.speaking) {
      speechSynthesisRef.current.cancel();
    }
    
    setIsSpeaking(true);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onend = () => setIsSpeaking(false);
    speechSynthesisRef.current.speak(utterance);
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Use WebM format with Opus codec
      const options = { 
        mimeType: 'audio/webm;codecs=opus',
        audioBitsPerSecond: 128000
      };
      
      // Check if the browser supports the specified MIME type
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        console.warn('WebM format not supported, falling back to default format');
        mediaRecorderRef.current = new MediaRecorder(stream);
      } else {
        mediaRecorderRef.current = new MediaRecorder(stream, options);
      }
      
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorderRef.current.onstop = async () => {
        // Create a blob with WebM MIME type
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await convertSpeechToText(audioBlob);
        
        // Stop all tracks to release the microphone
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const convertSpeechToText = async (audioBlob) => {
    try {
      // Create a FormData object to send the audio file
      const formData = new FormData();
      
      // Always use WebM format for the file extension
      formData.append('audio_file', audioBlob, 'recording.webm');
      
      // Send the audio to a speech-to-text API
      const response = await fetch('http://localhost:8000/api/v1/chat/speech-to-text', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Speech-to-text conversion failed: ${errorData.detail || 'Unknown error'}`);
      }
      
      const data = await response.json();
      const transcribedText = data.text;
      
      if (transcribedText) {
        // Add user message to the conversation
        const userMsg = { text: transcribedText, isUser: true };
        setMessages(prev => [...prev, userMsg]);
        
        // Send to AI and get response
        setLoading(true);
        await sendMessageToAI(transcribedText);
      }
    } catch (error) {
      console.error('Error converting speech to text:', error);
      alert(`Failed to convert speech to text: ${error.message}`);
    }
  };

  const toggleVoiceRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const switchToTextMode = () => {
    // Pass the current conversation to the text mode
    navigate('/dialogue/text', { 
      state: { 
        messages: messages,
        conversationId: conversationId
      } 
    });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Messages display area */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <div 
            key={index} 
            className={`mb-4 p-3 rounded-lg max-w-[80%] ${
              msg.isUser 
                ? 'bg-blue-100 ml-auto' 
                : 'bg-white border border-gray-200'
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="flex justify-center my-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Recording visualization */}
      <div className="flex-1 flex items-center justify-center">
        {isRecording ? (
          <div className="flex space-x-2">
            <div className="w-6 h-10 bg-pink-600 rounded-full animate-pulse" />
            <div className="w-6 h-10 bg-pink-600 rounded-full animate-pulse delay-100" />
            <div className="w-6 h-10 bg-pink-600 rounded-full animate-pulse delay-200" />
            <div className="w-6 h-10 bg-pink-600 rounded-full animate-pulse delay-300" />
          </div>
        ) : isSpeaking ? (
          <div className="text-gray-500">AI is speaking...</div>
        ) : (
          <div className="text-gray-400">Press and hold to speak</div>
        )}
      </div>
      
      {/* Controls */}
      <div className="border-t p-4 bg-white flex items-center justify-center">
        <Button
          color={isRecording ? 'failure' : 'light'}
          onMouseDown={startRecording}
          onMouseUp={stopRecording}
          onTouchStart={startRecording}
          onTouchEnd={stopRecording}
        >
          <span>Hold to talk</span>
        </Button>
        {/* Keyboard button */}
        <Button
          color="light"
          className="ml-1"
          onClick={switchToTextMode}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <rect x="3" y="7" width="18" height="10" rx="2" strokeWidth="2" />
            <path d="M7 13h.01M11 13h.01M15 13h.01" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </Button>
      </div>
    </div>
  );
};

export default DialogueVoice; 