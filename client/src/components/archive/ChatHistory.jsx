import React, { useState, useEffect } from 'react';
import { getIncidentConversations } from '../../services/api';

const ChatHistory = ({ incidentId }) => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const data = await getIncidentConversations(incidentId);
        setConversations(data);
      } catch (err) {
        setError('Failed to load conversations');
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, [incidentId]);

  if (loading) return <div className="text-gray-400">Loading conversations...</div>;
  if (error) return <div className="text-red-600">{error}</div>;
  if (!conversations || conversations.length === 0) {
    return <div className="text-gray-400">No conversations yet.</div>;
  }

  return (
    <div className="space-y-4">
      {conversations.map(conversation => (
        <div key={conversation.id} className="border-b pb-4">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium">{conversation.title}</h4>
            <span className="text-xs text-gray-500">
              {new Date(conversation.created_at).toLocaleDateString()}
            </span>
          </div>
          <div className="space-y-2">
            {conversation.messages.map(message => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`rounded-lg px-4 py-2 max-w-[80%] ${
                    message.role === 'user'
                      ? 'bg-blue-100 text-blue-900'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <div className="text-sm">{message.content}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(message.created_at).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatHistory; 